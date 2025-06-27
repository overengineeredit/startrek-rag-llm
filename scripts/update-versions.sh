#!/bin/bash

# Script to update versions across the project
# Usage: ./scripts/update-versions.sh [new_chroma_version]

set -e

# Default version
CURRENT_VERSION="0.4.24"
NEW_VERSION="${1:-$CURRENT_VERSION}"

if [ "$NEW_VERSION" = "$CURRENT_VERSION" ]; then
    echo "Current ChromaDB version is already $CURRENT_VERSION"
    echo "To update to a different version, run: $0 <new_version>"
    echo "Example: $0 0.4.25"
    exit 0
fi

echo "Updating ChromaDB version from $CURRENT_VERSION to $NEW_VERSION"
echo ""

# Update workflow files
echo "Updating GitHub Actions workflows..."
sed -i "s/CHROMA_VERSION: '$CURRENT_VERSION'/CHROMA_VERSION: '$NEW_VERSION'/g" .github/workflows/build-and-test.yml
sed -i "s/CHROMA_VERSION: '$CURRENT_VERSION'/CHROMA_VERSION: '$NEW_VERSION'/g" .github/workflows/test-only.yml
sed -i "s/CHROMA_VERSION: '$CURRENT_VERSION'/CHROMA_VERSION: '$NEW_VERSION'/g" .github/workflows/release.yml

# Update docker-compose.yml
echo "Updating docker-compose.yml..."
sed -i "s/CHROMA_VERSION:-$CURRENT_VERSION/CHROMA_VERSION:-$NEW_VERSION/g" docker-compose.yml

# Update reference file
echo "Updating config/versions.env..."
sed -i "s/export CHROMA_VERSION=$CURRENT_VERSION/export CHROMA_VERSION=$NEW_VERSION/g" config/versions.env

# Update Makefile
echo "Updating Makefile..."
sed -i "s/ChromaDB: $CURRENT_VERSION/ChromaDB: $NEW_VERSION/g" Makefile

echo ""
echo "✅ Version updated to $NEW_VERSION in all files"
echo ""
echo "Next steps:"
echo "1. Test the changes: make test-docker"
echo "2. Commit the changes: git add . && git commit -m 'Update ChromaDB to $NEW_VERSION'"
echo "3. Push to trigger CI: git push"
echo ""
echo "Files updated:"
echo "  - .github/workflows/build-and-test.yml"
echo "  - .github/workflows/test-only.yml"
echo "  - .github/workflows/release.yml"
echo "  - docker-compose.yml"
echo "  - config/versions.env"
echo "  - Makefile" 