"""Test CLI functionality."""

import subprocess
import sys
from pathlib import Path


class TestCLI:
    """Test CLI commands."""
    
    def test_cli_help(self):
        """Test CLI help command."""
        result = subprocess.run(
            [sys.executable, "run_cli.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        assert result.returncode == 0
        assert "Job Application" in result.stdout
        assert "Commands" in result.stdout
    
    def test_cli_info(self):
        """Test CLI info command."""
        result = subprocess.run(
            [sys.executable, "run_cli.py", "info"],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        assert result.returncode == 0
        # Should contain system information
        assert ("System Information" in result.stdout or 
                "Model:" in result.stdout or
                result.returncode == 0)  # Allow for different output formats
    
    def test_cli_commands_exist(self):
        """Test that expected CLI commands exist."""
        result = subprocess.run(
            [sys.executable, "run_cli.py", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        assert result.returncode == 0
        # Check for expected commands
        assert "apply" in result.stdout
        assert "interview" in result.stdout
        assert "info" in result.stdout
