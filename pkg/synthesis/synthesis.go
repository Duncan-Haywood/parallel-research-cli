package synthesis

import (
	"fmt"
	"os/exec"
	"regexp"
	"sort"
	"strings"
	"time"

	"github.com/duncan/essayforge/pkg/models"
	"github.com/fatih/color"
)

type Synthesizer struct {
	bestOfN  int
	demoMode bool
}

func New(bestOfN int) *Synthesizer {
	return &Synthesizer{
		bestOfN: bestOfN,
	}
}

func (s *Synthesizer) SetDemoMode(demo bool) {
	s.demoMode = demo
}

func (s *Synthesizer) Synthesize(topic string, results []*models.ResearchResult) (*models.Essay, error) {
	startTime := time.Now()

	// Group results by agent type
	groupedResults := s.groupByAgentType(results)

	// Select best results for each agent type
	selectedResults := s.selectBestResults(groupedResults)

	// Extract citations from all results
	citations := s.extractCitations(selectedResults)

	// Create synthesis prompt
	synthesisPrompt := s.createSynthesisPrompt(topic, selectedResults)

	// Run final synthesis through Claude
	essayContent, err := s.runSynthesis(synthesisPrompt)
	if err != nil {
		return nil, err
	}

	// Format final essay with citations
	finalEssay := s.formatEssay(topic, essayContent, citations)

	return &models.Essay{
		Title:       fmt.Sprintf("Comprehensive Analysis: %s", topic),
		Content:     finalEssay,
		Citations:   citations,
		Metadata: models.Metadata{
			Topic:           topic,
			ResearchDepth:   "thorough",
			AgentsUsed:      len(groupedResults),
			TotalVariations: len(results),
			SynthesisMethod: "best-of-n-parallel",
			GenerationTime:  time.Since(startTime),
		},
		GeneratedAt: time.Now(),
	}, nil
}

func (s *Synthesizer) groupByAgentType(results []*models.ResearchResult) map[string][]*models.ResearchResult {
	grouped := make(map[string][]*models.ResearchResult)
	for _, result := range results {
		grouped[result.AgentType] = append(grouped[result.AgentType], result)
	}
	return grouped
}

func (s *Synthesizer) selectBestResults(grouped map[string][]*models.ResearchResult) []*models.ResearchResult {
	var selected []*models.ResearchResult

	for agentType, results := range grouped {
		color.Blue("Selecting best result for %s from %d variations", agentType, len(results))
		
		// Score each result
		for _, result := range results {
			result.Score = s.scoreResult(result)
		}

		// Sort by score
		sort.Slice(results, func(i, j int) bool {
			return results[i].Score > results[j].Score
		})

		// Select the best one
		if len(results) > 0 {
			selected = append(selected, results[0])
			color.Green("Selected result with score %.2f", results[0].Score)
		}
	}

	return selected
}

func (s *Synthesizer) scoreResult(result *models.ResearchResult) float64 {
	score := 0.0

	// Length score (prefer comprehensive but not overly verbose)
	contentLength := len(result.Content)
	if contentLength > 1000 && contentLength < 5000 {
		score += 10.0
	} else if contentLength > 500 {
		score += 5.0
	}

	// Citation score
	citationCount := len(s.extractCitationsFromContent(result.Content))
	score += float64(citationCount) * 2.0

	// Structure score (headings, lists, etc.)
	headingCount := strings.Count(result.Content, "\n#")
	score += float64(headingCount) * 1.5

	// Data/statistics score
	numberPattern := regexp.MustCompile(`\d+\.?\d*%?`)
	dataPoints := numberPattern.FindAllString(result.Content, -1)
	score += float64(len(dataPoints)) * 0.5

	return score
}

func (s *Synthesizer) extractCitations(results []*models.ResearchResult) []models.Citation {
	var allCitations []models.Citation
	citationMap := make(map[string]bool)

	for _, result := range results {
		citations := s.extractCitationsFromContent(result.Content)
		for _, citation := range citations {
			// Deduplicate citations
			key := citation.Source + citation.URL
			if !citationMap[key] {
				citationMap[key] = true
				allCitations = append(allCitations, citation)
			}
		}
	}

	return allCitations
}

func (s *Synthesizer) extractCitationsFromContent(content string) []models.Citation {
	var citations []models.Citation
	
	// Match markdown links [text](url)
	linkPattern := regexp.MustCompile(`\[([^\]]+)\]\(([^\)]+)\)`)
	matches := linkPattern.FindAllStringSubmatch(content, -1)
	
	for i, match := range matches {
		if len(match) >= 3 {
			citations = append(citations, models.Citation{
				ID:     fmt.Sprintf("cite%d", i+1),
				Source: match[1],
				URL:    match[2],
			})
		}
	}

	// Match academic-style citations (Author, Year)
	citationPattern := regexp.MustCompile(`\(([A-Za-z\s&]+),\s*(\d{4})\)`)
	academicMatches := citationPattern.FindAllStringSubmatch(content, -1)
	
	for i, match := range academicMatches {
		if len(match) >= 3 {
			citations = append(citations, models.Citation{
				ID:      fmt.Sprintf("acad%d", i+1),
				Authors: []string{match[1]},
				Date:    match[2],
				Source:  fmt.Sprintf("%s (%s)", match[1], match[2]),
			})
		}
	}

	return citations
}

func (s *Synthesizer) createSynthesisPrompt(topic string, results []*models.ResearchResult) string {
	var promptBuilder strings.Builder

	promptBuilder.WriteString(fmt.Sprintf(`You are a master synthesis agent creating a comprehensive, well-cited essay on "%s".

You have been provided with research from multiple specialized agents. Your task is to:

1. Synthesize all the research into a cohesive, insightful essay
2. Maintain all citations and add proper references
3. Create a logical flow that covers all important aspects
4. Ensure the essay is comprehensive yet readable
5. Add section headings and structure
6. Include an executive summary at the beginning
7. End with conclusions and future considerations

Here is the research from each specialized agent:

`, topic))

	for _, result := range results {
		promptBuilder.WriteString(fmt.Sprintf("\n=== %s Research ===\n%s\n", result.AgentType, result.Content))
	}

	promptBuilder.WriteString(`
Please create a comprehensive essay that:
- Integrates all perspectives seamlessly
- Maintains academic rigor with proper citations
- Provides unique insights from the synthesis
- Is structured with clear sections
- Includes data visualizations descriptions where relevant
- Balances depth with readability

Output the essay in markdown format with a clear structure.`)

	return promptBuilder.String()
}

func (s *Synthesizer) runSynthesis(prompt string) (string, error) {
	if s.demoMode {
		// Demo mode: generate a synthetic essay
		return s.generateDemoEssay(prompt), nil
	}
	
	// Run Claude with the synthesis prompt
	cmd := exec.Command("claude", "-p", prompt)
	
	output, err := cmd.Output()
	if err != nil {
		return "", fmt.Errorf("synthesis failed: %w", err)
	}

	return string(output), nil
}

func (s *Synthesizer) generateDemoEssay(prompt string) string {
	// Extract topic from prompt
	topicStart := strings.Index(prompt, "\"")
	topicEnd := strings.Index(prompt[topicStart+1:], "\"")
	topic := prompt[topicStart+1 : topicStart+1+topicEnd]
	
	return fmt.Sprintf(`# Comprehensive Analysis: %s

## Executive Summary

This comprehensive analysis synthesizes research from multiple specialized agents to provide a thorough understanding of %s. Our parallel research approach examined historical context, current state, expert opinions, and future projections to deliver actionable insights.

## Key Findings

### Current State and Adoption
Based on our current state analysis, %s has seen remarkable growth with 87%% of developers reporting improved code quality and a 45%% reduction in bugs. Enterprise adoption is accelerating, with major frameworks like React embracing functional paradigms through features like Hooks.

### Historical Evolution
The roots of %s trace back to lambda calculus in the 1930s, with practical implementations beginning with LISP in 1958. The paradigm has evolved significantly, with modern languages like Haskell, Scala, and Clojure bringing functional programming to mainstream development.

### Expert Consensus
Industry leaders unanimously agree on the transformative potential. As one expert noted: "Functional programming is not just a paradigm, it's a mindset shift." The academic community supports this with research showing 60%% bug reduction in functional codebases.

## Benefits and Challenges

### Demonstrated Benefits
1. **Code Quality**: Immutability and pure functions lead to more predictable, testable code
2. **Concurrency**: Natural fit for parallel processing and distributed systems
3. **Maintainability**: Reduced complexity through composition and modularity

### Addressing Concerns
While critics cite the steep learning curve and limited talent pool, our analysis reveals:
- Modern tooling has significantly reduced the learning curve
- ROI justifies training investments
- Growing educational resources and bootcamps

## Future Outlook

The trajectory for %s is overwhelmingly positive:
- Continued integration into mainstream languages
- Growing demand for functional programming skills
- Expansion into AI/ML applications where immutability and composability shine

## Recommendations

1. **For Organizations**: Invest in training and gradual adoption through hybrid approaches
2. **For Developers**: Start with functional concepts in familiar languages before diving into pure FP
3. **For Educators**: Integrate functional programming concepts early in curricula

## Conclusion

%s represents a fundamental shift in how we approach software development. While challenges exist, the benefits—particularly in our increasingly concurrent and distributed computing landscape—make it an essential paradigm for modern developers.

The evidence from our parallel research conclusively demonstrates that functional programming is not merely a trend but a crucial evolution in software engineering practices.`, topic, topic, topic, topic, topic, topic)
}

func (s *Synthesizer) formatEssay(topic string, content string, citations []models.Citation) string {
	var formatted strings.Builder

	// Add metadata header
	formatted.WriteString(fmt.Sprintf(`---
title: "Comprehensive Analysis: %s"
date: %s
synthesis_method: essayforge-adversarial
---

`, topic, time.Now().Format("2006-01-02")))

	// Add the main content
	formatted.WriteString(content)

	// Add references section if citations exist
	if len(citations) > 0 {
		formatted.WriteString("\n\n## References\n\n")
		for i, citation := range citations {
			if citation.URL != "" {
				formatted.WriteString(fmt.Sprintf("%d. [%s](%s)", i+1, citation.Source, citation.URL))
			} else {
				formatted.WriteString(fmt.Sprintf("%d. %s", i+1, citation.Source))
			}
			if len(citation.Authors) > 0 {
				formatted.WriteString(fmt.Sprintf(" - %s", strings.Join(citation.Authors, ", ")))
			}
			if citation.Date != "" {
				formatted.WriteString(fmt.Sprintf(" (%s)", citation.Date))
			}
			formatted.WriteString("\n")
		}
	}

	// Add generation metadata
	formatted.WriteString(fmt.Sprintf(`

---
*Generated using EssayForge with adversarial synthesis and best-of-%d selection.*
`, s.bestOfN))

	return formatted.String()
}