#!/bin/bash

# Job Application Assistant Docker Build and Publish Script

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

# Configuration
IMAGE_NAME="job-application-assistant"
REGISTRY="docker.io"  # Change this to your registry
USERNAME="${DOCKERHUB_USERNAME:-yourusername}"  # Change this to your username

# Get version from pyproject.toml
VERSION=$(grep -E "^version = " pyproject.toml | sed 's/version = "\(.*\)"/\1/')

if [ -z "$VERSION" ]; then
    error "Could not find version in pyproject.toml"
fi

info "Building Docker image for version $VERSION"

# Build the image
info "Building Docker image..."
docker build -t "$IMAGE_NAME:$VERSION" -t "$IMAGE_NAME:latest" .
success "Docker image built successfully"

# Test the image
info "Testing Docker image..."
docker run --rm "$IMAGE_NAME:$VERSION" --help > /dev/null || error "Docker image test failed"
success "Docker image test passed"

# Ask if user wants to publish
read -p "Do you want to publish to Docker Hub? (y/N): " PUBLISH_CONFIRM

if [[ $PUBLISH_CONFIRM =~ ^[Yy]$ ]]; then
    # Check if user is logged in to Docker Hub
    info "Checking Docker Hub login..."
    if ! docker info | grep -q "Username:"; then
        warning "Not logged in to Docker Hub"
        read -p "Docker Hub username: " HUB_USERNAME
        docker login --username "$HUB_USERNAME" || error "Docker login failed"
    fi
    success "Docker Hub login verified"
    
    # Tag for registry
    FULL_IMAGE_NAME="$REGISTRY/$USERNAME/$IMAGE_NAME"
    
    info "Tagging image for registry..."
    docker tag "$IMAGE_NAME:$VERSION" "$FULL_IMAGE_NAME:$VERSION"
    docker tag "$IMAGE_NAME:latest" "$FULL_IMAGE_NAME:latest"
    success "Image tagged for registry"
    
    # Push to registry
    info "Pushing to Docker Hub..."
    docker push "$FULL_IMAGE_NAME:$VERSION"
    docker push "$FULL_IMAGE_NAME:latest"
    success "Image pushed to Docker Hub"
    
    echo
    success "Docker image published successfully!"
    info "Image available at: $FULL_IMAGE_NAME:$VERSION"
    info "Latest tag: $FULL_IMAGE_NAME:latest"
    echo
    info "Usage:"
    echo "  docker run -it --rm $FULL_IMAGE_NAME:latest --help"
    echo "  docker-compose up (using provided docker-compose.yml)"
else
    info "Skipping Docker Hub publish"
    echo
    success "Docker image built successfully!"
    info "Local images:"
    echo "  $IMAGE_NAME:$VERSION"
    echo "  $IMAGE_NAME:latest"
    echo
    info "Usage:"
    echo "  docker run -it --rm $IMAGE_NAME:latest --help"
    echo "  docker-compose up (using provided docker-compose.yml)"
fi

echo
info "Docker build process completed!"
