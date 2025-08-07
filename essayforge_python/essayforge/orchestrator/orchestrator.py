"""Orchestrator for coordinating research agents and synthesis."""

import asyncio
import os
import platform
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..agents import create_agents
from ..models import (
    Essay, Metadata, OutputFormat, Progress, QualityMetrics,
    ResearchResult, TokenUsage
)
from ..output import Formatter
from ..synthesis import Synthesizer
from ..ui import Dashboard


@dataclass
class Config:
    """Configuration for the orchestrator."""
    topic: str
    intensity: int
    parallelism: int
    best_of_n: int
    output_file: str
    demo_mode: bool
    auto_open: bool
    api_key: str
    output_format: OutputFormat
    show_dashboard: bool
    token_limit: int
    cost_limit: float
    claude_model: str


class TokenTracker:
    """Tracks token usage and costs."""
    
    def __init__(self, limit: int = 0, cost_limit: float = 0.0):
        self.total_tokens = 0
        self.total_cost = 0.0
        self.limit = limit
        self.cost_limit = cost_limit
        
    def add(self, usage: TokenUsage):
        """Add token usage."""
        self.total_tokens += usage.total_tokens
        self.total_cost += usage.cost
        
    def check_limits(self):
        """Check if limits have been exceeded."""
        if self.limit > 0 and self.total_tokens >= self.limit:
            raise Exception(f"Token limit exceeded: {self.total_tokens} >= {self.limit}")
        if self.cost_limit > 0 and self.total_cost >= self.cost_limit:
            raise Exception(f"Cost limit exceeded: ${self.total_cost:.2f} >= ${self.cost_limit:.2f}")


class Orchestrator:
    """Orchestrates the research and synthesis process."""
    
    def __init__(self, config: Config):
        self.config = config
        self.agents = create_agents(config.intensity)
        self.dashboard = Dashboard() if config.show_dashboard else None
        self.token_tracker = TokenTracker(config.token_limit, config.cost_limit)
        self.claude_client = None  # Would initialize Anthropic client here
        
    def execute(self):
        """Execute the research and synthesis process."""
        start_time = time.time()
        
        try:
            # Update progress
            self._update_progress("research", 0, "Starting research...")
            
            # Phase 1: Research
            research_results = self._conduct_research()
            
            # Phase 2: Synthesis
            self._update_progress("synthesis", 50, "Synthesizing research...")
            essay = self._synthesize_results(research_results)
            
            # Phase 3: Format and save
            self._update_progress("formatting", 90, "Formatting output...")
            self._save_essay(essay)
            
            # Complete
            self._update_progress("complete", 100, "Essay generation complete!")
            
            # Open file if requested
            if self.config.auto_open:
                self._open_file()
                
            # Print summary
            self._print_summary(essay, time.time() - start_time)
            
        except Exception as e:
            print(f"\nError: {e}")
            raise
            
    def _conduct_research(self) -> List[ResearchResult]:
        """Conduct parallel research using agents."""
        results = []
        
        if self.config.demo_mode:
            # Return demo results
            for agent in self.agents:
                results.append(ResearchResult(
                    agent_id=agent.type.value,
                    agent_type=agent.type.value,
                    content=f"Demo content for {agent.description}",
                    score=0.8,
                    quality_score=0.8
                ))
            return results
        
        # Real implementation would use ThreadPoolExecutor or asyncio
        # to run agents in parallel with the Claude API
        # For now, return placeholder
        print(f"\nDeploying {len(self.agents)} research agents...")
        
        with ThreadPoolExecutor(max_workers=self.config.parallelism) as executor:
            # Submit research tasks
            futures = []
            for agent in self.agents:
                future = executor.submit(self._run_agent, agent)
                futures.append(future)
            
            # Collect results
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    self._update_progress(
                        "research", 
                        len(results) / len(self.agents) * 50,
                        f"Completed {len(results)}/{len(self.agents)} agents"
                    )
                except Exception as e:
                    print(f"Agent failed: {e}")
                    
        return results
    
    def _run_agent(self, agent) -> ResearchResult:
        """Run a single agent (placeholder)."""
        # In real implementation, this would call Claude API
        prompt = agent.generate_prompt(self.config.topic)
        
        # Simulate some work
        time.sleep(0.5)
        
        return ResearchResult(
            agent_id=agent.type.value,
            agent_type=agent.type.value,
            content=f"Research content for {agent.description} on {self.config.topic}",
            score=0.85,
            quality_score=0.85,
            tokens_used=TokenUsage(
                prompt_tokens=len(prompt.split()),
                completion_tokens=500,
                total_tokens=len(prompt.split()) + 500,
                model=self.config.claude_model,
                cost=0.01
            )
        )
    
    def _synthesize_results(self, results: List[ResearchResult]) -> Essay:
        """Synthesize research results into an essay."""
        synthesizer = Synthesizer()
        
        # In real implementation, this would use Claude to synthesize
        # For now, create a simple essay
        content = f"# Research Essay: {self.config.topic}\n\n"
        content += "## Introduction\n\n"
        content += f"This essay explores {self.config.topic} through multiple perspectives.\n\n"
        
        for result in results:
            content += f"## {result.agent_type.replace('-', ' ').title()}\n\n"
            content += f"{result.content}\n\n"
        
        content += "## Conclusion\n\n"
        content += "This comprehensive analysis provides insights into the topic.\n"
        
        # Create metadata
        metadata = Metadata(
            topic=self.config.topic,
            research_depth=f"{len(self.agents)} agents",
            agents_used=len(self.agents),
            total_variations=self.config.best_of_n,
            synthesis_method="parallel",
            generation_time=timedelta(seconds=60),
            total_tokens=self.token_tracker.total_tokens,
            estimated_cost=self.token_tracker.total_cost,
            quality_metrics=QualityMetrics(
                coherence=0.85,
                citation_quality=0.80,
                depth_score=0.90,
                originality=0.75,
                overall_score=0.83
            )
        )
        
        return Essay(
            title=f"Research Essay: {self.config.topic}",
            content=content,
            metadata=metadata,
            word_count=len(content.split())
        )
    
    def _save_essay(self, essay: Essay):
        """Save the essay to file."""
        formatter = Formatter()
        formatted_content = formatter.format(essay, self.config.output_format)
        
        with open(self.config.output_file, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
    
    def _open_file(self):
        """Open the generated file."""
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', self.config.output_file])
            elif platform.system() == 'Windows':
                os.startfile(self.config.output_file)
            else:  # Linux
                subprocess.run(['xdg-open', self.config.output_file])
        except Exception as e:
            print(f"Could not open file automatically: {e}")
    
    def _update_progress(self, stage: str, percentage: float, message: str):
        """Update progress display."""
        if self.dashboard:
            progress = Progress(
                stage=stage,
                percentage=percentage,
                active_agents=len(self.agents),
                completed_agents=int(percentage / 50 * len(self.agents)),
                tokens_used=self.token_tracker.total_tokens,
                estimated_cost=self.token_tracker.total_cost,
                message=message
            )
            self.dashboard.update(progress)
        else:
            print(f"[{percentage:3.0f}%] {message}")
    
    def _print_summary(self, essay: Essay, duration: float):
        """Print generation summary."""
        print("\n" + "="*60)
        print("ESSAY GENERATION COMPLETE")
        print("="*60)
        print(f"Topic: {self.config.topic}")
        print(f"Output: {self.config.output_file}")
        print(f"Word Count: {essay.word_count:,}")
        print(f"Agents Used: {len(self.agents)}")
        print(f"Generation Time: {duration:.1f}s")
        if not self.config.demo_mode:
            print(f"Tokens Used: {self.token_tracker.total_tokens:,}")
            print(f"Estimated Cost: ${self.token_tracker.total_cost:.2f}")
        print("="*60)