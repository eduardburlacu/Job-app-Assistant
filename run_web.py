#!/usr/bin/env python3
"""Entry point for running the Streamlit web application."""

import sys
import subprocess
from pathlib import Path

def main():
    """Run the Streamlit web application."""
    # Get the path to the web app
    project_root = Path(__file__).parent
    app_path = project_root / "job_application_assistant" / "web" / "app.py"
    
    if not app_path.exists():
        print(f"Error: Web app not found at {app_path}")
        sys.exit(1)
    
    # Run streamlit
    try:
        cmd = ["streamlit", "run", str(app_path)]
        print(f"Starting web application: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running web app: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Streamlit not found. Please install it with: pip install streamlit")
        sys.exit(1)

if __name__ == "__main__":
    main()
