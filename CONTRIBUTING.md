# Contributing to Job Application Assistant

Thank you for your interest in contributing to the Job Application Assistant! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:
- Be respectful and inclusive
- Use welcoming and inclusive language
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in our issue tracker
2. If not, create a new issue with:
   - Clear description of the problem or feature request
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/job-application-assistant.git
   cd job-application-assistant
   ```

2. **Set up the development environment**
   ```bash
   # Install in development mode
   pip install -e .
   
   # Install development dependencies
   pip install -e ".[dev]"
   ```

3. **Set up pre-commit hooks** (optional but recommended)
   ```bash
   pre-commit install
   ```

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed
   - Ensure all tests pass

3. **Test your changes**
   ```bash
   # Run installation test
   python test_installation.py
   
   # Run functionality test
   python test_functionality.py
   
   # Run any additional tests
   pytest tests/ (if test directory exists)
   ```

4. **Format your code**
   ```bash
   # Format with Black
   black job_application_assistant/
   
   # Lint with Ruff
   ruff check job_application_assistant/
   
   # Type check with MyPy
   mypy job_application_assistant/
   ```

### Submitting Changes

1. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```
   
   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `style:` for formatting changes
   - `refactor:` for code refactoring
   - `test:` for adding tests
   - `chore:` for maintenance tasks

2. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Include screenshots for UI changes
   - Ensure all checks pass

## Development Guidelines

### Code Style

- Follow PEP 8 standards
- Use type hints consistently
- Write clear, descriptive docstrings
- Keep functions and classes focused and single-purpose
- Use meaningful variable and function names

### Architecture Principles

- **Modularity**: Create reusable, independent components
- **Dependency Injection**: Use dependency injection for better testability
- **Error Handling**: Implement comprehensive error handling
- **Logging**: Add appropriate logging throughout the code
- **Configuration**: Use environment variables and configuration files
- **Privacy**: Ensure all operations remain local and private

### Testing

- Write tests for new functionality
- Ensure existing tests continue to pass
- Test both happy path and error scenarios
- Include integration tests where appropriate

### Documentation

- Update README.md for new features or installation changes
- Add docstrings to all functions and classes
- Update CHANGELOG.md with your changes
- Include examples in documentation

## Project Structure

```
job_application_assistant/
├── __init__.py              # Package initialization
├── core/                    # Core functionality
│   ├── config.py           # Configuration management
│   ├── exceptions.py       # Custom exceptions
│   ├── llm.py             # LLM management
│   └── logging.py         # Logging setup
├── agents/                  # AI agents
│   ├── job_application_agent.py
│   └── interview_prep_agent.py
├── models/                  # Data models
│   └── data_models.py
├── tools/                   # Utility tools
│   └── document_processor.py
├── web/                     # Web interface
│   └── app.py
├── cli/                     # Command-line interface
│   └── main.py
└── utils/                   # General utilities
    └── streamlit_helpers.py
```

## Release Process

1. Update version numbers in `pyproject.toml` and `__init__.py`
2. Update CHANGELOG.md with new features and changes
3. Create a release PR
4. After approval, tag the release: `git tag v1.x.x`
5. Push tags: `git push --tags`

## Getting Help

- Check the documentation in README.md
- Look through existing issues for similar problems
- Create a new issue with the "question" label
- Join our community discussions (if applicable)

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file (if created)
- Release notes
- Project documentation

Thank you for contributing to make job applications easier for everyone!
