#!/usr/bin/env python3
"""
Launcher script for the Financial Tools GUI
"""

import sys
import os
from pathlib import Path

def main():
    """Launch the GUI calculator"""
    try:
        # Import and run the GUI
        from gui_calculator import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error: Could not import GUI module: {e}")
        print("Make sure you have tkinter installed and are running from the project root.")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 