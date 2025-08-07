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

## Features

- **GAN-Inspired Architecture**: Creator agents generate content while evaluator agents provide critical feedback, driving iterative improvement
- **Multi-Agent Research System**: Deploy up to 10 specialized research agents working in parallel
- **Intelligent Synthesis**: Advanced content merging and organization algorithms
- **Quality Assurance**: Built-in fact-checking, citation verification, and coherence analysis
- **Multiple Output Formats**: Export to Markdown, LaTeX, or HTML
- **Real-time Dashboard**: Monitor progress, token usage, and costs as research proceeds
- **Cost Controls**: Set token and dollar limits to manage API usage
- **Demo Mode**: Test the system without API calls

## Installation

### Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management)
- An Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com))

### Install Poetry

If you don't have Poetry installed:

```bash
# Using the official installer (recommended)
curl -sSL https://install.python-poetry.org | python3 -

# Or using pip
pip install poetry
```

### Install EssayForge

```bash
# Clone the repository
git clone https://github.com/duncan/essayforge.git
cd essayforge

# Install dependencies with Poetry
poetry install

# Activate the virtual environment
poetry shell
```

### Set up your API key

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Or create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=your-api-key-here
```

## Usage

### Basic Usage

```bash
# Generate an essay on quantum computing
poetry run essayforge -t "quantum computing"

# Or if you're in the poetry shell
essayforge -t "quantum computing"

# Use more research agents for deeper analysis
poetry run essayforge -t "climate change" -i 8

# Generate LaTeX output
poetry run essayforge -t "artificial intelligence" -f latex -o research.tex

# Demo mode (no API calls)
poetry run essayforge -t "blockchain technology" --demo
```

### Advanced Options

```bash
# Full example with all options
poetry run essayforge \
  -t "sustainable energy solutions" \
  -i 10 \                    # Use all 10 research agents
  -p 5 \                     # 5 parallel API calls
  -n 3 \                     # Generate 3 variations, pick best
  -o energy_research.html \  # Output file
  -f html \                  # HTML format
  --token-limit 50000 \      # Max 50k tokens
  --cost-limit 5.0 \         # Max $5 cost
  --model claude-3-opus-20240229  # Use most capable model
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--topic` | `-t` | Research topic (required) | - |
| `--intensity` | `-i` | Number of research agents (1-10) | 5 |
| `--parallel` | `-p` | Parallel API calls per agent | 3 |
| `--best-of` | `-n` | Generate N variations, select best | 1 |
| `--output` | `-o` | Output file path | essay.md |
| `--format` | `-f` | Output format: markdown, latex, html | markdown |
| `--demo` | - | Run without API calls | false |
| `--no-open` | - | Don't auto-open the result | false |
| `--no-dashboard` | - | Disable progress dashboard | false |
| `--token-limit` | - | Maximum tokens (0=unlimited) | 0 |
| `--cost-limit` | - | Maximum cost in USD (0=unlimited) | 0 |
| `--model` | - | Claude model to use | claude-3-sonnet-20240229 |

### Available Commands

```bash
# Show version
poetry run essayforge version

# List available Claude models
poetry run essayforge models

# Estimate costs (coming soon)
poetry run essayforge estimate
```

## Research Agents

The intensity parameter controls how many specialized agents are deployed:

1. **Fact Gatherer** - Core facts and verifiable information
2. **Current State** - Latest developments and trends
3. **Expert Opinions** - Authoritative perspectives
4. **Historical Context** - Background and evolution
5. **Counter Arguments** - Critical analysis and opposing views
6. **Future Projections** - Trends and predictions
7. **Case Studies** - Real-world examples
8. **Data Analysis** - Statistical insights
9. **Theoretical Framework** - Academic foundations
10. **Practical Applications** - Implementation strategies

## Output Formats

### Markdown (Default)
- Clean, readable format
- GitHub-compatible
- Easy to convert to other formats

### LaTeX
- Publication-ready academic format
- Professional typography
- Citation management

### HTML
- Self-contained web page
- Modern, responsive design
- Interactive elements

## Cost Management

EssayForge provides detailed cost tracking:

- Real-time token usage monitoring
- Per-agent token tracking
- Cost estimates based on current Claude pricing
- Configurable limits to prevent overruns

### Typical Costs

| Intensity | Tokens (avg) | Cost (Sonnet) | Cost (Opus) |
|-----------|--------------|---------------|-------------|
| 3 agents | ~15,000 | ~$0.20 | ~$0.75 |
| 5 agents | ~25,000 | ~$0.35 | ~$1.25 |
| 10 agents | ~50,000 | ~$0.70 | ~$2.50 |

## Development

### Project Structure

```
essayforge/
├── essayforge/
│   ├── agents/          # Research agent definitions
│   ├── models/          # Data models
│   ├── orchestrator/    # Main coordination logic
│   ├── synthesis/       # Content synthesis
│   ├── output/          # Output formatting
│   ├── ui/              # Dashboard and UI
│   └── cli.py           # CLI entry point
├── pyproject.toml       # Poetry configuration
├── poetry.lock          # Locked dependencies
└── README.md
```

### Running Tests

```bash
# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=essayforge

# Run linting
poetry run flake8 essayforge
poetry run mypy essayforge

# Format code
poetry run black essayforge
poetry run isort essayforge
```

### Development Setup

```bash
# Install with development dependencies
poetry install --with dev

# Run in development mode
poetry run essayforge --demo -t "test topic"
```

## Examples

See the `examples/` directory for sample outputs and use cases. Run the example script:

```bash
python example.py  # Shows all examples
python example.py 1  # Runs the first example
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with proper tests
4. Run the test suite and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Acknowledgments

- Inspired by GAN architecture and adversarial training
- Built with Claude API by Anthropic
- Uses Rich for beautiful terminal output
- Managed with Poetry for modern Python packaging
