#!/usr/bin/env python3
"""
Test script to verify GUI auto-calculation functionality
"""

import tkinter as tk
from tkinter import ttk
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gui_calculator import FinancialCalculatorGUI

def test_auto_calculation():
    """Test the auto-calculation functionality"""
    
    print("Testing GUI auto-calculation...")
    
    # Create a simple test window
    root = tk.Tk()
    root.title("Auto-Calculation Test")
    root.geometry("800x600")
    
    # Create the GUI
    app = FinancialCalculatorGUI(root)
    
    print("GUI created successfully")
    print("Testing parameter change detection...")
    
    # Test changing a parameter
    if 'starting_magi' in app.widgets:
        widget = app.widgets['starting_magi']
        print(f"Current starting_magi value: {widget.get()}")
        
        # Change the value
        widget.delete(0, tk.END)
        widget.insert(0, "150000")
        print(f"Changed starting_magi to: {widget.get()}")
        
        # Trigger the change event
        app.on_parameter_change()
        print("Parameter change event triggered")
    
    print("Test completed. Check the GUI for updates.")
    
    # Run the GUI
    root.mainloop()

if __name__ == "__main__":
    test_auto_calculation() 