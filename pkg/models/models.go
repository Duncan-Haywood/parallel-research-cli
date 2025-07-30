package models

import (
	"time"
)

// ResearchResult represents the output from a single research agent
type ResearchResult struct {
	AgentID      string
	AgentType    string
	Content      string
	Citations    []Citation
	TokensUsed   TokenUsage
	Timestamp    time.Time
	Score        float64 // For best-of-n selection
	QualityScore float64 // 0-1 quality metric
}

// Essay represents the final synthesized essay
type Essay struct {
	Title       string
	Content     string
	Citations   []Citation
	Metadata    Metadata
	GeneratedAt time.Time
	WordCount   int
}

// Citation represents a reference or source
type Citation struct {
	ID         string
	Type       string // article, book, web, video, etc.
	Title      string
	Source     string
	URL        string
	Authors    []string
	Date       string
	AccessDate time.Time
	Quote      string // Relevant quote from the source
}

// Metadata contains additional information about the essay
type Metadata struct {
	Topic           string
	ResearchDepth   string
	AgentsUsed      int
	TotalVariations int
	SynthesisMethod string
	GenerationTime  time.Duration
	TotalTokens     int
	EstimatedCost   float64
	QualityMetrics  QualityMetrics
}

// QualityMetrics tracks various quality indicators
type QualityMetrics struct {
	Coherence       float64 // 0-1 score
	CitationQuality float64 // 0-1 score
	DepthScore      float64 // 0-1 score
	Originality     float64 // 0-1 score
	OverallScore    float64 // Weighted average
}

// TokenUsage tracks API token consumption
type TokenUsage struct {
	PromptTokens     int
	CompletionTokens int
	TotalTokens      int
	Model            string
	Cost             float64
}

// OutputFormat represents different export formats
type OutputFormat string

const (
	FormatMarkdown OutputFormat = "markdown"
	FormatLaTeX    OutputFormat = "latex"
	FormatDOCX     OutputFormat = "docx"
	FormatPDF      OutputFormat = "pdf"
	FormatHTML     OutputFormat = "html"
)

// Progress represents real-time progress information
type Progress struct {
	Stage           string  // research, synthesis, formatting
	Percentage      float64 // 0-100
	ActiveAgents    int
	CompletedAgents int
	TokensUsed      int
	EstimatedCost   float64
	Message         string
}