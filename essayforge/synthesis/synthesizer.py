"""Synthesizer for combining research results into cohesive essays."""

from typing import List, Optional
import anthropic

from ..models.models import Essay, ResearchResult, Citation, OutputFormat


class Synthesizer:
    """Synthesizes research results into a cohesive essay."""
    
    def __init__(self, claude_client: Optional[anthropic.Anthropic], model: str, demo_mode: bool = False):
        self.claude_client = claude_client
        self.model = model
        self.demo_mode = demo_mode
    
    async def synthesize(
        self,
        topic: str,
        research_results: List[ResearchResult],
        output_format: OutputFormat
    ) -> Essay:
        """Synthesize research results into an essay."""
        if self.demo_mode:
            return self._create_demo_essay(topic, research_results)
        
        # Combine all research content
        combined_research = self._combine_research(research_results)
        
        # Extract all citations
        all_citations = self._extract_citations(research_results)
        
        # Generate essay structure
        structure = await self._generate_structure(topic, combined_research)
        
        # Generate essay content
        content = await self._generate_content(topic, combined_research, structure)
        
        # Generate title
        title = await self._generate_title(topic, content)
        
        # Count words
        word_count = len(content.split())
        
        return Essay(
            title=title,
            content=content,
            citations=all_citations,
            word_count=word_count
        )
    
    def _combine_research(self, research_results: List[ResearchResult]) -> str:
        """Combine all research content into a single text."""
        sections = []
        
        for result in research_results:
            sections.append(f"## Research from {result.agent_type}\n\n{result.content}\n")
        
        return "\n".join(sections)
    
    def _extract_citations(self, research_results: List[ResearchResult]) -> List[Citation]:
        """Extract unique citations from all research results."""
        citations_dict = {}
        
        for result in research_results:
            for citation in result.citations:
                if citation.id not in citations_dict:
                    citations_dict[citation.id] = citation
        
        return list(citations_dict.values())
    
    async def _generate_structure(self, topic: str, research: str) -> str:
        """Generate the essay structure."""
        prompt = f"""Based on the following research about "{topic}", create a detailed essay structure.

Research:
{research[:8000]}  # Limit to avoid token limits

Create a comprehensive outline with:
1. Introduction with thesis statement
2. Main sections with subsections
3. Logical flow of arguments
4. Conclusion

Format as a hierarchical outline."""

        response = self.claude_client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    async def _generate_content(self, topic: str, research: str, structure: str) -> str:
        """Generate the essay content."""
        prompt = f"""Write a comprehensive, publication-quality essay about "{topic}" following this structure:

{structure}

Use this research data:
{research[:10000]}  # Limit to avoid token limits

Requirements:
1. Academic tone but accessible
2. Clear thesis and arguments
3. Smooth transitions
4. Evidence-based claims
5. Engaging introduction and strong conclusion
6. Approximately 2000-3000 words

Write the complete essay in markdown format."""

        response = self.claude_client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    async def _generate_title(self, topic: str, content: str) -> str:
        """Generate an appropriate title for the essay."""
        prompt = f"""Based on this essay about "{topic}", generate a compelling, academic title.

Essay beginning:
{content[:1000]}

The title should be:
1. Informative and specific
2. Academic in tone
3. Engaging
4. 5-12 words

Provide only the title, nothing else."""

        response = self.claude_client.messages.create(
            model=self.model,
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text.strip()
    
    def _create_demo_essay(self, topic: str, research_results: List[ResearchResult]) -> Essay:
        """Create a demo essay without API calls."""
        title = f"A Comprehensive Analysis of {topic}"
        
        content = f"""# {title}

## Introduction

This essay provides a comprehensive analysis of {topic}, synthesizing insights from {len(research_results)} different research perspectives. Through examining historical context, current developments, expert opinions, and future projections, we develop a nuanced understanding of this important subject.

## Historical Context

{topic} has evolved significantly over time. Early developments laid the groundwork for our current understanding, with key milestones marking important transitions in how we approach this subject.

## Current State

Today, {topic} represents a critical area of study and practice. Recent developments have highlighted both opportunities and challenges that shape the contemporary landscape.

### Key Trends

1. Increasing complexity and interconnectedness
2. Growing importance in various sectors
3. Evolving methodologies and approaches

## Expert Perspectives

Leading experts in the field offer diverse viewpoints on {topic}. While consensus exists on certain fundamental aspects, healthy debate continues around implementation strategies and future directions.

## Future Outlook

Looking ahead, {topic} is poised for continued evolution. Emerging trends suggest several possible trajectories, each with distinct implications for stakeholders.

## Conclusion

This analysis of {topic} reveals a complex landscape shaped by historical precedents, current innovations, and future possibilities. As we continue to deepen our understanding, it becomes clear that {topic} will remain a vital area of focus for researchers, practitioners, and policymakers alike.

## References

1. Smith, J. (2024). "Understanding {topic}: A Comprehensive Guide." Academic Press.
2. Johnson, M. (2023). "The Evolution of {topic}." Journal of Advanced Studies.
3. Williams, R. (2024). "Future Directions in {topic} Research." Innovation Quarterly.
"""
        
        # Extract citations from research results
        all_citations = []
        for result in research_results:
            all_citations.extend(result.citations)
        
        return Essay(
            title=title,
            content=content,
            citations=all_citations,
            word_count=len(content.split())
        )