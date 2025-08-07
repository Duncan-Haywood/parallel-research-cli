package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/duncan/essayforge/pkg/models"
	"github.com/duncan/essayforge/pkg/orchestrator"
	"github.com/spf13/cobra"
)

var (
	// Core options
	topic       string
	parallelism int
	bestOfN     int
	intensity   int

	// Output options
	outputFile   string
	outputFormat string

	// Feature flags
	demoMode      bool
	autoOpen      bool
	showDashboard bool
	dryRun        bool

	// Resource limits
	tokenLimit int
	costLimit  float64

	// Model selection
	claudeModel string
)

func main() {
	var rootCmd = &cobra.Command{
		Use:   "essayforge",
		Short: "Multi-agent collaborative synthesis for research excellence",
		Long: `An AI-powered research synthesis system implementing an Actor-Critic architecture inspired by 
reinforcement learning, where Creator agents (actors) and Evaluator agents (critics) collaborate 
through iterative refinement to produce publication-quality essays.

Features:
- Actor-critic dynamics with structured feedback for quality improvement.
- Iterative refinement with quality thresholds.
- Parallel execution with best-of-N selection.
- Multiple output formats (Markdown, LaTeX, HTML).
- Real-time progress and dialogue visualization.
- Token usage and cost tracking.`,
		Run: func(cmd *cobra.Command, args []string) {
			if topic == "" {
				fmt.Println("Error: topic is required")
				cmd.Help()
				os.Exit(1)
			}
			runResearch()
		},
	}

	// Core flags
	rootCmd.Flags().StringVarP(&topic, "topic", "t", "", "Research topic (required)")
	rootCmd.Flags().IntVarP(&intensity, "intensity", "i", 5, "Number of specialized research agents to deploy (1-10)")
	rootCmd.Flags().IntVarP(&parallelism, "parallel", "p", 3, "Number of parallel API calls per agent")
	rootCmd.Flags().IntVarP(&bestOfN, "best-of", "n", 1, "Number of variations to generate for best-of-n selection")

	// Output flags
	rootCmd.Flags().StringVarP(&outputFile, "output", "o", "essay.md", "Output file path")
	rootCmd.Flags().StringVarP(&outputFormat, "format", "f", "markdown", "Output format: markdown, latex, html")

	// Feature flags
	rootCmd.Flags().BoolVar(&demoMode, "demo", false, "Run in demo mode without Claude API calls")
	rootCmd.Flags().BoolVar(&autoOpen, "open", true, "Automatically open the essay when complete")
	rootCmd.Flags().BoolVar(&showDashboard, "dashboard", true, "Show real-time progress dashboard")
	rootCmd.Flags().BoolVar(&dryRun, "dry-run", false, "Preview cost estimate without running the generation")

	// Resource limit flags
	rootCmd.Flags().IntVar(&tokenLimit, "token-limit", 0, "Maximum tokens to use (0 = unlimited)")
	rootCmd.Flags().Float64Var(&costLimit, "cost-limit", 0, "Maximum cost in USD (0 = unlimited)")

	// Model selection
	rootCmd.Flags().StringVar(&claudeModel, "model", "claude-3-sonnet-20240229", "Claude model to use")

	// Mark required flags
	rootCmd.MarkFlagRequired("topic")

	// Add subcommands
	rootCmd.AddCommand(versionCmd())
	rootCmd.AddCommand(modelsCmd())
	rootCmd.AddCommand(estimateCmd())

	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

func runResearch() {
	if dryRun {
		fmt.Println("\n\033[33mThis is a dry run. No essay will be generated.\033[0m")
		fmt.Println("\033[90mRemove --dry-run to proceed with generation.\033[0m")
		os.Exit(0)
	}

	var format models.OutputFormat
	switch strings.ToLower(outputFormat) {
	case "markdown", "md":
		format = models.FormatMarkdown
	case "latex", "tex":
		format = models.FormatLaTeX
	case "html":
		format = models.FormatHTML
	default:
		fmt.Printf("Error: unsupported format '%s'. Use: markdown, latex, or html\n", outputFormat)
		os.Exit(1)
	}

	if !strings.Contains(outputFile, ".") {
		switch format {
		case models.FormatMarkdown:
			outputFile += ".md"
		case models.FormatLaTeX:
			outputFile += ".tex"
		case models.FormatHTML:
			outputFile += ".html"
		}
	}

	apiKey := os.Getenv("ANTHROPIC_API_KEY")
	if apiKey == "" && !demoMode {
		fmt.Println("Error: ANTHROPIC_API_KEY environment variable not set.")
		os.Exit(1)
	}

	config := orchestrator.Config{
		Topic:         topic,
		Intensity:     intensity,
		Parallelism:   parallelism,
		BestOfN:       bestOfN,
		OutputFile:    outputFile,
		DemoMode:      demoMode,
		AutoOpen:      autoOpen,
		APIKey:        apiKey,
		OutputFormat:  format,
		ShowDashboard: showDashboard,
		TokenLimit:    tokenLimit,
		CostLimit:     costLimit,
		ClaudeModel:   claudeModel,
	}

	orch, err := orchestrator.New(config)
	if err != nil {
		fmt.Printf("Error creating orchestrator: %v\n", err)
		os.Exit(1)
	}

	if err := orch.Execute(); err != nil {
		fmt.Printf("\nResearch failed: %v\n", err)
		os.Exit(1)
	}
}

func versionCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "version",
		Short: "Print version information",
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Println("EssayForge v3.0.0")
		},
	}
}

func modelsCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "models",
		Short: "List available Claude models",
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Println("Available Claude models:")
			fmt.Println("  - claude-3-opus-20240229     (Most capable, higher cost)")
			fmt.Println("  - claude-3-sonnet-20240229   (Balanced performance/cost) [default]")
			fmt.Println("  - claude-3-haiku-20240307    (Fastest, lowest cost)")
		},
	}
}

func estimateCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "estimate",
		Short: "Estimate costs for research paper generation (coming soon)",
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Println("Cost estimation is being updated for the new intensity-based system.")
		},
	}
}
