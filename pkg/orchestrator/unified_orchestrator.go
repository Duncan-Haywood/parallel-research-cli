package orchestrator

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"runtime"
	"strings"
	"sync"
	"time"

	"github.com/duncan/parallel-research-cli/pkg/agents"
	"github.com/duncan/parallel-research-cli/pkg/models"
	"github.com/duncan/parallel-research-cli/pkg/output"
	"github.com/duncan/parallel-research-cli/pkg/synthesis"
	"github.com/duncan/parallel-research-cli/pkg/ui"

	"github.com/dleviminzi/anthrogo"
	"github.com/fatih/color"
	"golang.org/x/sync/errgroup"
)

type Config struct {
	Topic         string
	Intensity     int
	Parallelism   int
	BestOfN       int
	OutputFile    string
	DemoMode      bool
	AutoOpen      bool
	APIKey        string
	OutputFormat  models.OutputFormat
	ShowDashboard bool
	TokenLimit    int
	CostLimit     float64
	ClaudeModel   string
}

type Orchestrator struct {
	config       Config
	claudeClient *anthrogo.Client
	agents       []agents.Agent
	dashboard    *ui.Dashboard
	tokenTracker *TokenTracker
	mu           sync.Mutex
}

func New(config Config) (*Orchestrator, error) {
	var client *anthrogo.Client
	var err error

	if !config.DemoMode {
		// Set the API key in environment variable for anthrogo
		if config.APIKey != "" {
			os.Setenv("ANTHROPIC_API_KEY", config.APIKey)
		}
		client, err = anthrogo.NewClient()
		if err != nil {
			return nil, fmt.Errorf("failed to create anthrogo client: %w", err)
		}
	}

	return &Orchestrator{
		config:       config,
		claudeClient: client,
		agents:       agents.CreateAgents(config.Intensity),
		dashboard:    ui.NewDashboard(),
		tokenTracker: &TokenTracker{
			agentTokens: make(map[string]int),
			tokenLimit:  config.TokenLimit,
			costLimit:   config.CostLimit,
		},
	}, nil
}
func (o *Orchestrator) Execute() error {
	color.Green("🚀 Starting research on: %s", o.config.Topic)
	if o.config.ShowDashboard {
		o.dashboard.Start()
		defer o.dashboard.Close()
	}
	researchResults, err := o.conductParallelResearch()
	if err != nil {
		return fmt.Errorf("research phase failed: %w", err)
	}
	essay, err := o.synthesizeResults(researchResults)
	if err != nil {
		return fmt.Errorf("synthesis phase failed: %w", err)
	}
	if err := o.writeOutput(essay); err != nil {
		return fmt.Errorf("output phase failed: %w", err)
	}
	color.Green("✅ Research complete! Essay saved to %s", o.config.OutputFile)
	if o.config.AutoOpen {
		if err := o.openFile(o.config.OutputFile); err != nil {
			color.Yellow("⚠️  Could not open file automatically: %v", err)
		}
	}
	return nil
}

func (o *Orchestrator) conductParallelResearch() ([]*models.ResearchResult, error) {
	ctx := context.Background()
	g, ctx := errgroup.WithContext(ctx)

	var results []*models.ResearchResult
	var mu sync.Mutex

	tempDir, err := os.MkdirTemp("", "parallel-research-*")
	if err != nil {
		return nil, err
	}
	defer os.RemoveAll(tempDir)

	totalAgents := len(o.agents) * o.config.BestOfN
	completed := 0

	for i, agent := range o.agents {
		for n := 0; n < o.config.BestOfN; n++ {
			agent := agent
			agentID := fmt.Sprintf("%s-%d-%d", agent.Type, i, n)

			g.Go(func() error {
				o.dashboard.UpdateAgent(agentID, string(agent.Type), "running", 0)

				if o.tokenTracker.exceedsLimits() {
					color.Red("⚠️  Token or cost limit reached, skipping agent %s", agentID)
					return nil
				}

				result, err := o.runAgent(ctx, agent, agentID, tempDir)
				if err != nil {
					o.dashboard.UpdateAgent(agentID, string(agent.Type), "failed", 0)
					color.Red("❌ Agent %s failed: %v", agentID, err)
					return nil
				}

				mu.Lock()
				results = append(results, result)
				completed++
				percentage := float64(completed)/float64(totalAgents)*60 + 10
				mu.Unlock()

				o.updateProgress(models.Progress{
					Stage:           "research",
					Percentage:      percentage,
					ActiveAgents:    totalAgents - completed,
					CompletedAgents: completed,
					TokensUsed:      o.tokenTracker.totalTokens,
					EstimatedCost:   o.tokenTracker.totalCost,
					Message:         fmt.Sprintf("Agent %s completed", agentID),
				})

				o.dashboard.UpdateAgent(agentID, string(agent.Type), "completed", result.TokensUsed.TotalTokens)

				return nil
			})
		}
	}

	if err := g.Wait(); err != nil {
		return nil, err
	}

	return results, nil
}

func (o *Orchestrator) runAgent(ctx context.Context, agent agents.Agent, agentID string, tempDir string) (*models.ResearchResult, error) {
	if o.config.DemoMode {
		return o.runDemoAgent(agent, agentID)
	}
	return o.runClaudeAgent(ctx, agent, agentID)
}

func (o *Orchestrator) runDemoAgent(agent agents.Agent, agentID string) (*models.ResearchResult, error) {
	content := o.generateDemoResponse(string(agent.Type), o.config.Topic)
	tokensUsed := models.TokenUsage{
		PromptTokens:     150,
		CompletionTokens: 800,
		TotalTokens:      950,
		Model:            "demo",
		Cost:             0.05,
	}
	time.Sleep(time.Duration(500+time.Now().UnixNano()%1500) * time.Millisecond)

	citations := o.extractCitations(content)
	qualityScore := o.calculateQualityScore(content, citations)

	return &models.ResearchResult{
		AgentID:      agentID,
		AgentType:    string(agent.Type),
		Content:      content,
		Citations:    citations,
		TokensUsed:   tokensUsed,
		Timestamp:    time.Now(),
		Score:        qualityScore,
		QualityScore: qualityScore,
	}, nil
}

func (o *Orchestrator) getModel(modelString string) (anthrogo.AnthropicModel, error) {
	switch modelString {
	case "claude-3-opus-20240229":
		return anthrogo.ModelClaude3Opus, nil
	case "claude-3-sonnet-20240229":
		return anthrogo.ModelClaude3Sonnet, nil
	case "claude-3-haiku-20240307":
		return anthrogo.ModelClaude3Haiku, nil
	default:
		return "", fmt.Errorf("unknown model: %s", modelString)
	}
}

func (o *Orchestrator) runClaudeAgent(ctx context.Context, agent agents.Agent, agentID string) (*models.ResearchResult, error) {
	prompt := agent.GeneratePrompt(o.config.Topic)
	enhancedPrompt := fmt.Sprintf(`%s

Please ensure your response includes:
1. Specific facts and data with sources
2. Expert opinions with attribution
3. Recent developments (2023-2024)
4. Cite all sources in the format: [Source: Title, Author/Organization, Date, URL if available]

Focus on accuracy and verifiability.`, prompt)

	model, err := o.getModel(o.config.ClaudeModel)
	if err != nil {
		return nil, err
	}

	resp, err := o.claudeClient.MessageRequest(ctx, anthrogo.MessagePayload{
		Model: model,
		Messages: []anthrogo.Message{{
			Role: anthrogo.RoleTypeUser,
			Content: []anthrogo.MessageContent{{
				Type: anthrogo.ContentTypeText,
				Text: &enhancedPrompt,
			}},
		}},
		MaxTokens: 4000,
	})
	if err != nil {
		return nil, fmt.Errorf("claude message request failed: %w", err)
	}

	content := ""
	if len(resp.Content) > 0 {
		content = resp.Content[0].Text
	}

	tokensUsed := o.estimateTokenUsage(enhancedPrompt, content)
	o.tokenTracker.addUsage(agentID, tokensUsed)

	citations := o.extractCitations(content)
	qualityScore := o.calculateQualityScore(content, citations)

	return &models.ResearchResult{
		AgentID:      agentID,
		AgentType:    string(agent.Type),
		Content:      content,
		Citations:    citations,
		TokensUsed:   tokensUsed,
		Timestamp:    time.Now(),
		Score:        qualityScore,
		QualityScore: qualityScore,
	}, nil
}

func (o *Orchestrator) synthesizeResults(results []*models.ResearchResult) (*models.Essay, error) {
	color.Yellow("🔄 Synthesizing %d research results...", len(results))

	synthesizer := synthesis.New(o.config.BestOfN)
	if o.config.DemoMode {
		synthesizer.SetDemoMode(true)
	}

	essay, err := synthesizer.Synthesize(o.config.Topic, results)
	if err != nil {
		return nil, err
	}

	essay.Metadata.QualityMetrics = o.calculateEssayQuality(essay, results)

	return essay, nil
}

func (o *Orchestrator) writeOutput(essay *models.Essay) error {
	formatter, err := output.GetFormatter(o.config.OutputFormat)
	if err != nil {
		return err
	}

	content, err := formatter.Format(essay)
	if err != nil {
		return err
	}

	return os.WriteFile(o.config.OutputFile, content, 0644)
}

func (o *Orchestrator) openFile(filename string) error {
	var cmd *exec.Cmd
	switch runtime.GOOS {
	case "darwin":
		cmd = exec.Command("open", filename)
	case "linux":
		cmd = exec.Command("xdg-open", filename)
	case "windows":
		cmd = exec.Command("cmd", "/c", "start", filename)
	default:
		return fmt.Errorf("unsupported platform: %s", runtime.GOOS)
	}
	return cmd.Start()
}

func (o *Orchestrator) updateProgress(progress models.Progress) {
	if o.dashboard != nil {
		o.dashboard.UpdateProgress(progress)
	}
}

type TokenTracker struct {
	mu          sync.Mutex
	totalTokens int
	agentTokens map[string]int
	totalCost   float64
	tokenLimit  int
	costLimit   float64
}

func (tt *TokenTracker) addUsage(agentID string, usage models.TokenUsage) {
	tt.mu.Lock()
	defer tt.mu.Unlock()

	tt.totalTokens += usage.TotalTokens
	tt.agentTokens[agentID] = usage.TotalTokens
	tt.totalCost += usage.Cost
}

func (tt *TokenTracker) exceedsLimits() bool {
	tt.mu.Lock()
	defer tt.mu.Unlock()

	if tt.tokenLimit > 0 && tt.totalTokens >= tt.tokenLimit {
		return true
	}
	if tt.costLimit > 0 && tt.totalCost >= tt.costLimit {
		return true
	}
	return false
}

func (o *Orchestrator) extractCitations(content string) []models.Citation {
	var citations []models.Citation
	lines := strings.Split(content, "\n")
	for _, line := range lines {
		if strings.Contains(line, "[Source:") || strings.Contains(line, "[source:") {
			citation := o.parseCitation(line)
			if citation.Title != "" {
				citations = append(citations, citation)
			}
		}
	}
	return citations
}

func (o *Orchestrator) parseCitation(line string) models.Citation {
	start := strings.Index(line, "[Source:")
	if start == -1 {
		start = strings.Index(line, "[source:")
	}
	if start == -1 {
		return models.Citation{}
	}

	end := strings.Index(line[start:], "]")
	if end == -1 {
		return models.Citation{}
	}

	citationText := line[start+8 : start+end]
	parts := strings.Split(citationText, ",")

	citation := models.Citation{
		ID:         fmt.Sprintf("cite_%d", time.Now().UnixNano()),
		Type:       "web",
		AccessDate: time.Now(),
	}

	if len(parts) > 0 {
		citation.Title = strings.TrimSpace(parts[0])
	}
	if len(parts) > 1 {
		citation.Source = strings.TrimSpace(parts[1])
	}
	if len(parts) > 2 {
		citation.Date = strings.TrimSpace(parts[2])
	}
	if len(parts) > 3 {
		url := strings.TrimSpace(parts[3])
		if strings.HasPrefix(url, "http") {
			citation.URL = url
		}
	}

	return citation
}

func (o *Orchestrator) calculateQualityScore(content string, citations []models.Citation) float64 {
	score := 0.0

	wordCount := len(strings.Fields(content))
	if wordCount > 500 {
		score += 0.25
	} else {
		score += float64(wordCount) / 2000.0
	}

	citationCount := len(citations)
	if citationCount > 5 {
		score += 0.25
	} else {
		score += float64(citationCount) / 20.0
	}

	if strings.Contains(content, "##") || strings.Contains(content, "**") {
		score += 0.15
	}
	if strings.Contains(content, "\n\n") {
		score += 0.10
	}

	qualityIndicators := []string{
		"research", "study", "analysis", "data", "evidence",
		"expert", "according to", "found that", "indicates",
	}
	matches := 0
	contentLower := strings.ToLower(content)
	for _, indicator := range qualityIndicators {
		if strings.Contains(contentLower, indicator) {
			matches++
		}
	}
	score += float64(matches) / float64(len(qualityIndicators)) * 0.25

	return score
}
func (o *Orchestrator) calculateEssayQuality(essay *models.Essay, results []*models.ResearchResult) models.QualityMetrics {
	metrics := models.QualityMetrics{}
	if strings.Contains(essay.Content, "## ") && strings.Contains(essay.Content, "\n\n") {
		metrics.Coherence = 0.8
	} else {
		metrics.Coherence = 0.6
	}
	uniqueCitations := make(map[string]bool)
	for _, citation := range essay.Citations {
		uniqueCitations[citation.Title] = true
	}
	metrics.CitationQuality = float64(len(uniqueCitations)) / float64(len(results)*2)
	if metrics.CitationQuality > 1.0 {
		metrics.CitationQuality = 1.0
	}
	totalScore := 0.0
	for _, result := range results {
		totalScore += result.QualityScore
	}
	metrics.DepthScore = totalScore / float64(len(results))
	sourceTypes := make(map[string]bool)
	for _, result := range results {
		sourceTypes[result.AgentType] = true
	}
	metrics.Originality = float64(len(sourceTypes)) / float64(len(o.agents))
	metrics.OverallScore = (metrics.Coherence*0.25 +
		metrics.CitationQuality*0.35 +
		metrics.DepthScore*0.25 +
		metrics.Originality*0.15)
	return metrics
}

func (o *Orchestrator) estimateTokenUsage(prompt, response string) models.TokenUsage {
	promptTokens := len(prompt) / 4
	completionTokens := len(response) / 4
	costPerMillion := 15.0
	totalTokens := promptTokens + completionTokens
	cost := float64(totalTokens) / 1_000_000 * costPerMillion
	return models.TokenUsage{
		PromptTokens:     promptTokens,
		CompletionTokens: completionTokens,
		TotalTokens:      totalTokens,
		Model:            o.config.ClaudeModel,
		Cost:             cost,
	}
}

func (o *Orchestrator) generateDemoResponse(agentType, topic string) string {
	templates := map[string]string{
		"fact-gatherer":      "# Key Facts about %s\n\n## Statistics\n- 87%% of developers report improved code quality\n- 45%% reduction in bugs when using FP\n- 3x faster development cycles\n\n## Core Concepts\n1. Immutability\n2. Pure functions\n3. Higher-order functions\n\n[Source](https://example.com/fp-study)",
		"current-state":      "# Current State of %s\n\n## Latest Trends\n- Growing adoption in enterprise environments\n- Integration with modern frameworks\n- Increased tool support\n\n## Recent Developments\n- React Hooks embrace functional paradigm\n- Rust combines FP with systems programming\n- TypeScript adds better FP support\n\n[Industry Report 2024](https://example.com/report)",
		"expert-opinions":    "# Expert Perspectives on %s\n\n> \"Functional programming is not just a paradigm, it's a mindset shift\" - Jane Doe, Tech Lead\n\n> \"The benefits become clear once you embrace immutability\" - Dr. John Smith\n\n## Consensus Views\n- Improved code maintainability\n- Better testability\n- Enhanced parallelization\n\n[Expert Panel](https://example.com/panel)",
		"historical-context": "# Historical Development of %s\n\n## Origins\n- Lambda calculus (1930s)\n- LISP (1958)\n- ML family (1970s)\n\n## Evolution\n- Haskell standardization (1990)\n- Scala emergence (2003)\n- Mainstream adoption (2010s)\n\n[CS History](https://example.com/history)",
		"counter-arguments":  "# Criticisms of %s\n\n## Common Concerns\n- Steep learning curve\n- Performance overhead claims\n- Limited talent pool\n\n## Rebuttals\n- Modern compilers optimize well\n- Growing educational resources\n- ROI justifies training investment\n\n[Debate Analysis](https://example.com/debate)",
	}

	if template, ok := templates[agentType]; ok {
		return fmt.Sprintf(template, topic)
	}

	return fmt.Sprintf("# %s Research on %s\n\nComprehensive analysis from %s perspective.\n\n[Source](https://example.com)", agentType, topic, agentType)
}
