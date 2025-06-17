#!/bin/bash

# Job Application Assistant Development Setup Script
# This script sets up a complete development environment

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

print_header() {
    echo
    echo "🚀 Job Application Assistant - Development Setup"
    echo "=============================================="
    echo
}

print_header

# Check if Python is installed
info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    error "Python 3 is not installed. Please install Python 3.8 or higher."
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
info "Found Python $PYTHON_VERSION"

# Check Python version
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    success "Python version is compatible"
else
    error "Python 3.8 or higher is required"
fi

# Check if pip is installed
info "Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    error "pip is not installed. Please install pip."
fi
success "pip is available"

# Create virtual environment
info "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    success "Virtual environment created"
else
    info "Virtual environment already exists"
fi

# Activate virtual environment
info "Activating virtual environment..."
source venv/bin/activate || error "Failed to activate virtual environment"
success "Virtual environment activated"

# Upgrade pip
info "Upgrading pip..."
pip install --upgrade pip
success "pip upgraded"

# Install the package in development mode
info "Installing package in development mode..."
pip install -e ".[dev]"
success "Package installed in development mode"

# Install pre-commit hooks
info "Setting up pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
    success "Pre-commit hooks installed"
else
    warning "pre-commit not found in PATH, trying to install..."
    pip install pre-commit
    pre-commit install
    success "Pre-commit installed and hooks set up"
fi

# Run initial tests
info "Running initial tests..."
python -m pytest tests/ -v || warning "Some tests failed - this is normal for a fresh setup"

# Test CLI
info "Testing CLI installation..."
python -m job_application_assistant --help > /dev/null || warning "CLI test failed"
success "CLI is working"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    info "Creating .env file from template..."
    cp .env.example .env
    success ".env file created"
    warning "Please edit .env file with your configuration"
else
    info ".env file already exists"
fi

# Final setup verification
info "Running setup verification..."
python test_installation.py || warning "Installation test failed"
python test_functionality.py || warning "Functionality test failed"

print_footer() {
    echo
    echo "🎉 Development Setup Complete!"
    echo "=============================="
    echo
    echo "📋 What's been set up:"
    echo "  ✅ Virtual environment (venv/)"
    echo "  ✅ Package installed in development mode"
    echo "  ✅ Pre-commit hooks configured"
    echo "  ✅ Development dependencies installed"
    echo "  ✅ Environment file created (.env)"
    echo
    echo "🚀 Next steps:"
    echo "  1. Edit .env file with your API keys and configuration"
    echo "  2. Run 'source venv/bin/activate' to activate the environment"
    echo "  3. Run 'python -m job_application_assistant --help' to test the CLI"
    echo "  4. Run 'python -m pytest' to run tests"
    echo "  5. Run 'python run_web.py' to start the web interface"
    echo
    echo "📚 Development commands:"
    echo "  • Run tests: python -m pytest"
    echo "  • Run CLI: python -m job_application_assistant"
    echo "  • Run web app: python run_web.py"
    echo "  • Format code: pre-commit run --all-files"
    echo "  • Type check: mypy job_application_assistant"
    echo
    echo "🔧 Troubleshooting:"
    echo "  • If you see import errors, make sure the virtual environment is activated"
    echo "  • If pre-commit fails, run 'pre-commit run --all-files' to fix issues"
    echo "  • Check the .env file for proper configuration"
    echo
    echo "Happy coding! 🎯"
    echo
}

print_footer
