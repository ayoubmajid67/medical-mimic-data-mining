#!/usr/bin/env python
"""Run all tests with coverage report."""
import subprocess
import sys


def main():
    """Run pytest with coverage."""
    print("Running Bronze Layer Tests...")
    print("=" * 60)
    
    cmd = [
        "pytest",
        "tests/",
        "-v",
        "--cov=app",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("Coverage report: htmlcov/index.html")
    else:
        print("\n" + "=" * 60)
        print("✗ Some tests failed")
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
