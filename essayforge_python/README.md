# EssayForge Python

**Multi-agent collaborative synthesis for research excellence**

A Python implementation of EssayForge - an AI-powered research synthesis system implementing an Actor-Critic architecture inspired by reinforcement learning, where Creator agents (actors) and Evaluator agents (critics) collaborate through iterative refinement to produce publication-quality essays.

## Installation

### From Source

```bash
git clone https://github.com/duncan/essayforge-python.git
cd essayforge-python
pip install -e .
```

### Using pip

```bash
pip install -r requirements.txt
python main.py --help
```

## Usage

Basic usage:
```bash
python main.py -t "your research topic"
```

Advanced usage with full features:
```bash
python main.py \
  -t "artificial intelligence in healthcare" \
  -i 8 \
  --parallel 4 \
  --best-of 3 \
  -o ai-healthcare.md \
  -f markdown
```

## Command-Line Options

- `-t, --topic`: Research topic (required)
- `-o, --output`: Output file path (default: essay.md)
- `-i, --intensity`: Number of specialized research agents to deploy 1-10 (default: 5)
- `-p, --parallel`: Number of parallel API calls per agent (default: 3)
- `-n, --best-of`: Number of variations to generate for best-of-n selection (default: 1)
- `--demo`: Run in demo mode (no API calls)
- `--no-open`: Do not automatically open the essay when complete
- `--no-dashboard`: Do not show real-time progress dashboard
- `--dry-run`: Preview cost estimate without running
- `-f, --format`: Output format: markdown, latex, html (default: markdown)
- `--model`: Claude model to use (default: claude-3-sonnet-20240229)
- `--token-limit`: Maximum tokens to use (0 = unlimited)
- `--cost-limit`: Maximum cost in USD (0 = unlimited)

## Environment Setup

Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
ANTHROPIC_API_KEY=your-api-key-here
```

## Architecture

The Python implementation maintains the same Actor-Critic architecture as the original Go version:

### Research Agents (Actors)
- Fact Gatherer
- Historical Context
- Current State Analysis
- Future Projections
- Counter Arguments
- Expert Opinions
- Case Studies
- Data Analysis
- Theoretical Framework
- Practical Applications

### Evaluator Agents (Critics)
- Factual Accuracy Critic
- Argument Coherence Critic
- Citation Quality Critic
- Structure & Flow Critic
- Originality & Insight Critic

## Project Structure

```
essayforge-python/
├── main.py                 # CLI entry point
├── essayforge/
│   ├── __init__.py
│   ├── models/            # Data models
│   ├── agents/            # Research agents
│   ├── orchestrator/      # Coordination logic
│   ├── synthesis/         # Essay synthesis
│   ├── output/            # Output formatting
│   └── ui/                # Progress dashboard
├── requirements.txt
├── setup.py
└── README.md
```

## Examples

Generate a research essay with visible progress:
```bash
python main.py -t "quantum computing applications" --demo
```

High-quality mode with multiple agents:
```bash
python main.py \
  -t "climate change mitigation strategies" \
  -i 10 \
  --best-of 3 \
  -o climate-strategies.md
```

Export to different formats:
```bash
# LaTeX format
python main.py -t "machine learning in finance" -f latex -o ml-finance.tex

# HTML format
python main.py -t "renewable energy" -f html -o renewable-energy.html
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black essayforge/
```

### Type Checking
```bash
mypy essayforge/
```

## Differences from Go Version

This Python implementation provides:
- Same core functionality and architecture
- Simplified async handling using Python's asyncio
- Native Python data classes instead of Go structs
- Pythonic CLI using argparse
- Compatible output formats

Some advanced features from the Go version are simplified or marked for future implementation.

## Contributing

Contributions are welcome! Key areas for enhancement:
- Full Anthropic API integration
- Advanced agent implementations
- Enhanced synthesis algorithms
- Additional output formats
- Performance optimizations

## License

MIT License - see LICENSE file for details

---

*EssayForge Python: Where AI agents collaborate to forge knowledge*