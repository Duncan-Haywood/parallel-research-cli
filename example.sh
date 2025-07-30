#!/bin/bash

# Example usage of parallel-research-cli

echo "You can run the CLI in two ways:"
echo "1. Using go run (no build required):"
echo "   go run cmd/main.go -t \"your topic\" -p 5 -n 3"
echo ""
echo "2. Building first then running:"
echo "   go build -o parallel-research cmd/main.go"
echo "   ./parallel-research -t \"your topic\" -p 5 -n 3"
echo ""

# Using go run for examples
echo -e "\n🔍 Example 1: Quick research on a technical topic"
go run cmd/main.go -t "WebAssembly security implications" -d quick -o wasm-security.md

echo -e "\n🔍 Example 2: Thorough research with more parallelism"
go run cmd/main.go -t "sustainable urban transportation solutions" -p 8 -n 4 -d thorough -o urban-transport.md

echo -e "\n🔍 Example 3: Exhaustive research for academic paper"
go run cmd/main.go -t "CRISPR gene editing ethical considerations" -p 10 -n 5 -d exhaustive -o crispr-ethics.md

echo -e "\nResearch complete! Check the generated markdown files."