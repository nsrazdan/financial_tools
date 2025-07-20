#!/usr/bin/env python3
"""
Test runner script for Financial Tools
Runs all unit tests and provides coverage reports
"""

import sys
import subprocess
import os
from pathlib import Path

def run_unittest_tests():
    """Run tests using unittest"""
    print("🧪 Running tests with unittest...")
    print("=" * 50)
    
    test_files = [
        "test/test_ira_calculator.py",
        "test/test_401k_calculator.py",
        "test/test_gui.py"
    ]
    
    all_passed = True
    
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"\n📋 Running {test_file}...")
            try:
                result = subprocess.run([sys.executable, "-m", "unittest", test_file], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {test_file} passed")
                else:
                    print(f"❌ {test_file} failed")
                    print(result.stdout)
                    print(result.stderr)
                    all_passed = False
            except Exception as e:
                print(f"❌ Error running {test_file}: {e}")
                all_passed = False
        else:
            print(f"⚠️  {test_file} not found")
    
    return all_passed

def run_pytest_tests():
    """Run tests using pytest"""
    print("\n🧪 Running tests with pytest...")
    print("=" * 50)
    
    try:
        # Run pytest with coverage
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "--cov=modules", 
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov",
            "-v"
        ], capture_output=False)
        
        if result.returncode == 0:
            print("\n✅ All pytest tests passed!")
            return True
        else:
            print("\n❌ Some pytest tests failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error running pytest: {e}")
        return False

def run_specific_test(test_name):
    """Run a specific test file"""
    test_file = f"test/test_{test_name}.py"
    
    if not Path(test_file).exists():
        print(f"❌ Test file {test_file} not found")
        return False
    
    print(f"🧪 Running specific test: {test_file}")
    print("=" * 50)
    
    try:
        # Try pytest first
        result = subprocess.run([
            sys.executable, "-m", "pytest", test_file, "-v"
        ], capture_output=False)
        
        if result.returncode == 0:
            print(f"✅ {test_file} passed with pytest")
            return True
        else:
            print(f"❌ {test_file} failed with pytest")
            return False
            
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return False

def show_coverage_report():
    """Show coverage report if available"""
    coverage_file = Path("htmlcov/index.html")
    if coverage_file.exists():
        print(f"\n📊 Coverage report available at: {coverage_file.absolute()}")
        print("   Open this file in your browser to view detailed coverage")

def main():
    """Main test runner function"""
    print("🚀 Financial Tools Test Runner")
    print("=" * 50)
    
    # Check if specific test was requested
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
    else:
        # Run all tests
        print("Running all tests...")
        
        # Run unittest tests
        unittest_success = run_unittest_tests()
        
        # Run pytest tests
        pytest_success = run_pytest_tests()
        
        success = unittest_success and pytest_success
    
    # Show coverage report
    show_coverage_report()
    
    # Final result
    if success:
        print("\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 