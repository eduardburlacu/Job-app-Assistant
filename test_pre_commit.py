#!/usr/bin/env python3
"""Pre-commit verification script for GitHub repository."""

import sys
import subprocess
import json
from pathlib import Path
from typing import List, Tuple, Dict

def run_command(cmd: List[str], timeout: int = 60) -> Tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 124, "", f"Command timed out after {timeout}s"
    except Exception as e:
        return 1, "", str(e)

def check_github_files():
    """Check that all required GitHub files are present."""
    print("📁 Checking GitHub repository files...")
    
    required_files = [
        ".github/workflows/ci.yml",
        ".github/workflows/release.yml",
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/feature_request.yml",
        ".github/ISSUE_TEMPLATE/question.yml",
        ".github/pull_request_template.md",
        ".gitignore",
        ".pre-commit-config.yaml",
        "CODE_OF_CONDUCT.md",
        "SECURITY.md",
        "README.md",
        "LICENSE",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing GitHub files: {missing_files}")
        return False
    else:
        print(f"✅ All {len(required_files)} GitHub files present")
        return True

def check_code_quality():
    """Run code quality checks."""
    print("\n🔍 Running code quality checks...")
    
    checks = [
        (["ruff", "check", "."], "Ruff linting"),
        (["ruff", "format", ".", "--check"], "Ruff formatting"),
        (["mypy", "job_application_assistant/", "--ignore-missing-imports"], "MyPy type checking"),
        (["bandit", "-r", "job_application_assistant/", "-f", "json"], "Bandit security scan"),
    ]
    
    all_passed = True
    
    for cmd, name in checks:
        print(f"  Running {name}...")
        exit_code, stdout, stderr = run_command(cmd, timeout=120)
        
        if exit_code == 0:
            print(f"  ✅ {name} passed")
        else:
            print(f"  ❌ {name} failed")
            if stdout:
                print(f"     stdout: {stdout[:200]}...")
            if stderr:
                print(f"     stderr: {stderr[:200]}...")
            all_passed = False
    
    return all_passed

def check_tests():
    """Run test suite."""
    print("\n🧪 Running test suite...")
    
    test_commands = [
        (["python", "test_installation.py"], "Installation test"),
        (["python", "test_functionality.py"], "Functionality test"),
        (["python", "test_production_ready.py"], "Production readiness test"),
    ]
    
    # Try to run pytest if available
    if Path("tests").exists():
        test_commands.append((["python", "-m", "pytest", "tests/", "-v"], "Unit tests"))
    
    all_passed = True
    
    for cmd, name in test_commands:
        print(f"  Running {name}...")
        exit_code, stdout, stderr = run_command(cmd, timeout=180)
        
        if exit_code == 0:
            print(f"  ✅ {name} passed")
        else:
            print(f"  ❌ {name} failed")
            if stderr:
                print(f"     Error: {stderr[:300]}")
            all_passed = False
    
    return all_passed

def check_docker():
    """Check Docker configuration."""
    print("\n🐳 Checking Docker configuration...")
    
    docker_files = ["Dockerfile", "docker-compose.yml", "docker-compose.prod.yml"]
    missing_files = []
    
    for file_path in docker_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing Docker files: {missing_files}")
        return False
    
    # Try to build Docker image
    print("  Testing Docker build...")
    exit_code, stdout, stderr = run_command(
        ["docker", "build", "-t", "job-assistant-test", "."],
        timeout=300
    )
    
    if exit_code == 0:
        print("  ✅ Docker build successful")
        # Clean up
        subprocess.run(["docker", "rmi", "job-assistant-test"], capture_output=True)
        return True
    else:
        # Docker might not be available, which is OK for CI
        if "Cannot connect to the Docker daemon" in stderr:
            print("  ⚠️  Docker daemon not running (OK for CI)")
            return True
        else:
            print(f"  ❌ Docker build failed: {stderr[:200]}")
            return False

def check_package_build():
    """Check that package can be built."""
    print("\n📦 Checking package build...")
    
    # Install build if not available
    exit_code, _, _ = run_command(["python", "-m", "pip", "install", "build"])
    if exit_code != 0:
        print("  ❌ Failed to install build package")
        return False
    
    # Build package
    exit_code, stdout, stderr = run_command(["python", "-m", "build"], timeout=120)
    
    if exit_code == 0:
        print("  ✅ Package build successful")
        # Check if dist files were created
        dist_files = list(Path("dist").glob("*")) if Path("dist").exists() else []
        if dist_files:
            print(f"  📦 Created {len(dist_files)} distribution files")
        return True
    else:
        print(f"  ❌ Package build failed: {stderr[:200]}")
        return False

def generate_pre_commit_summary() -> Dict:
    """Generate a summary of the pre-commit checks."""
    try:
        git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()[:8]
    except:
        git_commit = "not-git"
    
    try:
        git_branch = subprocess.check_output(["git", "branch", "--show-current"], stderr=subprocess.DEVNULL).decode().strip()
    except:
        git_branch = "not-git"
    
    try:
        timestamp = subprocess.check_output(["date", "-Iseconds"], stderr=subprocess.DEVNULL).decode().strip()
    except:
        import datetime
        timestamp = datetime.datetime.now().isoformat()
    
    return {
        "timestamp": timestamp,
        "git_commit": git_commit,
        "git_branch": git_branch,
        "python_version": sys.version.split()[0],
        "platform": sys.platform,
    }

def main():
    """Run all pre-commit checks."""
    print("🎯 Job Application Assistant - Pre-Commit Verification")
    print("=" * 60)
    
    summary = generate_pre_commit_summary()
    print(f"📊 Environment: Python {summary['python_version']} on {summary['platform']}")
    print(f"🌿 Branch: {summary['git_branch']} ({summary['git_commit']})")
    print(f"🕐 Time: {summary['timestamp']}")
    print()
    
    checks = [
        ("GitHub Files", check_github_files),
        ("Code Quality", check_code_quality),
        ("Tests", check_tests),
        ("Docker", check_docker),
        ("Package Build", check_package_build),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        print(f"\n🔍 {check_name}...")
        try:
            success = check_func()
            results.append((check_name, success))
        except Exception as e:
            print(f"❌ {check_name} failed with exception: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Pre-Commit Verification Summary:")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for check_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} {check_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 ALL CHECKS PASSED! Ready for commit to GitHub! 🚀")
        print("\n📋 Next steps:")
        print("   1. git add .")
        print("   2. git commit -m 'feat: production-ready job application assistant'")
        print("   3. git push origin main")
        print("   4. Create GitHub release with tag v1.0.0")
        return 0
    else:
        print(f"\n❌ {total - passed} check(s) failed. Fix issues before committing.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
