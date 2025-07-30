package agents

import "fmt"

type AgentType string

const (
	FactGatherer          AgentType = "fact-gatherer"
	HistoricalContext     AgentType = "historical-context"
	CurrentState          AgentType = "current-state"
	FutureProjections     AgentType = "future-projections"
	CounterArguments      AgentType = "counter-arguments"
	ExpertOpinions        AgentType = "expert-opinions"
	CaseStudies           AgentType = "case-studies"
	DataAnalysis          AgentType = "data-analysis"
	TheoreticalFramework  AgentType = "theoretical-framework"
	PracticalApplications AgentType = "practical-applications"
)

type Agent struct {
	Type           AgentType
	Description    string
	PromptTemplate string
}

func CreateAgents(intensity int) []Agent {
	allAgents := []Agent{
		{
			Type:        FactGatherer,
			Description: "Gathers core facts and verifiable information",
			PromptTemplate: `You are a fact-gathering research agent. Your task is to research "%s" and provide:
1. Key facts and statistics
2. Verified information from reliable sources
3. Important definitions and concepts
4. Quantitative data points

Focus on accuracy and cite all sources. Output in markdown with proper citations.`,
		},
		{
			Type:        CurrentState,
			Description: "Analyzes current state and recent developments",
			PromptTemplate: `You are a current affairs research agent. Research the current state of "%s" including:
1. Latest developments and news
2. Current trends and patterns
3. Recent changes or updates
4. Present-day relevance and impact

Provide timely, up-to-date information with sources. Output in markdown.`,
		},
		{
			Type:        ExpertOpinions,
			Description: "Collects expert opinions and authoritative perspectives",
			PromptTemplate: `You are an expert opinion researcher. For the topic "%s", gather:
1. Opinions from recognized experts in the field
2. Academic perspectives
3. Industry leader insights
4. Consensus views and debates

Quote experts directly when possible and cite sources. Output in markdown.`,
		},
		{
			Type:        HistoricalContext,
			Description: "Provides historical background and evolution",
			PromptTemplate: `You are a historical research agent. Provide historical context for "%s" including:
1. Origins and historical development
2. Key milestones and turning points
3. Evolution over time
4. Historical precedents and patterns

Focus on how the past informs the present. Output in markdown with citations.`,
		},
		{
			Type:        CounterArguments,
			Description: "Explores opposing views and criticisms",
			PromptTemplate: `You are a critical analysis agent. For "%s", research:
1. Common criticisms and counter-arguments
2. Alternative perspectives
3. Potential weaknesses or limitations
4. Opposing viewpoints and their merits

Be balanced and fair in presenting different sides. Output in markdown.`,
		},
		{
			Type:        FutureProjections,
			Description: "Analyzes future trends and projections",
			PromptTemplate: `You are a future trends analyst. For "%s", research and analyze:
1. Future projections and forecasts
2. Emerging trends and possibilities
3. Potential scenarios and outcomes
4. Expert predictions

Base projections on current data and expert analysis. Output in markdown.`,
		},
		{
			Type:        CaseStudies,
			Description: "Provides relevant case studies and examples",
			PromptTemplate: `You are a case study researcher. For "%s", provide:
1. Relevant case studies and real-world examples
2. Success stories and failures
3. Practical implementations
4. Lessons learned from specific cases

Focus on concrete examples with details. Output in markdown with sources.`,
		},
		{
			Type:        DataAnalysis,
			Description: "Performs data-driven analysis",
			PromptTemplate: `You are a data analysis agent. For "%s", provide:
1. Statistical analysis and data visualization descriptions
2. Quantitative trends and patterns
3. Data-driven insights
4. Comparative analysis with benchmarks

Focus on numbers and measurable outcomes. Output in markdown.`,
		},
		{
			Type:        TheoreticalFramework,
			Description: "Explores theoretical foundations and frameworks",
			PromptTemplate: `You are a theoretical research agent. For "%s", explore:
1. Theoretical frameworks and models
2. Academic theories and concepts
3. Philosophical underpinnings
4. Conceptual relationships

Connect theory to practical understanding. Output in markdown.`,
		},
		{
			Type:        PracticalApplications,
			Description: "Focuses on practical applications and implementations",
			PromptTemplate: `You are a practical applications researcher. For "%s", detail:
1. Real-world applications and uses
2. Implementation strategies
3. Best practices and guidelines
4. Practical considerations and challenges

Focus on actionable insights. Output in markdown.`,
		},
	}

	if intensity <= 0 {
		return allAgents[:2] // Return a default minimum of 2 agents
	}
	if intensity > len(allAgents) {
		return allAgents
	}
	return allAgents[:intensity]
}

func (a Agent) GeneratePrompt(topic string) string {
	return fmt.Sprintf(a.PromptTemplate, topic)
}
