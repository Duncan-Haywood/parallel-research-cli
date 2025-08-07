# ResearchEssayForge

**Multi-agent collaborative synthesis for research excellence**

An AI-powered research synthesis system implementing an Actor-Critic architecture inspired by reinforcement learning, where Creator agents (actors) and Evaluator agents (critics) collaborate through iterative refinement to produce publication-quality essays. The system implements a multi-agent collaborative approach where specialized agents work together, with quality assessment driving continuous improvement through structured feedback loops.

## The Actor-Critic Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Input: Research Topic                 │
└────────────────────────┬────────────────────────────────┘
                         │
                         v
┌─────────────────────────────────────────────────────────┐
│                  ACTOR NETWORK (Creators)                │
│  ┌─────────────────────────────────────────────────┐   │
│  │ • Fact Synthesis Agent                          │   │
│  │ • Argument Construction Agent                   │   │
│  │ • Evidence Integration Agent                    │   │
│  │ • Narrative Flow Agent                          │   │
│  │ • Citation Management Agent                     │   │
│  └─────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────┘
                         │
                         v
                 [Draft Essay v1]
                         │
                         v
┌─────────────────────────────────────────────────────────┐
│                 CRITIC NETWORK (Evaluators)              │
│  ┌─────────────────────────────────────────────────┐   │
│  │ • Factual Accuracy Critic                       │   │
│  │ • Argument Coherence Critic                     │   │
│  │ • Citation Quality Critic                       │   │
│  │ • Structure & Flow Critic                       │   │
│  │ • Originality & Insight Critic                  │   │
│  └─────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────┘
                         │
                         v
              [Quality Score & Feedback]
                         │
                         v
        ┌────────────────┴────────────────┐
        │  Iterate until quality threshold │
        │    or maximum iterations met     │
        └────────────────┬────────────────┘
                         │
                         v
                [Final Essay Output]
```

## How It Works: The Collaborative Feedback Loop

1. **Topic Analysis**: The system analyzes the research topic and determines the required expertise
2. **Actor Phase**: Creator agents work in parallel to generate content from multiple perspectives
3. **Critic Phase**: Evaluator agents assess the output and provide structured feedback
4. **Refinement**: Actors incorporate feedback to improve the essay
5. **Iteration**: The process repeats until quality thresholds are met

## Key Features

### Multi-Agent Collaboration
- **Parallel Agent Execution**: Multiple specialized agents work simultaneously
- **Actor-Critic Dynamics**: Implements reinforcement learning principles with creators as actors and evaluators as critics
- **Structured Feedback**: Critics provide actionable feedback that actors use for improvement
- **Quality-Driven Iteration**: Continuous refinement based on quality metrics

### Creator Agents (Actors)
- Fact Synthesis Agent
- Argument Construction Agent  
- Evidence Integration Agent
- Narrative Flow Agent
- Citation Management Agent

### Evaluator Agents (Critics)
- Factual Accuracy Critic
- Argument Coherence Critic
- Citation Quality Critic
- Structure & Flow Critic
- Originality & Insight Critic

## Installation

```bash
git clone https://github.com/duncan/essayforge.git
cd essayforge
go mod tidy
go build -o essayforge cmd/main.go
```

## Usage

Basic usage:
```bash
essayforge -t "your research topic"
```

Advanced usage with full collaborative mode:
```bash
essayforge \
  -t "artificial intelligence in healthcare" \
  -m collaborative \
  --iterations 5 \
  --quality-threshold 0.85 \
  --show-dialogue \
  -o ai-healthcare.md
```

## Command-Line Options

- `-t, --topic`: Research topic (required)
- `-o, --output`: Output file path (default: essay.md)
- `-m, --mode`: Generation mode: standard, collaborative, ultra (default: collaborative)
- `--iterations`: Maximum collaborative iterations (default: 3)
- `--quality-threshold`: Target quality score 0.0-1.0 (default: 0.8)
- `--show-dialogue`: Display agent interactions
- `--save-iterations`: Save intermediate versions
- `--demo`: Run in demo mode (no API calls)
- `-f, --format`: Output format: markdown, latex, html (default: markdown)
- `--model`: Claude model to use (default: claude-3-sonnet-20240229)

## Architecture Advantages

### Actor-Critic Benefits
- **Structured Learning**: Actors learn from critic feedback, similar to RL policy improvement
- **Quality Assurance**: Critics provide consistent quality evaluation
- **Targeted Improvement**: Specific feedback enables focused refinement

### Multi-Agent Collaboration Benefits
- **Diverse Perspectives**: Each agent brings specialized expertise
- **Parallel Processing**: Agents work simultaneously for efficiency
- **Emergent Quality**: Collective intelligence produces superior results
- **Scalability**: Easy to add new specialized agents

## The Collaborative Advantage

Traditional AI writing tools generate content in a single pass. EssayForge's actor-critic approach ensures:

- **Higher Quality**: Multiple iterations with expert feedback
- **Better Research**: Specialized agents for different aspects
- **Improved Coherence**: Critics ensure logical flow and consistency
- **Accurate Citations**: Dedicated agents for source management
- **Emergent Insights**: Multi-agent collaboration reveals connections

## Examples

```bash
# Generate a research essay with visible collaborative dialogue
essayforge \
  -t "quantum computing applications" \
  -m collaborative \
  --show-dialogue \
  -o quantum-computing.md

# High-quality mode with multiple iterations
essayforge \
  -t "climate change mitigation strategies" \
  --iterations 5 \
  --quality-threshold 0.9 \
  --save-iterations

# Export to LaTeX format
essayforge \
  -t "machine learning in finance" \
  -f latex \
  -o ml-finance.tex
```

## Future Enhancements

- Additional specialized agents for domain-specific research
- Enhanced critic evaluation metrics
- Alternative collaborative strategies
- Real-time web research integration
- Multi-language support

## License

MIT License - see LICENSE file for details

## Contributing

We welcome contributions! Key areas for enhancement:
- Additional evaluator critics for specialized domains
- Alternative adversarial training strategies
- Integration with other LLM providers
- Real-time collaboration features

---

*EssayForge: Where AI agents debate to forge knowledge*
