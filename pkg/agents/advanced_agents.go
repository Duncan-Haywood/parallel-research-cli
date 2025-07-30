package agents

import "fmt"

// AdvancedAgentType represents sophisticated research agent types
type AdvancedAgentType string

const (
	// Deep Analysis Agents (Stage 2 - Parallel)
	MethodologyAnalyst    AdvancedAgentType = "methodology-analyst"
	LimitationsExplorer   AdvancedAgentType = "limitations-explorer"
	ImplicationsAnalyst   AdvancedAgentType = "implications-analyst"
	TheoreticalFrameworkAdv  AdvancedAgentType = "theoretical-framework"
	EmpiricalValidator    AdvancedAgentType = "empirical-validator"
	ComparativeAnalyst    AdvancedAgentType = "comparative-analyst"
	
	// Verification Agents (Stage 3 - Parallel)
	FactChecker          AdvancedAgentType = "fact-checker"
	CitationVerifier     AdvancedAgentType = "citation-verifier"
	LogicValidator       AdvancedAgentType = "logic-validator"
	BiasDetector         AdvancedAgentType = "bias-detector"
	
	// Synthesis Agents (Stage 4 - Sequential)
	StructureArchitect   AdvancedAgentType = "structure-architect"
	ArgumentBuilder      AdvancedAgentType = "argument-builder"
	TransitionCrafter    AdvancedAgentType = "transition-crafter"
	AbstractGenerator    AdvancedAgentType = "abstract-generator"
	
	// Review Agents (Stage 5 - Parallel)
	PeerReviewer1        AdvancedAgentType = "peer-reviewer-1"
	PeerReviewer2        AdvancedAgentType = "peer-reviewer-2"
	PeerReviewer3        AdvancedAgentType = "peer-reviewer-3"
	EditorInChief        AdvancedAgentType = "editor-in-chief"
	
	// Refinement Agents (Stage 6 - Sequential)
	ClarityEnhancer      AdvancedAgentType = "clarity-enhancer"
	TechnicalAccuracy    AdvancedAgentType = "technical-accuracy"
	StyleConsistency     AdvancedAgentType = "style-consistency"
	FinalPolisher        AdvancedAgentType = "final-polisher"
)

// AdvancedAgent represents a sophisticated research agent
type AdvancedAgent struct {
	Type        AdvancedAgentType
	Stage       int
	Parallel    bool
	Description string
	PromptFunc  func(topic string, context map[string]interface{}) string
}

// CreateAdvancedAgents returns all advanced agent configurations
func CreateAdvancedAgents() map[int][]AdvancedAgent {
	stages := make(map[int][]AdvancedAgent)
	
	// Stage 1: Primary Research (Parallel)
	stages[1] = []AdvancedAgent{
		{
			Type:     AdvancedAgentType(FactGatherer),
			Stage:    1,
			Parallel: true,
			Description: "Gathers verified facts, statistics, and empirical data",
			PromptFunc: func(topic string, _ map[string]interface{}) string {
				return fmt.Sprintf(`As a meticulous fact-gathering researcher, conduct an exhaustive search for verified facts, statistics, and empirical data about %s.

Requirements:
1. Focus on peer-reviewed sources, government data, and reputable institutions
2. Include specific numbers, percentages, and measurable outcomes
3. Verify each fact with at least two independent sources
4. Note any conflicting data and explain discrepancies
5. Prioritize recent data (2020-2024) but include historical benchmarks
6. Format each fact with clear source attribution

For each fact, provide:
- The specific claim or statistic
- Primary source with full citation
- Secondary verification source
- Confidence level (high/medium/low)
- Any important caveats or limitations

Aim for depth over breadth. Quality and verifiability are paramount.`, topic)
			},
		},
		// Add all other Stage 1 agents...
	}
	
	// Stage 2: Deep Analysis (Parallel)
	stages[2] = []AdvancedAgent{
		{
			Type:     MethodologyAnalyst,
			Stage:    2,
			Parallel: true,
			Description: "Analyzes research methodologies and approaches",
			PromptFunc: func(topic string, context map[string]interface{}) string {
				research := context["stage1_research"].(string)
				return fmt.Sprintf(`As a methodology expert, analyze the research methods and approaches used in studying %s.

Based on this research data:
%s

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

Cite specific studies as examples and evaluate their methodological rigor.`, topic, research)
			},
		},
		{
			Type:     LimitationsExplorer,
			Stage:    2,
			Parallel: true,
			Description: "Identifies limitations, gaps, and constraints",
			PromptFunc: func(topic string, context map[string]interface{}) string {
				research := context["stage1_research"].(string)
				return fmt.Sprintf(`As a critical analyst, identify and explore the limitations, gaps, and constraints in the current understanding of %s.

Based on this research:
%s

Conduct a thorough limitations analysis:

1. **Knowledge Gaps**
   - What remains unknown or poorly understood?
   - Areas lacking sufficient research
   - Unanswered questions

2. **Methodological Limitations**
   - Constraints of current research methods
   - Sampling limitations
   - Measurement challenges

3. **Theoretical Limitations**
   - Shortcomings of existing frameworks
   - Assumptions that may not hold
   - Need for new theoretical approaches

4. **Practical Constraints**
   - Implementation challenges
   - Resource limitations
   - Scalability issues

5. **Contextual Limitations**
   - Geographic or cultural constraints
   - Temporal limitations
   - Domain-specific boundaries

6. **Ethical and Social Limitations**
   - Ethical constraints on research
   - Social acceptance barriers
   - Policy limitations

Be specific and cite examples. This analysis will inform future research directions.`, topic, research)
			},
		},
		// Add more Stage 2 agents...
	}
	
	// Stage 3: Verification (Parallel)
	stages[3] = []AdvancedAgent{
		{
			Type:     FactChecker,
			Stage:    3,
			Parallel: true,
			Description: "Verifies facts and claims for accuracy",
			PromptFunc: func(topic string, context map[string]interface{}) string {
				allContent := context["all_content"].(string)
				return fmt.Sprintf(`As a professional fact-checker, rigorously verify all claims and facts about %s.

Content to verify:
%s

For each claim or fact:

1. **Verification Status**
   - ✓ Verified: Multiple reputable sources confirm
   - ⚠ Partially verified: Some support but caveats exist
   - ✗ Unverified: Cannot find reliable confirmation
   - ❌ False: Evidence contradicts the claim

2. **Source Quality Assessment**
   - Primary source credibility
   - Potential biases
   - Peer review status
   - Institutional backing

3. **Cross-Reference Check**
   - Compare with authoritative sources
   - Check for consensus in the field
   - Note any significant disagreements

4. **Context Verification**
   - Is the context accurately represented?
   - Are there missing qualifiers?
   - Is the scope properly defined?

5. **Currency Check**
   - Is the information still current?
   - Have there been recent updates?
   - Note any outdated claims

Provide a detailed fact-checking report with specific corrections needed.`, topic, allContent)
			},
		},
		{
			Type:     CitationVerifier,
			Stage:    3,
			Parallel: true,
			Description: "Verifies and enhances citations",
			PromptFunc: func(topic string, context map[string]interface{}) string {
				citations := context["citations"].(string)
				return fmt.Sprintf(`As a citation specialist, verify and enhance all citations related to %s.

Current citations:
%s

For each citation:

1. **Verification**
   - Confirm the source exists
   - Verify author names and credentials
   - Check publication dates
   - Validate URLs/DOIs

2. **Completeness**
   - Add missing information
   - Include page numbers for quotes
   - Add DOIs where available
   - Include access dates for web sources

3. **Quality Assessment**
   - Rate source credibility (1-10)
   - Note if peer-reviewed
   - Identify potential biases
   - Flag predatory journals

4. **Cross-References**
   - Find related citations
   - Identify seminal papers
   - Note citation networks

5. **Format Standardization**
   - Ensure consistent formatting
   - Apply academic standards (APA/MLA/Chicago)
   - Create proper bibliography entries

Provide enhanced citations with quality ratings and recommendations for additional sources.`, topic, citations)
			},
		},
	}
	
	// Stage 4: Synthesis (Sequential)
	stages[4] = []AdvancedAgent{
		{
			Type:     StructureArchitect,
			Stage:    4,
			Parallel: false,
			Description: "Designs optimal paper structure",
			PromptFunc: func(topic string, context map[string]interface{}) string {
				allResearch := context["verified_research"].(string)
				return fmt.Sprintf(`As a research paper architect, design the optimal structure for a comprehensive paper on %s.

Based on all research:
%s

Create a detailed structural blueprint:

1. **Paper Architecture**
   - Title: Compelling and descriptive
   - Abstract structure (150-250 words)
   - Section hierarchy with word targets
   - Logical flow between sections

2. **Introduction Design** (10-15%% of paper)
   - Hook/Opening statement
   - Background context
   - Problem statement
   - Research questions/hypotheses
   - Paper roadmap

3. **Literature Review Structure** (20-25%%)
   - Thematic organization
   - Chronological elements
   - Theoretical frameworks
   - Gap identification

4. **Methodology Section** (15-20%%)
   - Research design
   - Data collection
   - Analysis methods
   - Limitations

5. **Results/Findings** (20-25%%)
   - Primary findings
   - Supporting evidence
   - Data presentation
   - Statistical analysis

6. **Discussion Structure** (20-25%%)
   - Interpretation of findings
   - Theoretical implications
   - Practical applications
   - Limitations acknowledgment

7. **Conclusion Design** (5-10%%)
   - Summary of contributions
   - Future research
   - Final thoughts

Include specific content allocation and transition strategies.`, topic, allResearch)
			},
		},
		{
			Type:     ArgumentBuilder,
			Stage:    4,
			Parallel: false,
			Description: "Constructs logical arguments and thesis",
			PromptFunc: func(topic string, context map[string]interface{}) string {
				structure := context["structure"].(string)
				research := context["verified_research"].(string)
				return fmt.Sprintf(`As an expert in argumentation, build a compelling thesis and supporting arguments for %s.

Paper structure:
%s

Research base:
%s

Construct:

1. **Central Thesis**
   - Clear, debatable claim
   - Scope and boundaries
   - Significance statement

2. **Primary Arguments** (3-5 main points)
   - Claim statement
   - Evidence compilation
   - Logical reasoning
   - Counter-argument acknowledgment

3. **Supporting Arguments**
   - Sub-claims for each primary argument
   - Evidence hierarchy
   - Logical connectors

4. **Evidence Integration**
   - Statistical support
   - Expert testimony
   - Case examples
   - Theoretical backing

5. **Argument Flow**
   - Progression from simple to complex
   - Building momentum
   - Climactic ordering

6. **Rhetorical Strategies**
   - Ethos establishment
   - Logos development
   - Appropriate pathos

Create a detailed argument map with evidence assignments.`, topic, structure, research)
			},
		},
	}
	
	// Stage 5: Peer Review (Parallel)
	stages[5] = []AdvancedAgent{
		{
			Type:     PeerReviewer1,
			Stage:    5,
			Parallel: true,
			Description: "Senior researcher perspective review",
			PromptFunc: func(topic string, context map[string]interface{}) string {
				draft := context["complete_draft"].(string)
				return fmt.Sprintf(`As a senior researcher with 20+ years experience in fields related to %s, provide a thorough peer review.

Manuscript:
%s

Review Guidelines:

1. **Contribution Assessment**
   - Novelty of insights
   - Significance to the field
   - Theoretical advancement
   - Practical value

2. **Methodological Rigor**
   - Appropriateness of methods
   - Data quality
   - Analysis validity
   - Limitations acknowledgment

3. **Literature Integration**
   - Comprehensiveness
   - Currency of sources
   - Fair representation
   - Missing key works

4. **Argumentation Quality**
   - Logical coherence
   - Evidence strength
   - Counter-argument handling
   - Conclusion validity

5. **Technical Accuracy**
   - Factual correctness
   - Statistical validity
   - Terminology usage
   - Citation accuracy

6. **Recommendations**
   - Major revisions needed
   - Minor corrections
   - Strengths to preserve
   - Publication readiness

Provide specific, actionable feedback with examples.`, topic, draft)
			},
		},
		// Add more peer reviewers with different perspectives...
	}
	
	// Stage 6: Refinement (Sequential)
	stages[6] = []AdvancedAgent{
		{
			Type:     ClarityEnhancer,
			Stage:    6,
			Parallel: false,
			Description: "Enhances clarity and readability",
			PromptFunc: func(topic string, context map[string]interface{}) string {
				reviewedDraft := context["reviewed_draft"].(string)
				feedback := context["peer_feedback"].(string)
				return fmt.Sprintf(`As a clarity specialist, enhance the readability and comprehension of this paper on %s.

Current draft:
%s

Peer feedback:
%s

Enhancement tasks:

1. **Sentence Clarity**
   - Simplify complex sentences
   - Remove ambiguity
   - Active voice preference
   - Precise word choice

2. **Paragraph Structure**
   - Clear topic sentences
   - Logical flow
   - Appropriate length
   - Smooth transitions

3. **Technical Communication**
   - Define jargon on first use
   - Consistent terminology
   - Clear explanations
   - Helpful analogies

4. **Visual Clarity**
   - Heading hierarchy
   - Bullet points where appropriate
   - White space usage
   - Emphasis techniques

5. **Reader Guidance**
   - Signposting phrases
   - Preview statements
   - Summary points
   - Clear conclusions

Maintain academic rigor while maximizing accessibility.`, topic, reviewedDraft, feedback)
			},
		},
		{
			Type:     FinalPolisher,
			Stage:    6,
			Parallel: false,
			Description: "Final polish and quality assurance",
			PromptFunc: func(topic string, context map[string]interface{}) string {
				finalDraft := context["clarity_enhanced"].(string)
				return fmt.Sprintf(`As the final editor, polish this research paper on %s to publication standards.

Near-final draft:
%s

Final polish checklist:

1. **Consistency Check**
   - Terminology consistency
   - Formatting uniformity
   - Citation style
   - Numbering systems

2. **Flow Optimization**
   - Sentence variety
   - Paragraph transitions
   - Section connections
   - Overall narrative arc

3. **Impact Enhancement**
   - Powerful opening
   - Memorable key points
   - Strong conclusion
   - Quotable insights

4. **Technical Perfection**
   - Grammar and punctuation
   - Spelling verification
   - Reference accuracy
   - Format compliance

5. **Final Touches**
   - Title optimization
   - Abstract refinement
   - Keyword selection
   - Acknowledgments

Ensure the paper meets the highest academic standards while maintaining engagement.`, topic, finalDraft)
			},
		},
	}
	
	return stages
}

// GetStageAgents returns agents for a specific stage
func GetStageAgents(stage int) []AdvancedAgent {
	allStages := CreateAdvancedAgents()
	return allStages[stage]
}

// GetTotalStages returns the total number of processing stages
func GetTotalStages() int {
	return 6
}