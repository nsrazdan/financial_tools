#!/usr/bin/env python3
"""
GUI version of the Financial Tools calculator
Mimics the CLI interface with a graphical user interface
"""

import tkinter as tk
from tkinter import ttk
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ui.savings_calculator_tab import SavingsCalculatorTab

class FinancialCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Tools Calculator")
        self.root.geometry("1400x800")
        self.root.resizable(True, True)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="Financial Tools Calculator", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create Savings Calculator tab
        self.create_savings_calculator_tab()
        
        # Create Income Debt Calculator tab
        self.create_income_debt_calculator_tab()
        
    def create_savings_calculator_tab(self):
        """Create the Savings Calculator tab with all existing functionality"""
        self.savings_tab = SavingsCalculatorTab(self.notebook)
        
    def create_income_debt_calculator_tab(self):
        """Create the Income Debt Calculator tab"""
        income_debt_frame = ttk.Frame(self.notebook)
        self.notebook.add(income_debt_frame, text="Income Debt Calculator")
        
        # Add a simple label for now (blank tab as requested)
        label = ttk.Label(income_debt_frame, text="Income Debt Calculator - Coming Soon", 
                         font=("Arial", 14))
        label.pack(expand=True)

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme
    
    # Create and run the application
    app = FinancialCalculatorGUI(root)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main() 