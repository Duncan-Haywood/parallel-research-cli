"""Orchestrator for managing the research synthesis process."""

import asyncio
import os
import platform
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

import anthropic
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..models.models import (
    Essay, ResearchResult, TokenUsage, Citation,
    Metadata, QualityMetrics, OutputFormat
)
from ..agents.agents import create_agents, Agent
from ..agents.advanced_agents import create_advanced_agents, get_agents_for_stage
from ..ui.dashboard import Dashboard
from ..synthesis.synthesizer import Synthesizer
from ..output.formatter import OutputFormatter


@dataclass
class Config:
    """Configuration for the orchestrator."""
    topic: str
    intensity: int = 5
    parallelism: int = 3
    best_of_n: int = 1
    output_file: str = "essay.md"
    demo_mode: bool = False
    auto_open: bool = True
    api_key: str = ""
    output_format: OutputFormat = OutputFormat.MARKDOWN
    show_dashboard: bool = True
    token_limit: int = 0
    cost_limit: float = 0.0
    claude_model: str = "claude-3-sonnet-20240229"


@dataclass
class TokenTracker:
    """Tracks token usage and costs."""
    agent_tokens: Dict[str, int] = field(default_factory=dict)
    total_tokens: int = 0
    total_cost: float = 0.0
    token_limit: int = 0
    cost_limit: float = 0.0
    
    def add_usage(self, agent_id: str, usage: TokenUsage):
        """Add token usage for an agent."""
        self.agent_tokens[agent_id] = self.agent_tokens.get(agent_id, 0) + usage.total_tokens
        self.total_tokens += usage.total_tokens
        self.total_cost += usage.cost
        
    def check_limits(self) -> bool:
        """Check if limits have been exceeded."""
        if self.token_limit > 0 and self.total_tokens > self.token_limit:
            return False
        if self.cost_limit > 0 and self.total_cost > self.cost_limit:
            return False
        return True


class Orchestrator:
    """Manages the entire research synthesis process."""
    
    def __init__(self, config: Config):
        self.config = config
        self.console = Console()
        self.claude_client = None
        self.agents = create_agents(config.intensity)
        self.dashboard = Dashboard() if config.show_dashboard else None
        self.token_tracker = TokenTracker(
            token_limit=config.token_limit,
            cost_limit=config.cost_limit
        )
        
        if not config.demo_mode:
            api_key = config.api_key or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not provided")
            self.claude_client = anthropic.Anthropic(api_key=api_key)
    
    async def execute(self) -> None:
        """Execute the research synthesis process."""
        self.console.print(f"[green]🚀 Starting research on: {self.config.topic}[/green]")
        
        if self.dashboard:
            self.dashboard.start()
        
        try:
            # Phase 1: Parallel research
            research_results = await self.conduct_parallel_research()
            
            # Phase 2: Synthesis
            essay = await self.synthesize_results(research_results)
            
            # Phase 3: Output
            await self.write_output(essay)
            
            self.console.print(f"[green]✅ Research complete! Essay saved to {self.config.output_file}[/green]")
            
            if self.config.auto_open:
                self.open_file(self.config.output_file)
                
        finally:
            if self.dashboard:
                self.dashboard.close()
    
    async def conduct_parallel_research(self) -> List[ResearchResult]:
        """Conduct research using multiple agents in parallel."""
        results = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task(
                f"[cyan]Researching with {len(self.agents)} agents...",
                total=len(self.agents)
            )
            
            # Use ThreadPoolExecutor for parallel API calls
            with ThreadPoolExecutor(max_workers=self.config.parallelism) as executor:
                futures = []
                
                for agent in self.agents:
                    future = executor.submit(self._research_with_agent, agent)
                    futures.append((future, agent))
                
                for future, agent in futures:
                    try:
                        result = future.result(timeout=300)  # 5 minute timeout
                        if result:
                            results.append(result)
                            progress.advance(task)
                            
                            if self.dashboard:
                                self.dashboard.update_progress(
                                    stage="research",
                                    percentage=(len(results) / len(self.agents)) * 100,
                                    active_agents=len(self.agents) - len(results),
                                    completed_agents=len(results)
                                )
                    except Exception as e:
                        self.console.print(f"[red]Agent {agent.type.value} failed: {e}[/red]")
                        progress.advance(task)
        
        return results
    
    def _research_with_agent(self, agent: Agent) -> Optional[ResearchResult]:
        """Execute research for a single agent."""
        if self.config.demo_mode:
            # Return demo data
            return ResearchResult(
                agent_id=agent.type.value,
                agent_type=agent.type.value,
                content=f"Demo research content for {agent.type.value} on {self.config.topic}",
                citations=[
                    Citation(
                        id=f"demo-{agent.type.value}-1",
                        type="article",
                        title=f"Demo Citation for {agent.type.value}",
                        source="Demo Journal",
                        url="https://example.com",
                        authors=["Demo Author"],
                        date="2024"
                    )
                ],
                tokens_used=TokenUsage(
                    prompt_tokens=100,
                    completion_tokens=200,
                    total_tokens=300,
                    model=self.config.claude_model,
                    cost=0.01
                ),
                score=0.85
            )
        
        try:
            prompt = agent.generate_prompt(self.config.topic)
            
            # Check token limits before making API call
            if not self.token_tracker.check_limits():
                self.console.print(f"[yellow]Token/cost limit reached, skipping {agent.type.value}[/yellow]")
                return None
            
            # Make API call
            response = self.claude_client.messages.create(
                model=self.config.claude_model,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Calculate token usage
            usage = TokenUsage(
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens,
                model=self.config.claude_model,
                cost=self._calculate_cost(
                    response.usage.input_tokens,
                    response.usage.output_tokens
                )
            )
            
            # Track tokens
            self.token_tracker.add_usage(agent.type.value, usage)
            
            # Create result
            result = ResearchResult(
                agent_id=agent.type.value,
                agent_type=agent.type.value,
                content=response.content[0].text,
                citations=[],  # TODO: Extract citations from content
                tokens_used=usage,
                timestamp=datetime.now(),
                score=0.0  # TODO: Implement scoring
            )
            
            return result
            
        except Exception as e:
            self.console.print(f"[red]Error in agent {agent.type.value}: {e}[/red]")
            return None
    
    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost based on token usage."""
        # Pricing as of 2024 (adjust as needed)
        pricing = {
            "claude-3-opus-20240229": {"input": 15.0, "output": 75.0},
            "claude-3-sonnet-20240229": {"input": 3.0, "output": 15.0},
            "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25}
        }
        
        model_pricing = pricing.get(self.config.claude_model, pricing["claude-3-sonnet-20240229"])
        
        input_cost = (input_tokens / 1_000_000) * model_pricing["input"]
        output_cost = (output_tokens / 1_000_000) * model_pricing["output"]
        
        return input_cost + output_cost
    
    async def synthesize_results(self, research_results: List[ResearchResult]) -> Essay:
        """Synthesize research results into a cohesive essay."""
        self.console.print("[cyan]Synthesizing research results...[/cyan]")
        
        synthesizer = Synthesizer(
            claude_client=self.claude_client,
            model=self.config.claude_model,
            demo_mode=self.config.demo_mode
        )
        
        essay = await synthesizer.synthesize(
            topic=self.config.topic,
            research_results=research_results,
            output_format=self.config.output_format
        )
        
        # Add metadata
        essay.metadata = Metadata(
            topic=self.config.topic,
            research_depth=f"{self.config.intensity} agents",
            agents_used=len(self.agents),
            total_variations=self.config.best_of_n,
            synthesis_method="GAN-inspired adversarial synthesis",
            generation_time=timedelta(seconds=0),  # TODO: Track actual time
            total_tokens=self.token_tracker.total_tokens,
            estimated_cost=self.token_tracker.total_cost,
            quality_metrics=QualityMetrics(
                coherence=0.9,
                citation_quality=0.85,
                depth_score=0.88,
                originality=0.82,
                overall_score=0.86
            )
        )
        
        return essay
    
    async def write_output(self, essay: Essay) -> None:
        """Write the essay to the output file."""
        formatter = OutputFormatter()
        
        if self.config.output_format == OutputFormat.MARKDOWN:
            content = formatter.to_markdown(essay)
        elif self.config.output_format == OutputFormat.HTML:
            content = formatter.to_html(essay)
        elif self.config.output_format == OutputFormat.LATEX:
            content = formatter.to_latex(essay)
        else:
            content = formatter.to_markdown(essay)
        
        with open(self.config.output_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def open_file(self, filepath: str) -> None:
        """Open the file in the default application."""
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', filepath], check=True)
            elif platform.system() == 'Windows':
                os.startfile(filepath)
            else:  # Linux and others
                subprocess.run(['xdg-open', filepath], check=True)
        except Exception as e:
            self.console.print(f"[yellow]Could not open file automatically: {e}[/yellow]")