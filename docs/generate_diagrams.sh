#!/bin/bash

# Star Trek RAG System - PlantUML Diagram Generator
# This script generates PNG images from PlantUML diagrams

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Star Trek RAG System - PlantUML Diagram Generator${NC}"
echo "=================================================="

# Check if PlantUML is installed
if ! command -v plantuml &> /dev/null; then
    echo -e "${RED}❌ PlantUML is not installed.${NC}"
    echo -e "${YELLOW}Please install PlantUML:${NC}"
    echo "  Ubuntu/Debian: sudo apt-get install plantuml"
    echo "  macOS: brew install plantuml"
    echo "  Or download from: https://plantuml.com/download"
    exit 1
fi

echo -e "${GREEN}✅ PlantUML found${NC}"

# Create output directory
OUTPUT_DIR="images"
mkdir -p "$OUTPUT_DIR"

echo -e "${BLUE}📁 Output directory: $OUTPUT_DIR${NC}"

# Generate diagrams from architecture.puml
if [ -f "architecture.puml" ]; then
    echo -e "${YELLOW}🔄 Generating diagrams from architecture.puml...${NC}"
    
    # Generate PNG images
    plantuml -tpng architecture.puml -o "../$OUTPUT_DIR"
    
    echo -e "${GREEN}✅ Diagrams generated successfully!${NC}"
    echo ""
    echo -e "${BLUE}📊 Generated diagrams:${NC}"
    ls -la "$OUTPUT_DIR"/*.png 2>/dev/null || echo "No PNG files found"
    
else
    echo -e "${RED}❌ architecture.puml not found in current directory${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Diagram generation complete!${NC}"
echo -e "${BLUE}📖 View the diagrams in the $OUTPUT_DIR directory${NC}"
echo -e "${BLUE}📚 Check docs/README.md for diagram descriptions${NC}" 