#!/usr/bin/env python3
"""
EssayForge - Multi-agent collaborative synthesis for research excellence

An AI-powered research synthesis system implementing an Actor-Critic architecture
inspired by reinforcement learning, where Creator agents (actors) and Evaluator
agents (critics) collaborate through iterative refinement to produce
publication-quality essays.
"""

import argparse
import os
import sys
from pathlib import Path

from essayforge import __version__
from essayforge.models import OutputFormat
from essayforge.orchestrator import Config, Orchestrator


def create_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog='essayforge',
        description="""An AI-powered research synthesis system implementing an Actor-Critic architecture inspired by 
reinforcement learning, where Creator agents (actors) and Evaluator agents (critics) collaborate 
through iterative refinement to produce publication-quality essays.

Features:
- Actor-critic dynamics with structured feedback for quality improvement.
- Iterative refinement with quality thresholds.
- Parallel execution with best-of-N selection.
- Multiple output formats (Markdown, LaTeX, HTML).
- Real-time progress and dialogue visualization.
- Token usage and cost tracking.""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Core options
    parser.add_argument(
        '-t', '--topic',
        type=str,
        required=True,
        help='Research topic (required)'
    )
    parser.add_argument(
        '-i', '--intensity',
        type=int,
        default=5,
        help='Number of specialized research agents to deploy (1-10)'
    )
    parser.add_argument(
        '-p', '--parallel',
        type=int,
        default=3,
        help='Number of parallel API calls per agent'
    )
    parser.add_argument(
        '-n', '--best-of',
        type=int,
        default=1,
        help='Number of variations to generate for best-of-n selection'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='essay.md',
        help='Output file path'
    )
    parser.add_argument(
        '-f', '--format',
        type=str,
        default='markdown',
        choices=['markdown', 'latex', 'html'],
        help='Output format: markdown, latex, html'
    )
    
    # Feature flags
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run in demo mode without Claude API calls'
    )
    parser.add_argument(
        '--no-open',
        action='store_true',
        help='Do not automatically open the essay when complete'
    )
    parser.add_argument(
        '--no-dashboard',
        action='store_true',
        help='Do not show real-time progress dashboard'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview cost estimate without running the generation'
    )
    
    # Resource limits
    parser.add_argument(
        '--token-limit',
        type=int,
        default=0,
        help='Maximum tokens to use (0 = unlimited)'
    )
    parser.add_argument(
        '--cost-limit',
        type=float,
        default=0,
        help='Maximum cost in USD (0 = unlimited)'
    )
    
    # Model selection
    parser.add_argument(
        '--model',
        type=str,
        default='claude-3-sonnet-20240229',
        help='Claude model to use'
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Version command
    version_parser = subparsers.add_parser('version', help='Print version information')
    
    # Models command
    models_parser = subparsers.add_parser('models', help='List available Claude models')
    
    # Estimate command
    estimate_parser = subparsers.add_parser('estimate', help='Estimate costs for research paper generation')
    
    return parser


def run_research(args):
    """Run the research generation process."""
    if args.dry_run:
        print("\n\033[33mThis is a dry run. No essay will be generated.\033[0m")
        print("\033[90mRemove --dry-run to proceed with generation.\033[0m")
        sys.exit(0)
    
    # Determine output format
    format_map = {
        'markdown': OutputFormat.MARKDOWN,
        'md': OutputFormat.MARKDOWN,
        'latex': OutputFormat.LATEX,
        'tex': OutputFormat.LATEX,
        'html': OutputFormat.HTML
    }
    
    output_format = format_map.get(args.format.lower())
    if not output_format:
        print(f"Error: unsupported format '{args.format}'. Use: markdown, latex, or html")
        sys.exit(1)
    
    # Add extension if missing
    output_file = args.output
    if '.' not in output_file:
        extensions = {
            OutputFormat.MARKDOWN: '.md',
            OutputFormat.LATEX: '.tex',
            OutputFormat.HTML: '.html'
        }
        output_file += extensions.get(output_format, '.md')
    
    # Check API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key and not args.demo:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)
    
    # Create configuration
    config = Config(
        topic=args.topic,
        intensity=args.intensity,
        parallelism=args.parallel,
        best_of_n=args.best_of,
        output_file=output_file,
        demo_mode=args.demo,
        auto_open=not args.no_open,
        api_key=api_key,
        output_format=output_format,
        show_dashboard=not args.no_dashboard,
        token_limit=args.token_limit,
        cost_limit=args.cost_limit,
        claude_model=args.model
    )
    
    # Create and run orchestrator
    try:
        orchestrator = Orchestrator(config)
        orchestrator.execute()
    except Exception as e:
        print(f"\nResearch failed: {e}")
        sys.exit(1)


def show_version():
    """Print version information."""
    print(f"EssayForge v{__version__}")


def show_models():
    """List available Claude models."""
    print("Available Claude models:")
    print("  - claude-3-opus-20240229     (Most capable, higher cost)")
    print("  - claude-3-sonnet-20240229   (Balanced performance/cost) [default]")
    print("  - claude-3-haiku-20240307    (Fastest, lowest cost)")


def show_estimate():
    """Show cost estimation (placeholder)."""
    print("Cost estimation is being updated for the new intensity-based system.")


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle subcommands
    if args.command == 'version':
        show_version()
    elif args.command == 'models':
        show_models()
    elif args.command == 'estimate':
        show_estimate()
    else:
        # Main research command
        if not args.topic and args.command is None:
            parser.print_help()
            sys.exit(1)
        run_research(args)


if __name__ == '__main__':
    main()