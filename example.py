#!/usr/bin/env python3
"""Example usage of EssayForge."""

import subprocess
import sys

# Example commands to demonstrate EssayForge usage
examples = [
    {
        "description": "Basic usage - Generate an essay on quantum computing",
        "command": ["poetry", "run", "essayforge", "-t", "quantum computing"]
    },
    {
        "description": "Demo mode - Test without API calls",
        "command": ["poetry", "run", "essayforge", "-t", "artificial intelligence ethics", "--demo"]
    },
    {
        "description": "High intensity research with 8 agents",
        "command": ["poetry", "run", "essayforge", "-t", "climate change solutions", "-i", "8"]
    },
    {
        "description": "Generate LaTeX output for academic paper",
        "command": ["poetry", "run", "essayforge", "-t", "machine learning in healthcare", "-f", "latex", "-o", "ml_healthcare.tex"]
    },
    {
        "description": "HTML output with cost limits",
        "command": ["poetry", "run", "essayforge", "-t", "renewable energy", "-f", "html", "-o", "energy.html", "--cost-limit", "2.0"]
    },
    {
        "description": "Full configuration example",
        "command": [
            "poetry", "run", "essayforge",
            "-t", "future of transportation",
            "-i", "10",           # All 10 agents
            "-p", "5",            # 5 parallel calls
            "-n", "3",            # Best of 3
            "-o", "transport.md",
            "--token-limit", "50000",
            "--model", "claude-3-opus-20240229",
            "--no-dashboard"      # Disable dashboard
        ]
    }
]

def main():
    print("EssayForge Example Usage")
    print("=" * 50)
    print()
    
    if len(sys.argv) > 1:
        # Run specific example
        try:
            idx = int(sys.argv[1]) - 1
            if 0 <= idx < len(examples):
                example = examples[idx]
                print(f"Running: {example['description']}")
                print(f"Command: {' '.join(example['command'])}")
                print("-" * 50)
                subprocess.run(example["command"])
            else:
                print(f"Invalid example number. Choose 1-{len(examples)}")
        except ValueError:
            print("Please provide a valid example number")
    else:
        # Show all examples
        print("Available examples:")
        print()
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example['description']}")
            print(f"   $ {' '.join(example['command'])}")
            print()
        
        print("To run an example, use:")
        print("  python example.py <number>")
        print()
        print("For example:")
        print("  python example.py 1  # Run the basic usage example")

if __name__ == "__main__":
    main()