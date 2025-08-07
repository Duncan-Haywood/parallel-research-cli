#!/bin/bash

# Example usage of EssayForge

echo "You can run EssayForge in two ways:"
echo "1. Using go run (no build required):"
echo "   go run cmd/main.go -t \"your topic\" -m collaborative"
echo ""
echo "2. Building first then running:"
echo "   go build -o essayforge cmd/main.go"
echo "   ./essayforge -t \"your topic\" -m collaborative"
echo ""

# Using go run for examples
echo -e "\n🔍 Example 1: Quick research with standard mode"
go run cmd/main.go -t "WebAssembly security implications" -d quick -o wasm-security.md

echo -e "\n🔍 Example 2: Collaborative mode with visible dialogue"
go run cmd/main.go -t "sustainable urban transportation solutions" -m collaborative --iterations 3 --show-dialogue -o urban-transport.md

echo -e "\n🔍 Example 3: Full collaborative synthesis with high quality threshold"
go run cmd/main.go -t "CRISPR gene editing ethical considerations" -m collaborative --iterations 5 --quality-threshold 0.9 --save-iterations -o crispr-ethics.md

echo -e "\nResearch complete! Check the generated essays and iteration drafts."