"""Entry point for running the job application assistant as a module."""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    from job_application_assistant.cli.main import app
    app()
