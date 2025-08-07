"""Advanced agent definitions for sophisticated research synthesis."""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Callable, Optional


class AdvancedAgentType(Enum):
    """Sophisticated research agent types."""
    # Deep Analysis Agents (Stage 2 - Parallel)
    METHODOLOGY_ANALYST = "methodology-analyst"
    LIMITATIONS_EXPLORER = "limitations-explorer"
    IMPLICATIONS_ANALYST = "implications-analyst"
    THEORETICAL_FRAMEWORK_ADV = "theoretical-framework"
    EMPIRICAL_VALIDATOR = "empirical-validator"
    COMPARATIVE_ANALYST = "comparative-analyst"
    
    # Verification Agents (Stage 3 - Parallel)
    FACT_CHECKER = "fact-checker"
    CITATION_VERIFIER = "citation-verifier"
    LOGIC_VALIDATOR = "logic-validator"
    BIAS_DETECTOR = "bias-detector"
    
    # Synthesis Agents (Stage 4 - Sequential)
    STRUCTURE_ARCHITECT = "structure-architect"
    ARGUMENT_BUILDER = "argument-builder"
    TRANSITION_CRAFTER = "transition-crafter"
    ABSTRACT_GENERATOR = "abstract-generator"
    
    # Review Agents (Stage 5 - Parallel)
    PEER_REVIEWER_1 = "peer-reviewer-1"
    PEER_REVIEWER_2 = "peer-reviewer-2"
    PEER_REVIEWER_3 = "peer-reviewer-3"
    EDITOR_IN_CHIEF = "editor-in-chief"
    
    # Refinement Agents (Stage 6 - Sequential)
    CLARITY_ENHANCER = "clarity-enhancer"
    TECHNICAL_ACCURACY = "technical-accuracy"
    STYLE_CONSISTENCY = "style-consistency"
    FINAL_POLISHER = "final-polisher"


@dataclass
class AdvancedAgent:
    """Sophisticated research agent configuration."""
    type: AdvancedAgentType
    stage: int
    parallel: bool
    description: str
    prompt_func: Callable[[str, Dict[str, Any]], str]


def create_advanced_agents() -> Dict[int, List[AdvancedAgent]]:
    """Create all advanced agent configurations organized by stage."""
    stages = {}
    
    # Stage 2: Deep Analysis (Parallel)
    stages[2] = [
        AdvancedAgent(
            type=AdvancedAgentType.METHODOLOGY_ANALYST,
            stage=2,
            parallel=True,
            description="Analyzes research methodologies and approaches",
            prompt_func=lambda topic, context: f"""As a methodology expert, analyze the research methods and approaches used in studying {topic}.

Based on this research data:
{context.get('stage1_research', '')}

Provide a comprehensive methodological analysis including:

1. **Dominant Research Paradigms**
   - Quantitative vs. Qualitative approaches
   - Experimental vs. Observational studies
   - Cross-sectional vs. Longitudinal designs

2. **Data Collection Methods**
   - Survey instruments and sampling techniques
   - Experimental protocols
   - Data sources and databases used

3. **Analytical Frameworks**
   - Statistical methods employed
   - Theoretical models applied
   - Computational approaches

4. **Methodological Strengths**
   - What methods work well for this topic?
   - Best practices identified

5. **Methodological Limitations**
   - Common biases or limitations
   - Gaps in current approaches
   - Suggested improvements

6. **Emerging Methodologies**
   - New techniques being developed
   - Interdisciplinary approaches

Cite specific studies as examples and evaluate their methodological rigor."""
        ),
        AdvancedAgent(
            type=AdvancedAgentType.LIMITATIONS_EXPLORER,
            stage=2,
            parallel=True,
            description="Identifies limitations, gaps, and constraints",
            prompt_func=lambda topic, context: f"""As a critical analyst, identify and explore the limitations, gaps, and constraints in the current understanding of {topic}.

Based on this research:
{context.get('stage1_research', '')}

Conduct a thorough limitations analysis:

1. **Knowledge Gaps**
   - What remains unknown or poorly understood?
   - Areas lacking sufficient research
   - Unanswered questions

2. **Methodological Limitations**
   - Common research design flaws
   - Measurement challenges
   - Sampling limitations

3. **Practical Constraints**
   - Real-world implementation barriers
   - Resource limitations
   - Scalability issues

4. **Theoretical Limitations**
   - Incomplete or conflicting theories
   - Assumptions that may not hold
   - Boundary conditions

5. **Data Limitations**
   - Data availability issues
   - Quality concerns
   - Temporal or geographic constraints

Be specific and cite examples. Suggest how future research might address these limitations."""
        ),
    ]
    
    # Stage 3: Verification (Parallel)
    stages[3] = [
        AdvancedAgent(
            type=AdvancedAgentType.FACT_CHECKER,
            stage=3,
            parallel=True,
            description="Verifies facts and claims for accuracy",
            prompt_func=lambda topic, context: f"""As a meticulous fact-checker, verify all claims and facts about {topic}.

Review this compiled research:
{context.get('compiled_research', '')}

For each major claim or fact:
1. Verify accuracy against multiple sources
2. Check for outdated information
3. Identify any contradictions
4. Rate confidence level (high/medium/low)
5. Note any caveats or qualifications needed

Output a fact-checking report with:
- Verified facts (with sources)
- Disputed or uncertain claims
- Corrections needed
- Confidence ratings"""
        ),
    ]
    
    # Stage 4: Synthesis (Sequential)
    stages[4] = [
        AdvancedAgent(
            type=AdvancedAgentType.STRUCTURE_ARCHITECT,
            stage=4,
            parallel=False,
            description="Designs the optimal essay structure",
            prompt_func=lambda topic, context: f"""As a structure architect, design the optimal organization for an essay on {topic}.

Based on all research and analysis:
{context.get('verified_research', '')}

Create a detailed structural blueprint:

1. **Essay Architecture**
   - Optimal flow of ideas
   - Section organization
   - Paragraph structure

2. **Argumentative Framework**
   - Main thesis statement
   - Supporting arguments hierarchy
   - Evidence placement

3. **Narrative Arc**
   - Introduction strategy
   - Development progression
   - Conclusion approach

4. **Integration Points**
   - Where to weave in different perspectives
   - Placement of case studies
   - Data visualization opportunities

Provide a detailed outline with rationale for each structural decision."""
        ),
    ]
    
    # Stage 5: Review (Parallel)
    stages[5] = [
        AdvancedAgent(
            type=AdvancedAgentType.PEER_REVIEWER_1,
            stage=5,
            parallel=True,
            description="Academic peer review focusing on content accuracy",
            prompt_func=lambda topic, context: f"""As an academic peer reviewer, critically evaluate this essay on {topic}.

Essay to review:
{context.get('draft_essay', '')}

Focus on:
1. Factual accuracy and citation quality
2. Logical coherence of arguments
3. Appropriate use of evidence
4. Academic rigor and standards
5. Originality and contribution

Provide specific feedback with:
- Strengths to preserve
- Weaknesses to address
- Specific revision suggestions
- Overall quality assessment"""
        ),
    ]
    
    # Stage 6: Refinement (Sequential)
    stages[6] = [
        AdvancedAgent(
            type=AdvancedAgentType.CLARITY_ENHANCER,
            stage=6,
            parallel=False,
            description="Enhances clarity and readability",
            prompt_func=lambda topic, context: f"""As a clarity specialist, enhance the readability of this essay on {topic}.

Current version:
{context.get('reviewed_essay', '')}

Improvements to make:
1. Simplify complex sentences without losing meaning
2. Clarify technical terms and jargon
3. Improve transitions between ideas
4. Enhance topic sentences
5. Ensure consistent terminology

Maintain academic tone while maximizing accessibility."""
        ),
    ]
    
    return stages


def get_agents_for_stage(stage: int) -> List[AdvancedAgent]:
    """Get all agents for a specific stage."""
    all_stages = create_advanced_agents()
    return all_stages.get(stage, [])