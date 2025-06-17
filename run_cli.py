#!/usr/bin/env python3
"""Entry point for running the CLI application."""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Run the CLI application."""
    try:
        from job_application_assistant.cli.main import app
        app()
    except ImportError as e:
        print(f"Error importing CLI app: {e}")
        print("Please make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error running CLI app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
