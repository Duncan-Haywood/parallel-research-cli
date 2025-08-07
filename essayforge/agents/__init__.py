"""Agent module for EssayForge."""

from .agents import Agent, AgentType, create_agents
from .advanced_agents import (
    AdvancedAgent,
    AdvancedAgentType,
    create_advanced_agents,
    get_agents_for_stage
)

__all__ = [
    'Agent',
    'AgentType',
    'create_agents',
    'AdvancedAgent',
    'AdvancedAgentType',
    'create_advanced_agents',
    'get_agents_for_stage'
]