<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Job Application Assistant - Copilot Instructions

This is a Python project that builds a job application and interview preparation assistant using LangChain, LangSmith, and LangGraph.

## Key Technologies and Patterns

- **LangChain**: Use for building chains and prompts
- **LangGraph**: Use for creating complex agent workflows and state management
- **LangSmith**: Use for monitoring and debugging agent interactions
- **Pydantic**: Use for data validation and settings management
- **Rich/Typer**: Use for beautiful CLI interfaces
- **Streamlit**: Use for web interface components

## Code Style Guidelines

- Follow Python PEP 8 standards
- Use type hints consistently
- Create modular, reusable components
- Implement proper error handling
- Add comprehensive docstrings
- Use async/await patterns where appropriate
- Implement proper logging

## Architecture Patterns

- Use dependency injection for components
- Implement the Repository pattern for data access
- Use Factory pattern for creating different types of agents
- Implement Strategy pattern for different job application strategies
- Use Observer pattern for monitoring agent activities

## Agent Design Principles

- Create stateful agents using LangGraph's StateGraph
- Use tool calling for external integrations
- Implement proper memory management
- Design for scalability and maintainability
- Use structured outputs with Pydantic models

## Security Considerations

- Store API keys in environment variables
- Validate all external inputs
- Implement rate limiting for API calls
- Use secure methods for file handling
- Implement proper authentication for web interface
