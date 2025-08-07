"""Models for the EssayForge research synthesis system."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional
from enum import Enum


@dataclass
class Citation:
    """Represents a reference or source."""
    id: str
    type: str  # article, book, web, video, etc.
    title: str
    source: str
    url: str
    authors: List[str] = field(default_factory=list)
    date: str = ""
    access_date: datetime = field(default_factory=datetime.now)
    quote: str = ""  # Relevant quote from the source


@dataclass
class TokenUsage:
    """Tracks API token consumption."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    model: str = ""
    cost: float = 0.0


@dataclass
class ResearchResult:
    """Represents the output from a single research agent."""
    agent_id: str
    agent_type: str
    content: str
    citations: List[Citation] = field(default_factory=list)
    tokens_used: TokenUsage = field(default_factory=TokenUsage)
    timestamp: datetime = field(default_factory=datetime.now)
    score: float = 0.0  # For best-of-n selection
    quality_score: float = 0.0  # 0-1 quality metric


@dataclass
class QualityMetrics:
    """Tracks various quality indicators."""
    coherence: float = 0.0  # 0-1 score
    citation_quality: float = 0.0  # 0-1 score
    depth_score: float = 0.0  # 0-1 score
    originality: float = 0.0  # 0-1 score
    overall_score: float = 0.0  # Weighted average


@dataclass
class Metadata:
    """Contains additional information about the essay."""
    topic: str
    research_depth: str
    agents_used: int
    total_variations: int
    synthesis_method: str
    generation_time: timedelta
    total_tokens: int
    estimated_cost: float
    quality_metrics: QualityMetrics = field(default_factory=QualityMetrics)


@dataclass
class Essay:
    """Represents the final synthesized essay."""
    title: str
    content: str
    citations: List[Citation] = field(default_factory=list)
    metadata: Optional[Metadata] = None
    generated_at: datetime = field(default_factory=datetime.now)
    word_count: int = 0


class OutputFormat(Enum):
    """Represents different export formats."""
    MARKDOWN = "markdown"
    LATEX = "latex"
    DOCX = "docx"
    PDF = "pdf"
    HTML = "html"


@dataclass
class Progress:
    """Represents real-time progress information."""
    stage: str  # research, synthesis, formatting
    percentage: float = 0.0  # 0-100
    active_agents: int = 0
    completed_agents: int = 0
    tokens_used: int = 0
    estimated_cost: float = 0.0
    message: str = ""