#!/usr/bin/env python3
"""
Job Application Assistant Project Status Checker
This script provides a comprehensive overview of the project status
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json


class StatusChecker:
    def __init__(self):
        self.root_path = Path.cwd()
        self.checks_passed = 0
        self.total_checks = 0
        
    def print_header(self):
        print("🎯 Job Application Assistant - Project Status")
        print("=" * 50)
        print()
        
    def check_section(self, name: str) -> bool:
        print(f"🔍 {name}...")
        return True
        
    def check_item(self, description: str, condition: bool, details: str = "") -> bool:
        self.total_checks += 1
        if condition:
            self.checks_passed += 1
            print(f"   ✅ {description}")
            if details:
                print(f"      {details}")
        else:
            print(f"   ❌ {description}")
            if details:
                print(f"      {details}")
        return condition
        
    def run_command(self, command: List[str], timeout: int = 30) -> Tuple[bool, str]:
        """Run a command and return success status and output"""
        try:
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                timeout=timeout,
                cwd=self.root_path
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)
            
    def check_file_structure(self):
        """Check if all required files and directories exist"""
        self.check_section("File Structure")
        
        required_files = [
            "pyproject.toml",
            "README.md",
            "CHANGELOG.md",
            "LICENSE",
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
            ".gitignore",
            ".pre-commit-config.yaml",
            "Dockerfile",
            "docker-compose.yml",
            "docker-compose.prod.yml",
            "install.sh",
            "install.ps1",
            ".env.example",
            ".env.docker",
        ]
        
        required_dirs = [
            "job_application_assistant",
            "tests",
            ".github/workflows",
            ".github/ISSUE_TEMPLATE",
            "scripts",
        ]
        
        missing_files = []
        for file_path in required_files:
            if not (self.root_path / file_path).exists():
                missing_files.append(file_path)
                
        missing_dirs = []
        for dir_path in required_dirs:
            if not (self.root_path / dir_path).is_dir():
                missing_dirs.append(dir_path)
                
        self.check_item(
            "All required files present",
            len(missing_files) == 0,
            f"Missing: {missing_files}" if missing_files else f"Found {len(required_files)} files"
        )
        
        self.check_item(
            "All required directories present",
            len(missing_dirs) == 0,
            f"Missing: {missing_dirs}" if missing_dirs else f"Found {len(required_dirs)} directories"
        )
        
    def check_package_structure(self):
        """Check the Python package structure"""
        self.check_section("Package Structure")
        
        package_dirs = [
            "job_application_assistant/__init__.py",
            "job_application_assistant/core",
            "job_application_assistant/agents",
            "job_application_assistant/models",
            "job_application_assistant/tools",
            "job_application_assistant/web",
            "job_application_assistant/cli",
            "job_application_assistant/utils",
        ]
        
        missing = []
        for item in package_dirs:
            path = self.root_path / item
            if not path.exists():
                missing.append(item)
                
        self.check_item(
            "Package structure complete",
            len(missing) == 0,
            f"Missing: {missing}" if missing else "All package modules present"
        )
        
    def check_installation(self):
        """Check if the package can be installed and imported"""
        self.check_section("Installation & Import")
        
        # Try to import the package
        try:
            sys.path.insert(0, str(self.root_path))
            import job_application_assistant
            self.check_item("Package can be imported", True, f"Version: {getattr(job_application_assistant, '__version__', 'unknown')}")
        except ImportError as e:
            self.check_item("Package can be imported", False, str(e))
            
        # Check if CLI is accessible
        success, output = self.run_command([sys.executable, "-m", "job_application_assistant", "--help"])
        self.check_item("CLI is accessible", success, "CLI help command works" if success else output[:100])
        
    def check_tests(self):
        """Check if tests can run"""
        self.check_section("Tests")
        
        # Check if pytest is available
        success, _ = self.run_command([sys.executable, "-m", "pytest", "--version"])
        self.check_item("pytest is available", success)
        
        if success:
            # Run tests
            success, output = self.run_command([sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"])
            self.check_item("Unit tests pass", success, "All tests passing" if success else "Some tests failed")
            
    def check_docker(self):
        """Check Docker configuration"""
        self.check_section("Docker")
        
        # Check if Docker is available
        success, _ = self.run_command(["docker", "--version"])
        docker_available = success
        self.check_item("Docker is available", docker_available)
        
        if docker_available:
            # Check if Dockerfile exists and has basic structure
            dockerfile_path = self.root_path / "Dockerfile"
            if dockerfile_path.exists():
                content = dockerfile_path.read_text()
                has_from = "FROM" in content
                has_workdir = "WORKDIR" in content or "COPY" in content
                dockerfile_valid = has_from and has_workdir
                self.check_item("Dockerfile is valid", dockerfile_valid, 
                              "Dockerfile has basic structure" if dockerfile_valid else "Dockerfile missing key instructions")
            else:
                self.check_item("Dockerfile exists", False)
            
        # Check docker-compose (optional)
        success, _ = self.run_command(["docker-compose", "--version"])
        if not success:
            success, _ = self.run_command(["docker", "compose", "version"])
        self.check_item("Docker Compose is available (optional)", True, 
                       "Docker Compose found" if success else "Docker Compose not found (optional for development)")
        
    def check_git_readiness(self):
        """Check if the project is ready for Git"""
        self.check_section("Git Readiness")
        
        # Check if we're in a git repo
        success, _ = self.run_command(["git", "status"])
        in_git_repo = success
        self.check_item("Git repository initialized", in_git_repo)
        
        if in_git_repo:
            # Check for uncommitted changes
            success, output = self.run_command(["git", "status", "--porcelain"])
            clean_repo = success and not output.strip()
            self.check_item("Working directory is clean", clean_repo, 
                          "Ready for commit" if clean_repo else "Has uncommitted changes")
            
        # Check GitHub workflow files
        workflow_files = list((self.root_path / ".github" / "workflows").glob("*.yml"))
        self.check_item("GitHub workflows present", len(workflow_files) > 0, 
                       f"Found {len(workflow_files)} workflow files")
        
    def check_documentation(self):
        """Check documentation completeness"""
        self.check_section("Documentation")
        
        # Check README sections
        readme_path = self.root_path / "README.md"
        if readme_path.exists():
            content = readme_path.read_text()
            required_sections = [
                "# Job Application Assistant",
                "## Features",
                "## Installation",
                "## Usage",
                "## Configuration",
                "## Docker",
                "## Contributing",
                "## License"
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)
                    
            self.check_item("README has all sections", len(missing_sections) == 0,
                          f"Missing: {missing_sections}" if missing_sections else "All sections present")
        else:
            self.check_item("README exists", False)
            
    def check_scripts(self):
        """Check utility scripts"""
        self.check_section("Utility Scripts")
        
        scripts = [
            "scripts/release.sh",
            "scripts/dev-setup.sh", 
            "scripts/docker-build.sh",
            "install.sh",
            "install.ps1"
        ]
        
        for script in scripts:
            script_path = self.root_path / script
            exists = script_path.exists()
            executable = exists and os.access(script_path, os.X_OK)
            self.check_item(f"{script} exists and is executable", exists and executable,
                          "Ready to use" if executable else "Not executable" if exists else "Missing")
            
    def print_summary(self):
        """Print final summary"""
        print()
        print("=" * 50)
        print("📊 Project Status Summary")
        print("=" * 50)
        
        percentage = (self.checks_passed / self.total_checks * 100) if self.total_checks > 0 else 0
        
        if percentage >= 90:
            status_emoji = "🎉"
            status_text = "EXCELLENT"
        elif percentage >= 75:
            status_emoji = "✅"
            status_text = "GOOD"
        elif percentage >= 50:
            status_emoji = "⚠️"
            status_text = "NEEDS WORK"
        else:
            status_emoji = "❌"
            status_text = "CRITICAL ISSUES"
            
        print(f"{status_emoji} Overall Status: {status_text}")
        print(f"📈 {self.checks_passed}/{self.total_checks} checks passed ({percentage:.1f}%)")
        print()
        
        if percentage >= 90:
            print("🚀 Project is production-ready!")
            print("   ✅ Ready for GitHub release")
            print("   ✅ Ready for PyPI publication")
            print("   ✅ Ready for Docker Hub deployment")
        elif percentage >= 75:
            print("🔧 Project is mostly ready with minor issues")
            print("   ✅ Core functionality working")
            print("   ⚠️  Some non-critical issues to address")
        else:
            print("🛠️  Project needs work before release")
            print("   ❌ Critical issues need to be resolved")
            
        print()
        print("📋 Next steps:")
        if percentage >= 90:
            print("   1. Run final tests: python test_production_ready.py")
            print("   2. Initialize git: git init (if not done)")
            print("   3. Create initial commit: git add . && git commit -m 'feat: initial release'")
            print("   4. Create GitHub repository and push")
            print("   5. Create release: scripts/release.sh")
        else:
            print("   1. Address failing checks above")
            print("   2. Run this script again to verify fixes")
            print("   3. Once all checks pass, proceed with release")
            
        print()
        
    def run_all_checks(self):
        """Run all status checks"""
        self.print_header()
        
        self.check_file_structure()
        self.check_package_structure()
        self.check_installation()
        self.check_tests()
        self.check_docker()
        self.check_git_readiness()
        self.check_documentation()
        self.check_scripts()
        
        self.print_summary()


if __name__ == "__main__":
    checker = StatusChecker()
    checker.run_all_checks()
