"""Research agents for EssayForge."""

from dataclasses import dataclass
from enum import Enum
from typing import List


class AgentType(Enum):
    """Types of research agents available."""
    FACT_GATHERER = "fact-gatherer"
    HISTORICAL_CONTEXT = "historical-context"
    CURRENT_STATE = "current-state"
    FUTURE_PROJECTIONS = "future-projections"
    COUNTER_ARGUMENTS = "counter-arguments"
    EXPERT_OPINIONS = "expert-opinions"
    CASE_STUDIES = "case-studies"
    DATA_ANALYSIS = "data-analysis"
    THEORETICAL_FRAMEWORK = "theoretical-framework"
    PRACTICAL_APPLICATIONS = "practical-applications"


@dataclass
class Agent:
    """Represents a research agent with its type and prompt template."""
    type: AgentType
    description: str
    prompt_template: str
    
    def generate_prompt(self, topic: str) -> str:
        """Generate a prompt for this agent with the given topic."""
        return self.prompt_template % topic


def create_agents(intensity: int) -> List[Agent]:
    """Create a list of agents based on the specified intensity level."""
    all_agents = [
        Agent(
            type=AgentType.FACT_GATHERER,
            description="Gathers core facts and verifiable information",
            prompt_template="""You are a fact-gathering research agent. Your task is to research "%s" and provide:
1. Key facts and statistics
2. Verified information from reliable sources
3. Important definitions and concepts
4. Quantitative data points

Focus on accuracy and cite all sources. Output in markdown with proper citations."""
        ),
        Agent(
            type=AgentType.CURRENT_STATE,
            description="Analyzes current state and recent developments",
            prompt_template="""You are a current affairs research agent. Research the current state of "%s" including:
1. Latest developments and news
2. Current trends and patterns
3. Recent changes or updates
4. Present-day relevance and impact

Provide timely, up-to-date information with sources. Output in markdown."""
        ),
        Agent(
            type=AgentType.EXPERT_OPINIONS,
            description="Collects expert opinions and authoritative perspectives",
            prompt_template="""You are an expert opinion researcher. For the topic "%s", gather:
1. Opinions from recognized experts in the field
2. Academic perspectives
3. Industry leader insights
4. Consensus views and debates

Quote experts directly when possible and cite sources. Output in markdown."""
        ),
        Agent(
            type=AgentType.HISTORICAL_CONTEXT,
            description="Provides historical background and evolution",
            prompt_template="""You are a historical research agent. Provide historical context for "%s" including:
1. Origins and historical development
2. Key milestones and turning points
3. Evolution over time
4. Historical precedents and patterns

Focus on how the past informs the present. Output in markdown with citations."""
        ),
        Agent(
            type=AgentType.COUNTER_ARGUMENTS,
            description="Explores opposing views and criticisms",
            prompt_template="""You are a critical analysis agent. For "%s", research:
1. Common criticisms and counter-arguments
2. Alternative perspectives
3. Potential weaknesses or limitations
4. Opposing viewpoints and their merits

Be balanced and fair in presenting different sides. Output in markdown."""
        ),
        Agent(
            type=AgentType.FUTURE_PROJECTIONS,
            description="Analyzes future trends and projections",
            prompt_template="""You are a future trends analyst. For "%s", research and analyze:
1. Future projections and forecasts
2. Emerging trends and possibilities
3. Potential scenarios and outcomes
4. Expert predictions

Base projections on current data and expert analysis. Output in markdown."""
        ),
        Agent(
            type=AgentType.CASE_STUDIES,
            description="Provides relevant case studies and examples",
            prompt_template="""You are a case study researcher. For "%s", provide:
1. Relevant case studies and real-world examples
2. Success stories and failures
3. Practical implementations
4. Lessons learned from specific cases

Focus on concrete examples with details. Output in markdown with sources."""
        ),
        Agent(
            type=AgentType.DATA_ANALYSIS,
            description="Performs data-driven analysis",
            prompt_template="""You are a data analysis agent. For "%s", provide:
1. Statistical analysis and data visualization descriptions
2. Quantitative trends and patterns
3. Data-driven insights
4. Comparative analysis with benchmarks

Focus on numbers and measurable outcomes. Output in markdown."""
        ),
        Agent(
            type=AgentType.THEORETICAL_FRAMEWORK,
            description="Explores theoretical foundations and frameworks",
            prompt_template="""You are a theoretical research agent. For "%s", explore:
1. Theoretical frameworks and models
2. Academic theories and concepts
3. Philosophical underpinnings
4. Conceptual relationships

Connect theory to practical understanding. Output in markdown."""
        ),
        Agent(
            type=AgentType.PRACTICAL_APPLICATIONS,
            description="Focuses on practical applications and implementations",
            prompt_template="""You are a practical applications researcher. For "%s", detail:
1. Real-world applications and uses
2. Implementation strategies
3. Best practices and guidelines
4. Practical considerations and challenges

Focus on actionable insights. Output in markdown."""
        ),
    ]
    
    if intensity <= 0:
        return all_agents[:2]  # Return a default minimum of 2 agents
    if intensity > len(all_agents):
        return all_agents
    return all_agents[:intensity]