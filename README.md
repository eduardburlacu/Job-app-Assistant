# Job Application Assistant

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/yourusername/job-application-assistant/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

A comprehensive AI-powered assistant built with LangChain, LangSmith, and LangGraph to help you with job applications and interview preparation.

## Features

- **Job Analysis**: Analyzes job descriptions to understand requirements
- **CV Processing**: Reads and analyzes your CV/resume
- **Social Profile Integration**: Connects with LinkedIn and GitHub profiles
- **Personalized Applications**: Generates tailored motivation letters and cover letters
- **Interview Preparation**: Creates study lists and mock interview questions
- **User-Centric Approach**: Asks for your personal insights and preferences

## Installation

### Option 1: Quick Install (Recommended)

**Linux/macOS:**
```bash
# Download and run the installation script
curl -fsSL https://raw.githubusercontent.com/yourusername/job-application-assistant/main/install.sh | bash
```

**Windows:**
```powershell
# Download and run the installation script
iwr -useb https://raw.githubusercontent.com/yourusername/job-application-assistant/main/install.ps1 | iex
```

### Option 2: Manual Installation

## Setup

1. **Activate Your Conda Environment**:
   ```bash
   conda activate langchainollama
   ```

2. **Install Additional Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   Create a `.env` file in the root directory with:
   ```
   # Local Ollama Configuration
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=gemma:7b  # or deepseek-coder:6.7b or your preferred model
   
   # Optional: LangSmith for monitoring (can be disabled)
   LANGSMITH_API_KEY=your_langsmith_api_key
   LANGSMITH_PROJECT=job-application-assistant
   
   # Social Media Integration (optional)
   LINKEDIN_USERNAME=your_linkedin_username
   LINKEDIN_PASSWORD=your_linkedin_password
   GITHUB_TOKEN=your_github_token
   ```

4. **Verify Ollama Setup** (if not already done):
   ```bash
   # Check if your models are available
   ollama list
   
   # Pull models if needed
   ollama pull gemma:7b
   ollama pull deepseek-coder:6.7b
   ```
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull your preferred model
   ollama pull gemma:7b
   # or
   ollama pull deepseek-coder:6.7b
   
   # Start Ollama service
   ollama serve
   ```

## 🎉 Your Assistant is Ready!

The Job Application & Interview Preparation Assistant is now fully configured and working with your local `langchainollama` conda environment and your local Gemma3 model!

### 🚀 Quick Start

1. **Test your setup** (recommended first step):
   ```bash
   ./demo.sh
   ```

2. **Web Interface** (Recommended):
   ```bash
   cd /Users/edibrlc/projects/assistant_agent
   conda activate langchainollama
   streamlit run src/app.py
   ```
   Then open: http://localhost:8501

3. **Command Line Interface**:
   ```bash
   cd /Users/edibrlc/projects/assistant_agent
   conda activate langchainollama
   python src/main.py apply
   ```

## Testing

The project includes comprehensive test scripts to verify everything works correctly:

#### Installation Test
```bash
python test_installation.py
```
This verifies:
- All modules can be imported correctly
- Configuration loads properly
- LLM manager initializes
- Entry points are accessible

#### Functionality Test
```bash
python test_functionality.py
```
This tests:
- Data models work correctly
- Agent classes can be imported
- Configuration is properly loaded
- Basic object creation and validation

#### Manual Testing

1. **Test CLI Interface**:
   ```bash
   python run_cli.py --help
   python run_cli.py
   ```

2. **Test Web Interface**:
   ```bash
   python run_web.py
   # Then open http://localhost:8501 in your browser
   ```

3. **Test with Docker**:
   ```bash
   docker-compose up
   # Then open http://localhost:8501 in your browser
   ```

This will test both job application generation and interview preparation features.

### 📋 Available Commands

- `apply` - Create job application with personalized documents
- `interview` - Prepare for job interviews
- `info` - Display system information

### 🛠️ What's Working

✅ **Local AI Models**: Using your Gemma3 model via Ollama  
✅ **Conda Environment**: Running in your `langchainollama` environment  
✅ **Web Interface**: Streamlit app with beautiful UI  
✅ **CLI Interface**: Rich command-line interface  
✅ **Document Processing**: CV/resume analysis  
✅ **Job Analysis**: Extract requirements from job postings  
✅ **Content Generation**: Cover letters, motivation letters  
✅ **Interview Prep**: Technical and behavioral questions  

### 🎯 How It Works

1. **Upload your CV** or provide your background information
2. **Add job description** (paste text, URL, or manual entry)
3. **Share your thoughts** about the role and company
4. **Get personalized content**:
   - Tailored cover letters
   - Motivation letters
   - Interview preparation materials
   - Mock questions and study plans
   ```bash
   # CLI Version
   python src/main.py

   # Web Interface
   streamlit run src/app.py
   ```

## Usage

### Job Application Mode
1. Provide job description (URL or text)
2. Upload your CV/resume
3. Share your thoughts about the position
4. Get personalized application materials

### Interview Preparation Mode
1. Input the job details you applied for
2. Get a confidence checklist
3. Practice with mock interview questions
4. Receive personalized study recommendations

## Project Structure

```
assistant_agent/
├── src/
│   ├── agents/          # LangGraph agents
│   ├── chains/          # LangChain chains
│   ├── tools/           # Custom tools
│   ├── utils/           # Utility functions
│   ├── main.py          # CLI application
│   └── app.py           # Streamlit web app
├── data/                # Sample data and templates
├── config/              # Configuration files
└── tests/               # Test files
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Code of conduct
- Development workflow
- Pull request process
- Issue reporting
- Code style guidelines

To get started:

1. Fork the repository
2. Run the development setup: `./scripts/dev-setup.sh`
3. Make your changes
4. Run tests: `python -m pytest tests/`
5. Submit a pull request

## License

MIT License

## Configuration

The assistant uses environment variables for configuration. Create a `.env` file in the project root:

```bash
# Copy the example configuration
cp .env.example .env

# Edit the configuration
nano .env
```

### Key Configuration Options

```bash
# Ollama Settings
JOB_ASSISTANT_OLLAMA_BASE_URL=http://localhost:11434
JOB_ASSISTANT_PRIMARY_MODEL_NAME=llama3.1:8b
JOB_ASSISTANT_FALLBACK_MODEL_NAMES=["gemma2:9b", "qwen2.5:7b"]

# Application Settings
JOB_ASSISTANT_DEBUG=false
JOB_ASSISTANT_LOG_LEVEL=INFO

# Web Interface
JOB_ASSISTANT_STREAMLIT_HOST=localhost
JOB_ASSISTANT_STREAMLIT_PORT=8501
```

## Docker

### Quick Start with Docker

```bash
# Start everything with docker-compose
docker-compose up -d

# The web interface will be available at http://localhost:8501
```

### Manual Docker Build

```bash
# Build the image
docker build -t job-application-assistant .

# Run the container
docker run -p 8501:8501 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 job-application-assistant
```

### Docker Environment Variables

```yaml
environment:
  - OLLAMA_BASE_URL=http://ollama:11434
  - PRIMARY_MODEL_NAME=llama3.1:8b
  - DEBUG=false
```

## Utility Scripts

The project includes several utility scripts to help with development and deployment:

### Development Scripts

- **`check_status.py`** - Comprehensive project status checker
  ```bash
  python check_status.py
  ```

- **`scripts/dev-setup.sh`** - Set up complete development environment
  ```bash
  ./scripts/dev-setup.sh
  ```

### Release Scripts

- **`scripts/release.sh`** - Automated release process
  ```bash
  ./scripts/release.sh [version]
  ```

- **`scripts/docker-build.sh`** - Build and publish Docker images
  ```bash
  ./scripts/docker-build.sh
  ```

### Test Scripts

- **`test_production_ready.py`** - Production readiness checker
- **`test_github_ready.py`** - GitHub publication readiness  
- **`test_installation.py`** - Installation verification
- **`test_functionality.py`** - Core functionality tests

## Troubleshooting

### Common Issues

**1. Ollama Connection Error**
```bash
# Check if Ollama is running
ollama list

# Start Ollama if not running
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

**2. Model Not Found**
```bash
# Install a model
ollama pull llama3.1:8b

# Verify installation
ollama list
```

**3. Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

**4. Permission Errors**
```bash
# Make scripts executable
chmod +x install.sh run_*.py test_*.py
```

**5. Port Already in Use**
```bash
# Kill process using port 8501
lsof -ti:8501 | xargs kill -9

# Or use a different port
export JOB_ASSISTANT_STREAMLIT_PORT=8502
```

### Getting Help

1. Run the diagnostic test: `python test_installation.py`
2. Check the logs in `~/.job_assistant/logs/`
3. Verify configuration with: `python run_cli.py info`
4. Check GitHub issues for known problems
5. Create a new issue with system information and error logs

## 👥 For Maintainers

### Pre-Commit Verification

Before committing to the GitHub repository, run:

```bash
python test_pre_commit.py
```

This verifies:
- All GitHub workflow files are present
- Code quality checks pass (ruff, mypy, bandit)
- All tests pass
- Docker configuration works
- Package can be built

### Release Process

1. **Update version numbers**:
   ```bash
   # Update pyproject.toml
   version = "1.1.0"
   
   # Update __init__.py
   __version__ = "1.1.0"
   ```

2. **Update CHANGELOG.md** with new features and changes

3. **Run pre-commit verification**:
   ```bash
   python test_pre_commit.py
   ```

4. **Commit and tag**:
   ```bash
   git add .
   git commit -m "chore: bump version to 1.1.0"
   git tag v1.1.0
   git push origin main --tags
   ```

5. **GitHub Actions will automatically**:
   - Run CI/CD pipeline
   - Build and publish to PyPI
   - Create GitHub release
   - Build and push Docker images

### Development Workflow

1. **Set up development environment**:
   ```bash
   pip install -e ".[dev]"
   pre-commit install
   ```

2. **Make changes** and ensure tests pass:
   ```bash
   python test_installation.py
   python test_functionality.py
   pytest tests/
   ```

3. **Run quality checks**:
   ```bash
   ruff check .
   ruff format .
   mypy job_application_assistant/
   ```

4. **Create PR** with proper description and tests
