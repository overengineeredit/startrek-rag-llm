#!/bin/bash

# Star Trek RAG System - PlantUML Diagram Generator
# This script generates PNG images from PlantUML diagrams

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PLANTUML_JAR="plantuml-1.2024.0.jar"

echo -e "${BLUE}🚀 Star Trek RAG System - PlantUML Diagram Generator${NC}"
echo "=================================================="

# Check if PlantUML jar is present
if [ ! -f "$PLANTUML_JAR" ]; then
    echo -e "${RED}❌ $PLANTUML_JAR not found in docs directory.${NC}"
    echo -e "${YELLOW}Please download the latest PlantUML jar and place it in the docs directory.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ PlantUML jar found${NC}"

# Create output directory
OUTPUT_DIR="./images"
mkdir -p "$OUTPUT_DIR"

echo -e "${BLUE}📁 Output directory: $OUTPUT_DIR${NC}"

# Count total files
TOTAL_FILES=$(ls *.puml 2>/dev/null | wc -l)
SUCCESS_FILES=0
FAILED_FILES=0

echo -e "${BLUE}📊 Found $TOTAL_FILES .puml files to process${NC}"
echo ""

# Generate diagrams from all .puml files in docs
for puml in *.puml; do
    echo -e "${YELLOW}🔄 Generating diagram from $puml...${NC}"
    
    # Capture both stdout and stderr
    OUTPUT=$(java -jar "$PLANTUML_JAR" -tpng -o "$OUTPUT_DIR" "$puml" 2>&1)
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✅ Successfully generated ${puml%.puml}.png${NC}"
        ((SUCCESS_FILES++))
    else
        echo -e "${RED}❌ Failed to generate diagram from $puml${NC}"
        echo -e "${RED}   Error output: $OUTPUT${NC}"
        ((FAILED_FILES++))
    fi
    echo ""
done

echo -e "${GREEN}✅ Diagram generation complete!${NC}"
echo -e "${BLUE}📊 Summary:${NC}"
echo -e "  • Total files: $TOTAL_FILES"
echo -e "  • Successfully processed: $SUCCESS_FILES"
echo -e "  • Failed: $FAILED_FILES"
echo ""
echo -e "${BLUE}📊 Generated diagrams:${NC}"
ls -la "$OUTPUT_DIR"/*.png 2>/dev/null | grep -v architecture_ || echo "No PNG files found"

echo ""
echo -e "${GREEN}🎉 Diagram generation complete!${NC}"
echo -e "${BLUE}📖 View the diagrams in the $OUTPUT_DIR directory${NC}"
echo -e "${BLUE}📚 Check docs/README.md for diagram descriptions${NC}" 