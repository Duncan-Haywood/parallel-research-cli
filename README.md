# EssayForge

**Adversarial synthesis for research excellence**

An AI-powered research synthesis system inspired by Generative Adversarial Networks (GANs), where Creator and Evaluator agents collaborate through iterative refinement to produce publication-quality essays. The system implements a dialogue-based approach where agents compete and collaborate, with quality assessment driving continuous improvement—similar to how discriminators and generators work in GANs.

## The GAN-Inspired Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Input: Research Topic                 │
└────────────────────────┬────────────────────────────────┘
                         │
                         v
┌─────────────────────────────────────────────────────────┐
│                  CREATOR NETWORK                         │
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
│                 EVALUATOR NETWORK                        │
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

## How It Works: The Adversarial Loop

1. **Creation Phase**: Multiple Creator agents work in parallel to generate research content, arguments, and evidence from different perspectives.

2. **Evaluation Phase**: Evaluator agents critically assess the output across multiple dimensions:
   - Factual accuracy and citation quality
   - Logical coherence and argument strength  
   - Structural flow and readability
   - Originality and insight depth

3. **Feedback Integration**: The Creator network receives detailed feedback and regenerates improved content, focusing on identified weaknesses.

4. **Convergence**: Through iterative refinement, the system converges on a high-quality essay that satisfies all evaluation criteria.

## Key Features

### Adversarial Synthesis
- **Creator-Evaluator Dynamics**: Mimics GAN architecture with competing objectives
- **Multi-Agent Collaboration**: Specialized agents for different aspects of research
- **Iterative Refinement**: Continuous improvement through feedback loops
- **Quality Metrics**: Automated scoring across multiple dimensions

### Research Capabilities  
- **Parallel Processing**: Multiple agents work simultaneously
- **Best-of-N Selection**: Generate variations and select the highest quality
- **Comprehensive Coverage**: Agents specialize in facts, arguments, counter-arguments, case studies, and more
- **Citation Management**: Automatic extraction and formatting of all sources

### Customization Options
- **Depth Levels**: Quick, standard, thorough, or exhaustive research
- **Quality Thresholds**: Set minimum quality scores for acceptance
- **Iteration Limits**: Control the refinement process
- **Output Formats**: Markdown, LaTeX, or HTML export

## Installation

```bash
git clone https://github.com/duncan/essayforge.git
cd essayforge
go mod tidy
go build -o essayforge cmd/main.go
```

## Usage

Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-api-key"
```

Basic usage:
```bash
./essayforge -t "quantum computing applications in cryptography"
```

Advanced usage with full adversarial mode:
```bash
./essayforge \
  -t "climate change mitigation strategies" \
  -m adversarial \
  --iterations 5 \
  --quality-threshold 0.85 \
  --creator-agents 8 \
  --evaluator-agents 5 \
  -o climate-essay \
  -f latex \
  --show-dialogue
```

## Command Line Options

### Core Options
- `-t, --topic`: Research topic (required)
- `-m, --mode`: Generation mode: standard, adversarial, ultra (default: adversarial)
- `--iterations`: Maximum adversarial iterations (default: 3)
- `--quality-threshold`: Minimum quality score (0-1) to accept output (default: 0.8)

### Agent Configuration
- `--creator-agents`: Number of parallel creator agents (default: 6)
- `--evaluator-agents`: Number of evaluator critics (default: 4)
- `-n, --best-of`: Variations per agent for selection (default: 3)
- `-d, --depth`: Research depth: quick, standard, thorough, exhaustive

### Output Options
- `-o, --output`: Output file path (default: essay.md)
- `-f, --format`: Output format: markdown, latex, html
- `--show-dialogue`: Display the creator-evaluator dialogue
- `--save-iterations`: Save all iteration drafts

### Resource Management
- `--token-limit`: Maximum tokens to use (0 = unlimited)
- `--cost-limit`: Maximum cost in USD (0 = unlimited)
- `--model`: Claude model selection (opus, sonnet, haiku)

## The Adversarial Advantage

Traditional AI writing tools generate content in a single pass. EssayForge's adversarial approach ensures:

1. **Higher Quality**: Critical evaluation identifies and fixes weaknesses
2. **Better Citations**: Evaluators verify source quality and relevance
3. **Stronger Arguments**: Logical flaws are caught and corrected
4. **Improved Clarity**: Structure and flow are iteratively refined
5. **Reduced Hallucination**: Fact-checking agents validate all claims

## Example Workflow

```bash
# Generate a research essay with visible adversarial dialogue
./essayforge \
  -t "The impact of large language models on scientific research" \
  -m adversarial \
  --iterations 4 \
  --show-dialogue \
  --save-iterations \
  -o llm-science-essay

# Output:
# → Iteration 1: Quality Score: 0.72 (Below threshold)
# → Iteration 2: Quality Score: 0.81 (Improving...)  
# → Iteration 3: Quality Score: 0.88 (Accepted!)
# → Final essay saved to: llm-science-essay.md
# → Iteration drafts saved to: llm-science-essay-iterations/
```

## Requirements

- Go 1.21+
- Anthropic API key with Claude 3 access
- Sufficient API credits for iterative generation

## License

MIT

## Contributing

We welcome contributions! Key areas for enhancement:
- Additional evaluator critics for specialized domains
- Alternative adversarial training strategies
- Integration with other LLM providers
- Real-time collaboration features

---

*EssayForge: Where AI agents debate to forge knowledge*
