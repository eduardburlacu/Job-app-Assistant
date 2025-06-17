#!/bin/bash

# Job Application Assistant Release Script
# This script automates the release process

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    error "Not in a git repository"
fi

# Check if working directory is clean
if [[ -n $(git status --porcelain) ]]; then
    error "Working directory is not clean. Please commit or stash your changes."
fi

# Get version from user
if [ -z "$1" ]; then
    echo "Current version in pyproject.toml:"
    grep -E "^version = " pyproject.toml || error "Could not find version in pyproject.toml"
    echo
    read -p "Enter new version (e.g., 1.0.0): " VERSION
else
    VERSION=$1
fi

# Validate version format
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    error "Invalid version format. Use semantic versioning (e.g., 1.0.0)"
fi

info "Starting release process for version $VERSION"

# Update version in pyproject.toml
info "Updating version in pyproject.toml..."
sed -i.bak "s/^version = .*/version = \"$VERSION\"/" pyproject.toml
rm pyproject.toml.bak
success "Version updated to $VERSION"

# Run all tests
info "Running all tests..."
python test_installation.py || error "Installation test failed"
python test_functionality.py || error "Functionality test failed"
python test_comprehensive.py || error "Comprehensive test failed"
python test_production_ready.py || error "Production readiness test failed"
python test_github_ready.py || error "GitHub readiness test failed"
success "All tests passed"

# Run pre-commit hooks
info "Running pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    pre-commit run --all-files || error "Pre-commit hooks failed"
    success "Pre-commit hooks passed"
else
    warning "Pre-commit not installed, skipping hooks"
fi

# Update CHANGELOG.md
info "Updating CHANGELOG.md..."
TODAY=$(date +%Y-%m-%d)
TEMP_FILE=$(mktemp)

# Create new changelog entry
cat > "$TEMP_FILE" << EOF
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [${VERSION}] - ${TODAY}

### Added
- Version ${VERSION} release

### Changed
- Updated dependencies

### Fixed
- Bug fixes and improvements

EOF

# Append existing changelog (skip the header)
tail -n +8 CHANGELOG.md >> "$TEMP_FILE"
mv "$TEMP_FILE" CHANGELOG.md

success "CHANGELOG.md updated"

# Build the package
info "Building package..."
python -m build || error "Package build failed"
success "Package built successfully"

# Commit changes
info "Committing changes..."
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to $VERSION"
success "Changes committed"

# Create tag
info "Creating git tag..."
git tag -a "v$VERSION" -m "Release version $VERSION"
success "Tag v$VERSION created"

# Push changes and tags
read -p "Push changes to remote repository? (y/N): " PUSH_CONFIRM
if [[ $PUSH_CONFIRM =~ ^[Yy]$ ]]; then
    info "Pushing changes..."
    git push origin main
    git push origin "v$VERSION"
    success "Changes pushed to remote repository"
    
    info "Release v$VERSION completed successfully!"
    echo
    info "Next steps:"
    echo "1. Go to GitHub and create a release from the v$VERSION tag"
    echo "2. Upload the built packages from dist/ directory"
    echo "3. Publish to PyPI: twine upload dist/*"
    echo "4. Build and push Docker image if needed"
else
    warning "Changes not pushed. You can push manually later:"
    echo "  git push origin main"
    echo "  git push origin v$VERSION"
fi

success "Release script completed!"
