# Job Application Assistant - Installation Script for Windows
# This script sets up the Job Application Assistant with all dependencies

param(
    [switch]$SkipOllama,
    [switch]$SkipPython,
    [switch]$Help
)

if ($Help) {
    Write-Host @"
Job Application Assistant Installation Script for Windows

Usage: .\install.ps1 [OPTIONS]

Options:
  -SkipOllama    Skip Ollama installation
  -SkipPython    Skip Python environment setup
  -Help          Show this help message

Examples:
  .\install.ps1                 # Full installation
  .\install.ps1 -SkipOllama     # Skip Ollama installation
"@
    exit 0
}

# Colors for output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

Write-Host "🚀 Job Application Assistant Installation Script" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Check if running as administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (Test-Administrator) {
    Write-Warning "Running as Administrator. This is not required for most operations."
}

# Check system requirements
function Test-Requirements {
    Write-Status "Checking system requirements..."
    
    # Check for Docker Desktop
    try {
        $dockerVersion = docker --version
        Write-Status "Docker found: $dockerVersion"
    } catch {
        Write-Error "Docker is not installed or not in PATH."
        Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
        Write-Host "After installation, restart your computer and run this script again." -ForegroundColor Yellow
        exit 1
    }
    
    # Check for Docker Compose
    try {
        docker-compose --version | Out-Null
        Write-Status "Docker Compose found"
    } catch {
        try {
            docker compose version | Out-Null
            Write-Status "Docker Compose (plugin) found"
        } catch {
            Write-Error "Docker Compose is not available."
            exit 1
        }
    }
    
    # Check for Python (optional)
    try {
        $pythonVersion = python --version 2>$null
        if ($pythonVersion) {
            Write-Status "Python found: $pythonVersion"
        } else {
            $python3Version = python3 --version 2>$null
            if ($python3Version) {
                Write-Status "Python found: $python3Version"
            }
        }
    } catch {
        Write-Warning "Python not found in PATH. Python environment setup will be skipped."
    }
    
    Write-Success "System requirements check passed!"
}

# Setup environment
function Initialize-Environment {
    Write-Status "Setting up environment..."
    
    # Create .env file if it doesn't exist
    if (-not (Test-Path ".env")) {
        Write-Status "Creating .env file from template..."
        Copy-Item ".env.example" ".env"
        Write-Warning "Please edit .env file to add your API keys (optional for local-only usage)"
    }
    
    # Create data directories
    $directories = @("data", "logs", "uploads")
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir | Out-Null
            Write-Status "Created directory: $dir"
        }
    }
    
    Write-Success "Environment setup completed!"
}

# Install Ollama (optional)
function Install-Ollama {
    if ($SkipOllama) {
        Write-Status "Skipping Ollama installation as requested."
        return
    }
    
    $response = Read-Host "Would you like to install Ollama for local LLM support? (y/N)"
    
    if ($response -match "^[Yy]$") {
        Write-Status "Installing Ollama..."
        
        # Download and install Ollama
        $ollamaUrl = "https://github.com/ollama/ollama/releases/latest/download/OllamaSetup.exe"
        $installerPath = "$env:TEMP\OllamaSetup.exe"
        
        try {
            Write-Status "Downloading Ollama installer..."
            Invoke-WebRequest -Uri $ollamaUrl -OutFile $installerPath
            
            Write-Status "Running Ollama installer..."
            Start-Process -FilePath $installerPath -Wait
            
            Write-Success "Ollama installed successfully!"
            
            # Wait for Ollama to be available
            Write-Status "Waiting for Ollama service to start..."
            Start-Sleep -Seconds 10
            
            # Pull recommended models
            $modelResponse = Read-Host "Would you like to download recommended models? (llama3.1:8b, qwen2.5:7b) (y/N)"
            
            if ($modelResponse -match "^[Yy]$") {
                Write-Status "Downloading models (this may take a while)..."
                try {
                    ollama pull llama3.1:8b
                    ollama pull qwen2.5:7b
                    Write-Success "Models downloaded successfully!"
                } catch {
                    Write-Warning "Failed to download models. You can download them later using: ollama pull <model-name>"
                }
            }
        } catch {
            Write-Error "Failed to install Ollama: $_"
        } finally {
            # Clean up installer
            if (Test-Path $installerPath) {
                Remove-Item $installerPath
            }
        }
    }
}

# Setup Docker
function Initialize-Docker {
    Write-Status "Setting up Docker containers..."
    
    try {
        Write-Status "Building Docker image..."
        docker-compose build
        Write-Success "Docker setup completed!"
    } catch {
        Write-Error "Failed to build Docker image: $_"
        exit 1
    }
}

# Setup Python environment (alternative to Docker)
function Initialize-Python {
    if ($SkipPython) {
        Write-Status "Skipping Python environment setup as requested."
        return
    }
    
    $response = Read-Host "Would you like to set up Python environment as well? (y/N)"
    
    if ($response -match "^[Yy]$") {
        Write-Status "Setting up Python virtual environment..."
        
        try {
            # Try python first, then python3
            $pythonCmd = "python"
            try {
                & python --version | Out-Null
            } catch {
                $pythonCmd = "python3"
                & python3 --version | Out-Null
            }
            
            # Create virtual environment
            & $pythonCmd -m venv venv
            
            # Activate virtual environment and install dependencies
            $activateScript = "venv\Scripts\Activate.ps1"
            if (Test-Path $activateScript) {
                & $activateScript
                pip install --upgrade pip
                pip install -r requirements.txt
                Write-Success "Python environment setup completed!"
                Write-Status "To activate the environment, run: venv\Scripts\Activate.ps1"
            } else {
                Write-Error "Failed to create virtual environment."
            }
        } catch {
            Write-Error "Failed to setup Python environment: $_"
            Write-Warning "You can set it up manually later if needed."
        }
    }
}

# Main installation function
function Start-Installation {
    Write-Status "Starting installation process..."
    
    Test-Requirements
    Initialize-Environment
    Install-Ollama
    Initialize-Docker
    Initialize-Python
    
    Write-Host ""
    Write-Success "Installation completed successfully! 🎉"
    Write-Host ""
    Write-Host "Quick Start:" -ForegroundColor Cyan
    Write-Host "  1. Docker (recommended): docker-compose up -d"
    Write-Host "  2. Python: venv\Scripts\Activate.ps1 && streamlit run job_application_assistant\web\app.py"
    Write-Host "  3. CLI: python -m job_application_assistant.cli.main --help"
    Write-Host ""
    Write-Host "Access the web interface at: http://localhost:8501"
    Write-Host ""
    Write-Host "For more information, see README.md"
}

# Run main installation
try {
    Start-Installation
} catch {
    Write-Error "Installation failed: $_"
    exit 1
}
