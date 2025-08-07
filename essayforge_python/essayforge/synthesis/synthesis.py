"""Synthesis module for combining research results into essays."""

from typing import List

from ..models import ResearchResult, Essay


class Synthesizer:
    """Synthesizes research results into a coherent essay."""
    
    def __init__(self):
        self.synthesis_prompt_template = """
You are an expert research synthesizer. Your task is to combine multiple research perspectives into a coherent, well-structured essay.

Topic: {topic}

Research Results:
{research_content}

Requirements:
1. Create a comprehensive essay that integrates all research perspectives
2. Ensure logical flow and smooth transitions between sections
3. Maintain academic rigor while being accessible
4. Include proper citations and references
5. Provide balanced coverage of all aspects
6. Draw insightful conclusions from the combined research

Structure the essay with:
- Engaging introduction
- Well-organized body sections
- Thoughtful conclusion
- Proper citations throughout
"""
    
    def synthesize(self, topic: str, results: List[ResearchResult]) -> str:
        """Synthesize research results into essay content."""
        # In a real implementation, this would use Claude API
        # For now, return a placeholder
        
        research_content = self._format_research_results(results)
        prompt = self.synthesis_prompt_template.format(
            topic=topic,
            research_content=research_content
        )
        
        # Placeholder synthesis
        return self._create_placeholder_essay(topic, results)
    
    def _format_research_results(self, results: List[ResearchResult]) -> str:
        """Format research results for the synthesis prompt."""
        formatted = []
        for result in results:
            formatted.append(f"### {result.agent_type}\n{result.content}\n")
        return "\n".join(formatted)
    
    def _create_placeholder_essay(self, topic: str, results: List[ResearchResult]) -> str:
        """Create a placeholder essay structure."""
        essay = f"# {topic}\n\n"
        essay += "## Abstract\n\n"
        essay += f"This comprehensive analysis examines {topic} from multiple perspectives, "
        essay += "integrating findings from specialized research agents to provide "
        essay += "a thorough understanding of the subject.\n\n"
        
        essay += "## Introduction\n\n"
        essay += f"The topic of {topic} represents a significant area of study that "
        essay += "warrants careful examination from various angles. This essay synthesizes "
        essay += "research from multiple specialized perspectives to provide a comprehensive "
        essay += "understanding of the subject matter.\n\n"
        
        # Add sections from research results
        for i, result in enumerate(results, 1):
            section_title = result.agent_type.replace('-', ' ').title()
            essay += f"## {section_title}\n\n"
            essay += f"{result.content}\n\n"
        
        essay += "## Synthesis and Analysis\n\n"
        essay += "The diverse perspectives presented above reveal the multifaceted nature "
        essay += f"of {topic}. By integrating these various viewpoints, we can develop "
        essay += "a more nuanced understanding of the subject.\n\n"
        
        essay += "## Conclusion\n\n"
        essay += f"This comprehensive examination of {topic} demonstrates the importance "
        essay += "of approaching complex topics from multiple angles. The synthesis of "
        essay += "these perspectives provides valuable insights that would not be apparent "
        essay += "from any single viewpoint alone.\n\n"
        
        essay += "## References\n\n"
        essay += "[References would be listed here]\n"
        
        return essay