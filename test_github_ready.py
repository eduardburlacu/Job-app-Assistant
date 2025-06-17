#!/usr/bin/env python3
"""Final GitHub readiness check - minimal dependencies."""

import sys
import subprocess
from pathlib import Path

def check_essential_files():
    """Check essential files for GitHub repository."""
    print("📁 Checking essential GitHub files...")
    
    essential_files = [
        "README.md",
        "LICENSE", 
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "SECURITY.md",
        ".gitignore",
        ".github/workflows/ci.yml",
        ".github/workflows/release.yml",
        "Dockerfile",
        "docker-compose.yml",
        "pyproject.toml",
    ]
    
    missing = [f for f in essential_files if not Path(f).exists()]
    
    if missing:
        print(f"❌ Missing files: {missing}")
        return False
    else:
        print(f"✅ All {len(essential_files)} essential files present")
        return True

def check_core_functionality():
    """Check core functionality without dev dependencies."""
    print("\n🧪 Checking core functionality...")
    
    tests = [
        ("python test_installation.py", "Installation test"),
        ("python test_functionality.py", "Functionality test"),
        ("python test_production_ready.py", "Production readiness"),
        ("python run_cli.py --help", "CLI help"),
        ("python run_cli.py info", "CLI info"),
    ]
    
    all_passed = True
    
    for cmd, name in tests:
        try:
            result = subprocess.run(
                cmd.split(),
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print(f"  ✅ {name}")
            else:
                print(f"  ❌ {name} failed")
                all_passed = False
        except Exception as e:
            print(f"  ❌ {name} failed: {e}")
            all_passed = False
    
    return all_passed

def check_package_structure():
    """Check package structure."""
    print("\n📦 Checking package structure...")
    
    required_dirs = [
        "job_application_assistant",
        "job_application_assistant/core",
        "job_application_assistant/agents",
        "job_application_assistant/models",
        "job_application_assistant/tools",
        "job_application_assistant/web",
        "job_application_assistant/cli",
        "job_application_assistant/utils",
    ]
    
    missing = [d for d in required_dirs if not Path(d).exists()]
    
    if missing:
        print(f"❌ Missing directories: {missing}")
        return False
    else:
        print(f"✅ All {len(required_dirs)} package directories present")
        return True

def check_documentation():
    """Check documentation completeness."""
    print("\n📚 Checking documentation...")
    
    try:
        with open("README.md", "r") as f:
            readme = f.read()
        
        required_sections = [
            "# Job Application Assistant",
            "## Features",
            "## Installation",
            "## Usage",
            "## Docker",
            "## Testing",
            "## Troubleshooting"
        ]
        
        missing = [s for s in required_sections if s not in readme]
        
        if missing:
            print(f"❌ Missing README sections: {missing}")
            return False
        else:
            print(f"✅ All required README sections present")
            return True
            
    except Exception as e:
        print(f"❌ Error checking README: {e}")
        return False

def main():
    """Run GitHub readiness check."""
    print("🎯 Job Application Assistant - GitHub Readiness Check")
    print("=" * 60)
    
    checks = [
        ("Essential Files", check_essential_files),
        ("Package Structure", check_package_structure), 
        ("Core Functionality", check_core_functionality),
        ("Documentation", check_documentation),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            success = check_func()
            results.append((check_name, success))
        except Exception as e:
            print(f"❌ {check_name} failed: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 GitHub Readiness Summary:")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for check_name, success in results:
        status = "✅ READY" if success else "❌ NEEDS WORK"
        print(f"   {status} {check_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 GITHUB READY! 🚀")
        print("\n📋 Ready for repository setup:")
        print("   1. Initialize git: git init")
        print("   2. Add files: git add .")
        print("   3. Initial commit: git commit -m 'feat: initial commit - production-ready job application assistant'")
        print("   4. Add remote: git remote add origin <your-repo-url>")
        print("   5. Push: git push -u origin main")
        print("   6. Set up GitHub secrets for CI/CD")
        print("   7. Create first release: git tag v1.0.0 && git push --tags")
        
        print("\n🔧 Recommended GitHub secrets:")
        print("   - PYPI_API_TOKEN (for PyPI publishing)")
        print("   - DOCKERHUB_USERNAME (for Docker Hub)")
        print("   - DOCKERHUB_TOKEN (for Docker Hub)")
        
        return 0
    else:
        print(f"\n❌ {total - passed} check(s) failed. Address issues before GitHub setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
