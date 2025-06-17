#!/bin/bash

# Job Application Assistant - Installation Script for Linux/macOS
# This script sets up the Job Application Assistant with all dependencies

set -e

echo "🚀 Job Application Assistant Installation Script"
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    print_error "Please don't run this script as root!"
    exit 1
fi

# Detect OS
OS=""
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

print_status "Detected OS: $OS"

# Check for required tools
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check for Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first:"
        if [ "$OS" = "macos" ]; then
            echo "  - Download Docker Desktop from: https://www.docker.com/products/docker-desktop"
        else
            echo "  - Install Docker: https://docs.docker.com/engine/install/"
        fi
        exit 1
    fi
    
    # Check for Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check for Python (optional, for non-Docker setup)
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
        print_status "Python $PYTHON_VERSION found"
    fi
    
    print_success "System requirements check passed!"
}

# Setup environment
setup_environment() {
    print_status "Setting up environment..."
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        print_status "Creating .env file from template..."
        cp .env.example .env
        print_warning "Please edit .env file to add your API keys (optional for local-only usage)"
    fi
    
    # Create data directories
    mkdir -p data logs uploads
    
    print_success "Environment setup completed!"
}

# Install Ollama (optional)
install_ollama() {
    print_status "Would you like to install Ollama for local LLM support? (y/N)"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        print_status "Installing Ollama..."
        
        if [ "$OS" = "macos" ]; then
            # macOS installation
            if command -v brew &> /dev/null; then
                brew install ollama
            else
                curl -fsSL https://ollama.com/install.sh | sh
            fi
        else
            # Linux installation
            curl -fsSL https://ollama.com/install.sh | sh
        fi
        
        print_success "Ollama installed successfully!"
        
        # Start Ollama service
        print_status "Starting Ollama service..."
        ollama serve &
        sleep 3
        
        # Pull recommended models
        print_status "Would you like to download recommended models? (llama3.1:8b, qwen2.5:7b) (y/N)"
        read -r model_response
        
        if [[ "$model_response" =~ ^[Yy]$ ]]; then
            print_status "Downloading models (this may take a while)..."
            ollama pull llama3.1:8b
            ollama pull qwen2.5:7b
            print_success "Models downloaded successfully!"
        fi
    fi
}

# Setup Docker
setup_docker() {
    print_status "Setting up Docker containers..."
    
    # Build the application
    print_status "Building Docker image..."
    docker-compose build
    
    print_success "Docker setup completed!"
}

# Setup Python environment (alternative to Docker)
setup_python() {
    print_status "Would you like to set up Python environment as well? (y/N)"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        print_status "Setting up Python virtual environment..."
        
        # Create virtual environment
        python3 -m venv venv
        source venv/bin/activate
        
        # Install dependencies
        pip install --upgrade pip
        pip install -r requirements.txt
        
        print_success "Python environment setup completed!"
        print_status "To activate the environment, run: source venv/bin/activate"
    fi
}

# Main installation
main() {
    echo
    print_status "Starting installation process..."
    
    check_requirements
    setup_environment
    install_ollama
    setup_docker
    setup_python
    
    echo
    print_success "Installation completed successfully! 🎉"
    echo
    echo "Quick Start:"
    echo "  1. Docker (recommended): docker-compose up -d"
    echo "  2. Python: source venv/bin/activate && streamlit run job_application_assistant/web/app.py"
    echo "  3. CLI: python -m job_application_assistant.cli.main --help"
    echo
    echo "Access the web interface at: http://localhost:8501"
    echo
    echo "For more information, see README.md"
}

# Run main function
main "$@"
