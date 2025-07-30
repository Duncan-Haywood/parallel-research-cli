# Parallel Research CLI

A Go-based meta-CLI that orchestrates multiple Claude processes in parallel to conduct thorough research and generate well-cited essays. It implements an encoder-decoder architecture where research expands wide across multiple specialized agents, then synthesizes back into a single comprehensive output.

## Architecture

```
Input Topic
    |
    v
[Encoder: Parallel Research Phase]
    |
    +---> Fact Gatherer Agent (x3 variations)
    +---> Current State Agent (x3 variations)
    +---> Expert Opinions Agent (x3 variations)
    +---> Historical Context Agent (x3 variations)
    +---> Counter Arguments Agent (x3 variations)
    +---> Future Projections Agent (x3 variations)
    +---> Case Studies Agent (x3 variations)
    +---> Data Analysis Agent (x3 variations)
    |
    v
[Best-of-N Selection per Agent Type]
    |
    v
[Decoder: Synthesis Phase]
    |
    v
Final Essay (Markdown)
```

## Features

- **Multiple Research Modes**: Standard, professional, and ultra modes for different levels of research depth.
- **Parallel Processing**: Spawns multiple Claude API calls simultaneously.
- **Best-of-N Selection**: Generates multiple variations per agent and selects the best.
- **Specialized Agents**: Different agent types focus on specific research aspects.
- **Automatic Citation Extraction**: Preserves and formats all citations.
- **Configurable Depth**: Quick, standard, thorough, or exhaustive research modes.
- **Multiple Output Formats**: Export to Markdown, LaTeX, or HTML.
- **Live Progress Dashboard**: Real-time visualization of agent progress.
- **Token & Cost Tracking**: Monitor API usage and estimated costs.
- **Quality Scoring**: Automated quality metrics for research and citations.

## Installation

```bash
cd parallel-research-cli
go mod tidy
go build -o parallel-research cmd/main.go
```

## Usage

First, set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

Basic usage:
```bash
./parallel-research -t "quantum computing applications in cryptography"
```

Advanced options:
```bash
./parallel-research \
  -t "climate change mitigation strategies" \
  -m ultra \
  -p 8 \
  -n 5 \
  -d exhaustive \
  -o climate-essay \
  -f latex \
  --dashboard \
  --cost-limit 10.00 \
  --model claude-3-opus-20240229
```

## Command Line Options

### Core Options
- `-t, --topic`: Research topic (required)
- `-m, --mode`: Research mode: standard, professional, ultra (default: standard)
- `-p, --parallel`: Number of parallel research agents (default: 5)
- `-n, --best-of`: Number of variations to generate for best-of-n selection (default: 3)
- `-d, --depth`: Research depth: quick, standard, thorough, exhaustive (default: thorough)

### Output Options
- `-o, --output`: Output file path (default: essay.md)
- `-f, --format`: Output format: markdown, latex, html (default: markdown)

### Feature Flags
- `--demo`: Run in demo mode without Claude API calls
- `--open`: Automatically open the essay when complete (default: true)
- `--dashboard`: Show real-time progress dashboard (default: true)

### Resource Limits
- `--token-limit`: Maximum tokens to use (0 = unlimited)
- `--cost-limit`: Maximum cost in USD (0 = unlimited)

### Model Selection
- `--model`: Claude model to use (default: claude-3-sonnet-20240229)
  - claude-3-opus-20240229 (most capable, higher cost)
  - claude-3-sonnet-20240229 (balanced performance/cost)
  - claude-3-haiku-20240307 (fastest, lowest cost)

## How It Works

1.  **Topic Analysis**: The topic is distributed to all configured agent types.
2.  **Parallel Research**: Each agent type spawns N variations (best-of-n).
3.  **Quality Scoring**: Each research output is scored based on content, citations, and structure.
4.  **Best Selection**: The highest-scoring variation for each agent type is selected.
5.  **Synthesis**: Selected research is combined using a master synthesis agent.
6.  **Citation Management**: All citations are extracted, deduplicated, and formatted.
7.  **Final Output**: A comprehensive essay with proper structure and references.

## Requirements

- Go 1.21+
- An active Anthropic API key with access to the Claude 3 models.

## License

MIT
