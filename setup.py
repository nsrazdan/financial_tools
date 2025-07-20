#!/usr/bin/env python3
"""
Setup script for Financial Tools project
Handles dependency installation and project setup
"""

import os
import sys
import subprocess
import pkg_resources
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible (3.7+)"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def read_requirements():
    """Read requirements from requirements.txt"""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ Error: requirements.txt not found")
        return []
    
    with open(requirements_file, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return requirements

def get_installed_packages():
    """Get list of installed packages"""
    return {pkg.key for pkg in pkg_resources.working_set}

def install_package(package):
    """Install a single package"""
    try:
        print(f"📦 Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def upgrade_pip():
    """Upgrade pip to latest version"""
    try:
        print("🔄 Upgrading pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ Pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Could not upgrade pip: {e}")
        return False

def install_requirements(requirements):
    """Install all requirements"""
    if not requirements:
        print("ℹ️  No requirements to install")
        return True
    
    print(f"\n📋 Installing {len(requirements)} dependencies...")
    print("=" * 50)
    
    installed_packages = get_installed_packages()
    failed_installations = []
    
    for requirement in requirements:
        # Extract package name (remove version specifiers)
        package_name = requirement.split('>=')[0].split('==')[0].split('<=')[0].split('~=')[0].split('!=')[0]
        
        if package_name.lower() in installed_packages:
            print(f"✅ {package_name} already installed")
        else:
            if not install_package(requirement):
                failed_installations.append(requirement)
    
    if failed_installations:
        print(f"\n❌ Failed to install {len(failed_installations)} packages:")
        for pkg in failed_installations:
            print(f"   - {pkg}")
        return False
    
    print(f"\n✅ All dependencies installed successfully!")
    return True

def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        "modules",
        "modules/masters", 
        "scripts",
        "data",
        "logs"
    ]
    
    print("\n📁 Creating directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def run_tests():
    """Run basic tests to verify installation"""
    print("\n🧪 Running basic tests...")
    
    try:
        # Test importing main modules
        sys.path.insert(0, str(Path.cwd()))
        
        from modules.masters.calc_ira_savings import total_ira_contributions_over_years
        from modules.masters.calc_401k_savings import total_401k_contributions_over_years
        from tabulate import tabulate
        
        print("✅ All modules imported successfully")
        
        # Test basic calculation
        result = total_ira_contributions_over_years(
            start_year=2025,
            years=1,
            age=25,
            filing_status='single',
            starting_magi=50000,
            return_details=False
        )
        print(f"✅ Basic calculation test passed: ${result:,.2f}")
        
        # Test GUI import
        try:
            import tkinter
            print("✅ Tkinter available for GUI")
        except ImportError:
            print("⚠️  Tkinter not available - GUI will not work")
        
        # Test pytest import
        try:
            import pytest
            print("✅ Pytest available for testing")
        except ImportError:
            print("⚠️  Pytest not available - testing will not work")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Calculation test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Financial Tools Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Upgrade pip
    upgrade_pip()
    
    # Read requirements
    requirements = read_requirements()
    
    # Install requirements
    if not install_requirements(requirements):
        print("\n❌ Setup failed due to dependency installation errors")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Run tests
    if not run_tests():
        print("\n⚠️  Setup completed with warnings (some tests failed)")
        print("   You may need to check your installation manually")
    else:
        print("\n🎉 Setup completed successfully!")
    
    print("\n📖 Next steps:")
    print("   1. Run the calculator: python3 scripts/run_masters_calc.py")
    print("   2. For detailed output: python3 scripts/run_masters_calc.py --verbose")
    print("   3. For interactive mode: python3 scripts/run_masters_calc.py --interactive")
    print("   4. Launch GUI: python3 run_gui.py")
    print("\n📚 Documentation: Check README.md for more information")

if __name__ == "__main__":
    main() 