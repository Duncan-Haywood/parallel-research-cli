#!/usr/bin/env python3
"""EssayForge CLI - Adversarial synthesis for research excellence."""

import asyncio
import os
import sys
import click
from dotenv import load_dotenv

from .orchestrator.orchestrator import Config, Orchestrator
from .models.models import OutputFormat

# Load environment variables
load_dotenv()

# Version
VERSION = "3.0.0"


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-t', '--topic', required=False, help='Research topic (required for main command)')
@click.option('-i', '--intensity', default=5, help='Number of specialized research agents to deploy (1-10)')
@click.option('-p', '--parallel', default=3, help='Number of parallel API calls per agent')
@click.option('-n', '--best-of', default=1, help='Number of variations to generate for best-of-n selection')
@click.option('-o', '--output', default='essay.md', help='Output file path')
@click.option('-f', '--format', default='markdown', 
              type=click.Choice(['markdown', 'latex', 'html'], case_sensitive=False),
              help='Output format')
@click.option('--demo', is_flag=True, help='Run in demo mode without Claude API calls')
@click.option('--no-open', is_flag=True, help='Do not automatically open the essay when complete')
@click.option('--no-dashboard', is_flag=True, help='Do not show real-time progress dashboard')
@click.option('--dry-run', is_flag=True, help='Preview cost estimate without running the generation')
@click.option('--token-limit', default=0, help='Maximum tokens to use (0 = unlimited)')
@click.option('--cost-limit', default=0.0, help='Maximum cost in USD (0 = unlimited)')
@click.option('--model', default='claude-3-sonnet-20240229', help='Claude model to use')
def cli(ctx, topic, intensity, parallel, best_of, output, format, demo, no_open, no_dashboard, 
        dry_run, token_limit, cost_limit, model):
    """An AI-powered research synthesis system inspired by GANs, where Creator and Evaluator agents 
    collaborate through iterative refinement to produce publication-quality essays.
    
    Features:
    - Adversarial creator-evaluator dynamics for quality improvement.
    - Iterative refinement with quality thresholds.
    - Parallel execution with best-of-N selection.
    - Multiple output formats (Markdown, LaTeX, HTML).
    - Real-time progress and dialogue visualization.
    - Token usage and cost tracking.
    """
    if ctx.invoked_subcommand is None:
        # Main command execution
        if not topic:
            click.echo("Error: topic is required")
            click.echo(ctx.get_help())
            sys.exit(1)
        
        if dry_run:
            click.echo("\n\033[33mThis is a dry run. No essay will be generated.\033[0m")
            click.echo("\033[90mRemove --dry-run to proceed with generation.\033[0m")
            sys.exit(0)
        
        # Map format string to enum
        format_map = {
            'markdown': OutputFormat.MARKDOWN,
            'latex': OutputFormat.LATEX,
            'html': OutputFormat.HTML
        }
        output_format = format_map[format.lower()]
        
        # Adjust output file extension if needed
        if '.' not in output:
            ext_map = {
                OutputFormat.MARKDOWN: '.md',
                OutputFormat.LATEX: '.tex',
                OutputFormat.HTML: '.html'
            }
            output += ext_map[output_format]
        
        # Check API key
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key and not demo:
            click.echo("Error: ANTHROPIC_API_KEY environment variable not set.")
            sys.exit(1)
        
        # Create config
        config = Config(
            topic=topic,
            intensity=intensity,
            parallelism=parallel,
            best_of_n=best_of,
            output_file=output,
            demo_mode=demo,
            auto_open=not no_open,
            api_key=api_key or "",
            output_format=output_format,
            show_dashboard=not no_dashboard,
            token_limit=token_limit,
            cost_limit=cost_limit,
            claude_model=model
        )
        
        # Run orchestrator
        try:
            orchestrator = Orchestrator(config)
            asyncio.run(orchestrator.execute())
        except Exception as e:
            click.echo(f"\nResearch failed: {e}", err=True)
            sys.exit(1)


@cli.command()
def version():
    """Print version information."""
    click.echo(f"EssayForge v{VERSION}")


@cli.command()
def models():
    """List available Claude models."""
    click.echo("Available Claude models:")
    click.echo("  - claude-3-opus-20240229     (Most capable, higher cost)")
    click.echo("  - claude-3-sonnet-20240229   (Balanced performance/cost) [default]")
    click.echo("  - claude-3-haiku-20240307    (Fastest, lowest cost)")


@cli.command()
def estimate():
    """Estimate costs for research paper generation (coming soon)."""
    click.echo("Cost estimation is being updated for the new intensity-based system.")


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()