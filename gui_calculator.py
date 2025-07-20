#!/usr/bin/env python3
"""
GUI version of the Financial Tools calculator
Mimics the CLI interface with a graphical user interface
"""

from sre_parse import IN
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.masters.masters_constants import *
from modules.masters.calc_total_savings import calculate_total_savings

class FinancialCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Tools Calculator")
        self.root.geometry("1400x800")
        self.root.resizable(True, True)
        
        # Default parameter values
        self.default_params = {
            'start_year': START_YEAR,
            'years': YEARS,
            'age': AGE,
            'filing_status': FILING_STATUS,
            'starting_magi': STARTING_MAGI,
            'magi_growth_rate': MAGI_GROWTH_RATE,
            'plan_covered': PLAN_COVERED,
            'stock_market_return': STOCK_MARKET_RETURN,
            'starting_401k_balance': STARTING_401K_BALANCE,
            'starting_401k_principal': STARTING_401K_PRINCIPAL,
            'inflation_rate': INFLATION_RATE,
            '_401k_limit_growth_rate': CONST_401K_LIMIT_GROWTH_RATE,
            'starting_brokerage_balance': STARTING_BROKERAGE_BALANCE,
            'annual_brokerage_contribution': ANNUAL_BROKERAGE_CONTRIBUTION,
            'brokerage_contribution_growth_rate': BROKERAGE_CONTRIBUTION_GROWTH_RATE,
            'starting_529_balance': STARTING_529_BALANCE,
            'annual_529_contribution': ANNUAL_529_CONTRIBUTION,
            '_529_contribution_growth_rate': CONST_529_CONTRIBUTION_GROWTH_RATE,
            'annual_living_expenses': ANNUAL_LIVING_EXPENSES,
            'masters_degree_enabled': MASTERS_DEGREE_ENABLED,
            'masters_start_year': MASTERS_START_YEAR,
            'masters_degree_years': MASTERS_DEGREE_YEARS,
            'masters_enrollment_type': MASTERS_ENROLLMENT_TYPE,
            'masters_annual_tuition': MASTERS_ANNUAL_TUITION,
            'masters_employer_contribution': MASTERS_EMPLOYER_CONTRIBUTION,
            'ft_annual_living_expenses': FT_ANNUAL_LIVING_EXPENSES,
            'pt_annual_living_expenses': PT_ANNUAL_LIVING_EXPENSES,
            'compare_degree_types': COMPARE_DEGREE_TYPES,
            'ft_degree_years': FT_DEGREE_YEARS,
            'pt_degree_years': PT_DEGREE_YEARS,
            'ft_annual_tuition': FT_ANNUAL_TUITION,
            'pt_annual_tuition': PT_ANNUAL_TUITION,
            'ft_employer_contribution': FT_EMPLOYER_CONTRIBUTION,
            'pt_employer_contribution': PT_EMPLOYER_CONTRIBUTION,
        }
        
        self.create_widgets()
        
        # Auto-calculate on startup
        self.root.after(100, self.auto_calculate)
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="Financial Tools Calculator", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Create horizontal split frame
        split_frame = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        split_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Parameters
        self.create_parameters_panel(split_frame)
        
        # Right side - Results
        self.create_results_panel(split_frame)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Calculate button
        calculate_btn = ttk.Button(button_frame, text="Calculate", 
                                  command=self.calculate)
        calculate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Refresh button for manual updates
        refresh_btn = ttk.Button(button_frame, text="Refresh", 
                                command=self.auto_calculate)
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Reset button
        reset_btn = ttk.Button(button_frame, text="Reset to Defaults", 
                              command=self.reset_to_defaults)
        reset_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear results button
        clear_btn = ttk.Button(button_frame, text="Clear Results", 
                              command=self.clear_results)
        clear_btn.pack(side=tk.LEFT)
        
    def create_parameters_panel(self, split_frame):
        # Parameters frame
        params_frame = ttk.LabelFrame(split_frame, text="Parameters", padding="10")
        split_frame.add(params_frame, weight=1)
        
        # Create scrollable frame for parameters
        canvas = tk.Canvas(params_frame)
        scrollbar = ttk.Scrollbar(params_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Parameters section
        self.create_parameter_section(scrollable_frame, "Basic Parameters", [
            ("start_year", "Start Year", "int", self.default_params['start_year']),
            ("years", "Number of Years", "int", self.default_params['years']),
            ("age", "Starting Age", "int", self.default_params['age']),
            ("filing_status", "Filing Status", "combo", ["single", "joint", "separate_lived"], "single"),
        ])
        
        self.create_parameter_section(scrollable_frame, "Income & Growth", [
            ("starting_magi", "Starting MAGI ($)", "float", self.default_params['starting_magi']),
            ("magi_growth_rate", "MAGI Growth Rate (%)", "percent", self.default_params['magi_growth_rate']),
            ("plan_covered", "Plan Covered", "bool", self.default_params['plan_covered']),
        ])
        
        self.create_parameter_section(scrollable_frame, "Investment Parameters", [
            ("stock_market_return", "Stock Market Return (%)", "percent", self.default_params['stock_market_return']),
            ("inflation_rate", "Inflation Rate (%)", "percent", self.default_params['inflation_rate']),
        ])
        
        self.create_parameter_section(scrollable_frame, "401(k) Parameters", [
            ("starting_401k_balance", "Starting 401k Balance ($)", "float", self.default_params['starting_401k_balance']),
            ("starting_401k_principal", "Starting 401k Principal ($)", "float", self.default_params['starting_401k_principal']),
            ("_401k_limit_growth_rate", "401k Limit Growth Rate (%)", "percent", self.default_params['_401k_limit_growth_rate']),
        ])

        self.create_parameter_section(scrollable_frame, "Brokerage Account Parameters", [
            ("starting_brokerage_balance", "Starting Brokerage Balance ($)", "float", self.default_params['starting_brokerage_balance']),
            ("annual_brokerage_contribution", "Annual Brokerage Contribution ($)", "float", self.default_params['annual_brokerage_contribution']),
            ("brokerage_contribution_growth_rate", "Brokerage Contribution Growth Rate (%)", "percent", self.default_params['brokerage_contribution_growth_rate']),
        ])

        self.create_parameter_section(scrollable_frame, "529 Plan Parameters", [
            ("starting_529_balance", "Starting 529 Balance ($)", "float", self.default_params['starting_529_balance']),
            ("annual_529_contribution", "Annual 529 Contribution ($)", "float", self.default_params['annual_529_contribution']),
            ("_529_contribution_growth_rate", "529 Contribution Growth Rate (%)", "percent", self.default_params['_529_contribution_growth_rate']),
            ("annual_living_expenses", "Annual Living Expenses ($)", "float", self.default_params['annual_living_expenses']),
        ])

        self.create_parameter_section(scrollable_frame, "Master's Degree Parameters", [
            ("masters_degree_enabled", "Include Master's Degree", "bool", self.default_params['masters_degree_enabled']),
            ("compare_degree_types", "Compare Degree Types", "bool", self.default_params['compare_degree_types']),
            ("masters_start_year", "Degree Start Year", "int", self.default_params['masters_start_year']),
            ("masters_degree_years", "Degree Years", "int", self.default_params['masters_degree_years']),
            ("masters_annual_tuition", "Annual Tuition ($)", "float", self.default_params['masters_annual_tuition']),
            ("masters_enrollment_type", "Enrollment Type", "combo", ["full_time", "part_time"], self.default_params['masters_enrollment_type']),
            ("masters_employer_contribution", "Employer Contribution ($)", "float", self.default_params['masters_employer_contribution']),
        ])
        
        # Add separate part-time and full-time sections (initially hidden)
        self.create_parameter_section(scrollable_frame, "Full-Time Degree Parameters", [
            ("ft_degree_years", "Degree Years", "int", self.default_params['ft_degree_years']),
            ("ft_annual_tuition", "Annual Tuition ($)", "float", self.default_params['ft_annual_tuition']),
            ("ft_employer_contribution", "Employer Contribution ($)", "float", self.default_params['ft_employer_contribution']),
            ("ft_annual_living_expenses", "Annual Living Expenses ($)", "float", self.default_params['ft_annual_living_expenses']),
        ])
        
        self.create_parameter_section(scrollable_frame, "Part-Time Degree Parameters", [
            ("pt_degree_years", "Degree Years", "int", self.default_params['pt_degree_years']),
            ("pt_annual_tuition", "Annual Tuition ($)", "float", self.default_params['pt_annual_tuition']),
            ("pt_employer_contribution", "Employer Contribution ($)", "float", self.default_params['pt_employer_contribution']),
            ("pt_annual_living_expenses", "Annual Living Expenses ($)", "float", self.default_params['pt_annual_living_expenses']),
        ])
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initialize degree section visibility
        self.update_degree_section_visibility()
        
    def create_results_panel(self, split_frame):
        # Results frame
        results_frame = ttk.LabelFrame(split_frame, text="Results", padding="10")
        split_frame.add(results_frame, weight=2)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, 
                                                     font=("Courier", 9))
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for formatting
        self.results_text.tag_configure("bold", font=("Courier", 9, "bold"))
        self.results_text.tag_configure("header", font=("Courier", 10, "bold"))
        self.results_text.tag_configure("total", font=("Courier", 11, "bold"))
        
        # Add initial message
        self.results_text.insert(tk.END, "Click 'Calculate' to see results here.\n")
        self.results_text.config(state=tk.DISABLED)
        
    def create_parameter_section(self, parent, title, parameters):
        # Section frame
        section_frame = ttk.LabelFrame(parent, text=title, padding="10")
        section_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Store section frame for visibility control
        if not hasattr(self, 'section_frames'):
            self.section_frames = {}
        self.section_frames[title] = section_frame
        
        # Store widgets for later access
        if not hasattr(self, 'widgets'):
            self.widgets = {}
        
        for i, param_tuple in enumerate(parameters):
            if len(param_tuple) == 5 and param_tuple[2] == "combo":
                param_name, label, param_type, values, default_value = param_tuple
            else:
                param_name, label, param_type, default_value = param_tuple
            # Label
            label_widget = ttk.Label(section_frame, text=label)
            label_widget.grid(row=i, column=0, sticky="w", padx=(0, 10), pady=2)
            
            # Input widget based on type
            if param_type == "int":
                widget = ttk.Entry(section_frame, width=15)
                widget.insert(0, str(default_value))
            elif param_type == "float":
                widget = ttk.Entry(section_frame, width=15)
                widget.insert(0, str(default_value))
            elif param_type == "percent":
                widget = ttk.Entry(section_frame, width=15)
                widget.insert(0, f"{default_value * 100:.1f}")
            elif param_type == "bool":
                widget = ttk.Checkbutton(section_frame, text="Yes")
                if default_value:
                    widget.state(['!alternate'])
                    widget.state(['selected'])
            elif param_type == "combo":
                # Create display values for filing status
                if param_name == "filing_status":
                    display_values = ["Single", "Joint", "Separated but not Living Together"]
                    widget = ttk.Combobox(section_frame, values=display_values, width=20)
                    # Map display values to internal values
                    if default_value == "single":
                        widget.set("Single")
                    elif default_value == "joint":
                        widget.set("Joint")
                    elif default_value == "separate_lived":
                        widget.set("Separated but not Living Together")
                    else:
                        widget.set("Single")
                elif param_name == "masters_enrollment_type":
                    # Create display values for enrollment type
                    display_values = ["Full Time", "Part Time"]
                    widget = ttk.Combobox(section_frame, values=display_values, width=15)
                    # Map display values to internal values
                    if default_value == "full_time":
                        widget.set("Full Time")
                    elif default_value == "part_time":
                        widget.set("Part Time")
                    else:
                        widget.set("Full Time")
                else:
                    widget = ttk.Combobox(section_frame, values=values, width=12)
                    widget.set(default_value)
                widget.state(['readonly'])
            
            widget.grid(row=i, column=1, sticky="w", pady=2)
            self.widgets[param_name] = widget
            
            # Add event bindings for auto-calculation
            if param_type in ["int", "float", "percent"]:
                widget.bind('<KeyRelease>', self.on_parameter_change)
                widget.bind('<FocusOut>', self.on_parameter_change)
                widget.bind('<Return>', self.on_parameter_change)
                widget.bind('<Tab>', self.on_parameter_change)
            elif param_type == "bool":
                widget.config(command=self.on_parameter_change)
            elif param_type == "combo":
                widget.bind('<<ComboboxSelected>>', self.on_parameter_change)
                widget.bind('<FocusOut>', self.on_parameter_change)
        
        # Set up visibility control for master's degree sections
        if title == "Master's Degree Parameters":
            # Add special handling for compare_degree_types toggle
            if "compare_degree_types" in self.widgets:
                self.widgets["compare_degree_types"].config(command=self.toggle_degree_comparison)
                # Initial visibility setup
                self.update_degree_section_visibility()
    
    def toggle_degree_comparison(self):
        """Toggle visibility of degree comparison sections"""
        self.update_degree_section_visibility()
        self.on_parameter_change()
    
    def update_degree_section_visibility(self):
        """Update visibility of master's degree sections based on compare toggle"""
        if not hasattr(self, 'section_frames'):
            return
            
        compare_enabled = "compare_degree_types" in self.widgets and "selected" in self.widgets["compare_degree_types"].state()
        
        # Show/hide the appropriate sections
        if "Master's Degree Parameters" in self.section_frames:
            masters_section = self.section_frames["Master's Degree Parameters"]
            if compare_enabled:
                # Hide individual parameters, show enrollment type only
                for i, child in enumerate(masters_section.winfo_children()):
                    if i >= 2:  # Skip the first two widgets (enabled and compare toggles)
                        if isinstance(child, ttk.Label):
                            label_text = child.cget("text")
                            if label_text in ["Degree Years", "Annual Tuition ($)", "Employer Contribution ($)"]:
                                child.grid_remove()
                        elif hasattr(child, 'grid_info') and child.grid_info():
                            widget_name = None
                            for name, widget in self.widgets.items():
                                if widget == child:
                                    widget_name = name
                                    break
                            if widget_name in ["masters_degree_years", "masters_annual_tuition", "masters_employer_contribution"]:
                                child.grid_remove()
            else:
                # Show all parameters
                for child in masters_section.winfo_children():
                    child.grid()
        
        # Show/hide comparison sections
        if "Full-Time Degree Parameters" in self.section_frames:
            ft_section = self.section_frames["Full-Time Degree Parameters"]
            if compare_enabled:
                ft_section.pack(fill=tk.X, padx=5, pady=5)
            else:
                ft_section.pack_forget()
        
        if "Part-Time Degree Parameters" in self.section_frames:
            pt_section = self.section_frames["Part-Time Degree Parameters"]
            if compare_enabled:
                pt_section.pack(fill=tk.X, padx=5, pady=5)
            else:
                pt_section.pack_forget()
    
    def auto_calculate(self):
        """Automatically calculate and display results"""
        try:
            # Check if any fields are empty
            params = self.get_parameter_values()
            if params is None:
                # Show message about empty fields
                self.results_text.config(state=tk.NORMAL)
                self.results_text.delete(.01, tk.END)
                self.results_text.insert(tk.END, "Please fill in all parameters to see results.\n")
                self.results_text.insert(tk.END, "All fields must have values before calculation can proceed.\n")
                self.results_text.config(state=tk.DISABLED)
                return
            
            # Proceed with calculation if all fields are filled
            self.calculate()
        except Exception as e:
            # Show error message for debugging
            print(f"Auto-calculation error: {e}")
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Error during auto-calculation: {str(e)}\n")
            self.results_text.config(state=tk.DISABLED)
    
    def on_parameter_change(self, event=None):
        """Handle parameter changes and trigger auto-calculation"""
        print(f"Parameter change detected: {event}")  # Debug print
        
        # Use a timer to avoid too many calculations while typing
        if hasattr(self, '_calculation_timer'):
            self.root.after_cancel(self._calculation_timer)
        
        # Reduce delay to 300ms for more responsive updates
        self._calculation_timer = self.root.after(300, self.auto_calculate)
            
    def get_parameter_values(self):
        """Extract values from GUI widgets"""
        values = {}
        
        for param_name, widget in self.widgets.items():
            try:
                # Check for empty fields
                if param_name in ["plan_covered", "masters_degree_enabled", "compare_degree_types"]:
                    # Checkboxes are never "empty" - they have a default state
                    values[param_name] = "selected" in widget.state()
                elif param_name in ["filing_status", "masters_enrollment_type"]:
                    # Comboboxes should have a selected value
                    display_value = widget.get()
                    if not display_value or display_value.strip() == "":
                        return None  # Empty combobox
                    
                    # Convert display values back to internal values
                    if param_name == "filing_status":
                        if display_value == "Single":
                            values[param_name] = "single"
                        elif display_value == "Joint":
                            values[param_name] = "joint"
                        elif display_value == "Separated but not Living Together":
                            values[param_name] = "separate_lived"
                        else:
                            values[param_name] = "single"  # Default fallback
                    elif param_name == "masters_enrollment_type":
                        if display_value == "Full Time":
                            values[param_name] = "full_time"
                        elif display_value == "Part Time":
                            values[param_name] = "part_time"
                        else:
                            values[param_name] = "full_time"  # Default fallback
                else:
                    # Text entry fields
                    field_value = widget.get().strip()
                    if not field_value:
                        return None  # Empty field
                    
                    if param_name in ["magi_growth_rate", "stock_market_return", 
                                      "inflation_rate", "_401k_limit_growth_rate", "brokerage_contribution_growth_rate",
                                      "_529_contribution_growth_rate"]:
                        # Convert percentage to decimal
                        values[param_name] = float(field_value) / 100
                    elif param_name in ["start_year", "years", "age", "masters_start_year", "masters_degree_years",
                                       "ft_degree_years", "pt_degree_years"]:
                        values[param_name] = int(field_value)
                    else:
                        values[param_name] = float(field_value)
            except ValueError as e:
                messagebox.showerror("Input Error", 
                                   f"Invalid value for {param_name}: {widget.get()}")
                return None
        
        # Handle compare degree types logic
        if values.get("compare_degree_types", False):
            # Use separate full-time and part-time parameters
            enrollment_type = values.get("masters_enrollment_type", "full_time")
            if enrollment_type == "full_time":
                values["masters_degree_years"] = values.get("ft_degree_years", FT_DEGREE_YEARS)
                values["masters_annual_tuition"] = values.get("ft_annual_tuition", FT_ANNUAL_TUITION)
                values["masters_employer_contribution"] = values.get("ft_employer_contribution", FT_EMPLOYER_CONTRIBUTION)
                values["ft_annual_living_expenses"] = values.get("ft_annual_living_expenses", FT_ANNUAL_LIVING_EXPENSES)
            else:  # part_time
                values["masters_degree_years"] = values.get("pt_degree_years", PT_DEGREE_YEARS)
                values["masters_annual_tuition"] = values.get("pt_annual_tuition", PT_ANNUAL_TUITION)
                values["masters_employer_contribution"] = values.get("pt_employer_contribution", PT_EMPLOYER_CONTRIBUTION)
                values["pt_annual_living_expenses"] = values.get("pt_annual_living_expenses", PT_ANNUAL_LIVING_EXPENSES)
        
        return values
    
    def calculate(self):
        """Perform calculations and display results"""
        # Get parameter values
        params = self.get_parameter_values()
        if params is None:
            messagebox.showwarning("Input Error", "Please fill in all parameters before calculating.")
            return
        
        # Clear previous results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        try:
            # Extract master's degree parameters
            masters_degree_enabled = "masters_degree_enabled" in self.widgets and "selected" in self.widgets["masters_degree_enabled"].state()
            masters_start_year = int(self.widgets["masters_start_year"].get()) if "masters_start_year" in self.widgets else MASTERS_START_YEAR
            masters_degree_years = int(self.widgets["masters_degree_years"].get()) if "masters_degree_years" in self.widgets else MASTERS_DEGREE_YEARS
            masters_annual_tuition = float(self.widgets["masters_annual_tuition"].get()) if "masters_annual_tuition" in self.widgets else MASTERS_ANNUAL_TUITION
            masters_employer_contribution = float(self.widgets["masters_employer_contribution"].get()) if "masters_employer_contribution" in self.widgets else MASTERS_EMPLOYER_CONTRIBUTION
            
            # Get enrollment type
            if "masters_enrollment_type" in self.widgets:
                enrollment_display = self.widgets["masters_enrollment_type"].get()
                if enrollment_display == "Full Time":
                    masters_enrollment_type = "full_time"
                elif enrollment_display == "Part Time":
                    masters_enrollment_type = "part_time"
                else:
                    masters_enrollment_type = "full_time"
            else:
                masters_enrollment_type = "full_time"
            
            # Extract living expenses parameters
            ft_annual_living_expenses = float(self.widgets["ft_annual_living_expenses"].get()) if "ft_annual_living_expenses" in self.widgets else FT_ANNUAL_LIVING_EXPENSES
            pt_annual_living_expenses = float(self.widgets["pt_annual_living_expenses"].get()) if "pt_annual_living_expenses" in self.widgets else PT_ANNUAL_LIVING_EXPENSES

            # Check if compare degree types is enabled
            compare_enabled = params.get("compare_degree_types", False)
            
            if compare_enabled:
                # Calculate both full-time and part-time scenarios
                self.calculate_comparison_results(params)
            else:
                # Calculate single scenario
                self.calculate_single_result(params)
                
        except Exception as e:
            self.results_text.insert(tk.END, f"Error during calculation: {str(e)}\n")
            print(f"Calculation error: {e}")
        
        self.results_text.config(state=tk.DISABLED)
    
    def calculate_single_result(self, params):
        """Calculate and display single scenario results"""
        # Calculate total savings
        total_savings = calculate_total_savings(
            start_year=params['start_year'],
            years=params['years'],
            age=params['age'],
            filing_status=params['filing_status'],
            starting_magi=params['starting_magi'],
            magi_growth_rate=params['magi_growth_rate'],
            plan_covered=params['plan_covered'],
            stock_market_return=params['stock_market_return'],
            starting_401k_balance=params['starting_401k_balance'],
            starting_401k_principal=params['starting_401k_principal'],
            inflation_rate=params['inflation_rate'],
            _401k_limit_growth_rate=params['_401k_limit_growth_rate'],
            starting_brokerage_balance=params['starting_brokerage_balance'],
            annual_brokerage_contribution=params['annual_brokerage_contribution'],
            brokerage_contribution_growth_rate=params['brokerage_contribution_growth_rate'],
            starting_529_balance=params['starting_529_balance'],
            annual_529_contribution=params['annual_529_contribution'],
            _529_contribution_growth_rate=params['_529_contribution_growth_rate'],
            annual_living_expenses=params['annual_living_expenses'],
            masters_degree_enabled=params['masters_degree_enabled'],
            masters_start_year=params['masters_start_year'],
            masters_degree_years=params['masters_degree_years'],
            masters_annual_tuition=params['masters_annual_tuition'],
            masters_enrollment_type=params['masters_enrollment_type'],
            masters_employer_contribution=params['masters_employer_contribution'],
            ft_annual_living_expenses=params['ft_annual_living_expenses'],
            pt_annual_living_expenses=params['pt_annual_living_expenses'],
            return_details=True
        )
        
        # Display results
        self.display_single_results(total_savings, params)
    
    def calculate_comparison_results(self, params):
        """Calculate and display comparison results for full-time vs part-time"""
        # Calculate full-time scenario
        ft_params = params.copy()
        ft_params['masters_enrollment_type'] = 'full_time'
        ft_params['masters_degree_years'] = params['ft_degree_years']
        ft_params['masters_annual_tuition'] = params['ft_annual_tuition']
        ft_params['masters_employer_contribution'] = params['ft_employer_contribution']
        ft_params['ft_annual_living_expenses'] = params['ft_annual_living_expenses']
        ft_params['pt_annual_living_expenses'] = params['pt_annual_living_expenses']
        
        ft_savings = calculate_total_savings(
            start_year=ft_params['start_year'],
            years=ft_params['years'],
            age=ft_params['age'],
            filing_status=ft_params['filing_status'],
            starting_magi=ft_params['starting_magi'],
            magi_growth_rate=ft_params['magi_growth_rate'],
            plan_covered=ft_params['plan_covered'],
            stock_market_return=ft_params['stock_market_return'],
            starting_401k_balance=ft_params['starting_401k_balance'],
            starting_401k_principal=ft_params['starting_401k_principal'],
            inflation_rate=ft_params['inflation_rate'],
            _401k_limit_growth_rate=ft_params['_401k_limit_growth_rate'],
            starting_brokerage_balance=ft_params['starting_brokerage_balance'],
            annual_brokerage_contribution=ft_params['annual_brokerage_contribution'],
            brokerage_contribution_growth_rate=ft_params['brokerage_contribution_growth_rate'],
            starting_529_balance=ft_params['starting_529_balance'],
            annual_529_contribution=ft_params['annual_529_contribution'],
            _529_contribution_growth_rate=ft_params['_529_contribution_growth_rate'],
            annual_living_expenses=ft_params['annual_living_expenses'],
            masters_degree_enabled=ft_params['masters_degree_enabled'],
            masters_start_year=ft_params['masters_start_year'],
            masters_degree_years=ft_params['masters_degree_years'],
            masters_annual_tuition=ft_params['masters_annual_tuition'],
            masters_enrollment_type=ft_params['masters_enrollment_type'],
            masters_employer_contribution=ft_params['masters_employer_contribution'],
            ft_annual_living_expenses=ft_params['ft_annual_living_expenses'],
            pt_annual_living_expenses=ft_params['pt_annual_living_expenses'],
            return_details=True
        )
        
        # Calculate part-time scenario
        pt_params = params.copy()
        pt_params['masters_enrollment_type'] = 'part_time'
        pt_params['masters_degree_years'] = params['pt_degree_years']
        pt_params['masters_annual_tuition'] = params['pt_annual_tuition']
        pt_params['masters_employer_contribution'] = params['pt_employer_contribution']
        pt_params['ft_annual_living_expenses'] = params['ft_annual_living_expenses']
        pt_params['pt_annual_living_expenses'] = params['pt_annual_living_expenses']
        
        pt_savings = calculate_total_savings(
            start_year=pt_params['start_year'],
            years=pt_params['years'],
            age=pt_params['age'],
            filing_status=pt_params['filing_status'],
            starting_magi=pt_params['starting_magi'],
            magi_growth_rate=pt_params['magi_growth_rate'],
            plan_covered=pt_params['plan_covered'],
            stock_market_return=pt_params['stock_market_return'],
            starting_401k_balance=pt_params['starting_401k_balance'],
            starting_401k_principal=pt_params['starting_401k_principal'],
            inflation_rate=pt_params['inflation_rate'],
            _401k_limit_growth_rate=pt_params['_401k_limit_growth_rate'],
            starting_brokerage_balance=pt_params['starting_brokerage_balance'],
            annual_brokerage_contribution=pt_params['annual_brokerage_contribution'],
            brokerage_contribution_growth_rate=pt_params['brokerage_contribution_growth_rate'],
            starting_529_balance=pt_params['starting_529_balance'],
            annual_529_contribution=pt_params['annual_529_contribution'],
            _529_contribution_growth_rate=pt_params['_529_contribution_growth_rate'],
            annual_living_expenses=pt_params['annual_living_expenses'],
            masters_degree_enabled=pt_params['masters_degree_enabled'],
            masters_start_year=pt_params['masters_start_year'],
            masters_degree_years=pt_params['masters_degree_years'],
            masters_annual_tuition=pt_params['masters_annual_tuition'],
            masters_enrollment_type=pt_params['masters_enrollment_type'],
            masters_employer_contribution=pt_params['masters_employer_contribution'],
            ft_annual_living_expenses=pt_params['ft_annual_living_expenses'],
            pt_annual_living_expenses=pt_params['pt_annual_living_expenses'],
            return_details=True
        )
        
        # Display comparison results
        self.display_comparison_results(ft_savings, pt_savings, ft_params, pt_params)
    
    def display_single_results(self, total_savings, params):
        """Display single scenario results"""
        # Display Total Savings Summary at the top in bold
        self.results_text.insert(tk.END, "TOTAL SAVINGS SUMMARY\n", "header")
        self.results_text.insert(tk.END, "=" * 80 + "\n")
        
        self.results_text.insert(tk.END, "TOTAL SAVINGS:\n", "total")
        self.results_text.insert(tk.END, f"  Nominal Value: ${total_savings['total_nominal']:,.2f}\n", "total")
        self.results_text.insert(tk.END, f"  Real Value (Inflation-Adjusted): ${total_savings['total_real']:,.2f}\n", "total")
        self.results_text.insert(tk.END, f"  Real Value as % of Nominal: {(total_savings['total_real']/total_savings['total_nominal']*100):.1f}%\n\n", "total")
        
        # Display detailed breakdown
        self.display_detailed_breakdown(total_savings, params)
    
    def display_detailed_breakdown(self, total_savings, params):
        """Display detailed breakdown of savings without headers"""
        self.results_text.insert(tk.END, "Savings Breakdown:\n", "bold")
        self.results_text.insert(tk.END, f"  IRA Accumulated (Nominal): ${total_savings['ira_nominal']:,.2f}\n")
        self.results_text.insert(tk.END, f"  IRA Accumulated (Real): ${total_savings['ira_real']:,.2f}\n")
        self.results_text.insert(tk.END, f"  401k Final Balance (Nominal): ${total_savings['401k_nominal']:,.2f}\n")
        self.results_text.insert(tk.END, f"  401k Final Balance (Real): ${total_savings['401k_real']:,.2f}\n")
        self.results_text.insert(tk.END, f"  401k Total Contributions: ${total_savings['401k_contributions']:,.2f}\n")
        self.results_text.insert(tk.END, f"  Brokerage Final Balance (Nominal): ${total_savings['brokerage_nominal']:,.2f}\n")
        self.results_text.insert(tk.END, f"  Brokerage Final Balance (Real): ${total_savings['brokerage_real']:,.2f}\n")
        self.results_text.insert(tk.END, f"  529 Final Balance (Nominal): ${total_savings['529_nominal']:,.2f}\n")
        self.results_text.insert(tk.END, f"  529 Final Balance (Real): ${total_savings['529_real']:,.2f}\n")
        self.results_text.insert(tk.END, f"  529 Withdrawal Tax: ${total_savings['529_tax']:,.2f}\n")
        self.results_text.insert(tk.END, f"  529 After-Tax Amount: ${total_savings['529_after_tax']:,.2f}\n\n")
        
        # Display master's degree info if enabled
        if params.get('masters_degree_enabled', False):
            self.results_text.insert(tk.END, "Master's Degree Information:\n", "bold")
            self.results_text.insert(tk.END, f"  Start Year: {params['masters_start_year']}\n")
            self.results_text.insert(tk.END, f"  Degree Years: {params['masters_degree_years']}\n")
            self.results_text.insert(tk.END, f"  Annual Tuition: ${params['masters_annual_tuition']:,.0f}\n")
            self.results_text.insert(tk.END, f"  Enrollment Type: {params['masters_enrollment_type'].replace('_', ' ').title()}\n")
            self.results_text.insert(tk.END, f"  Employer Contribution: ${params['masters_employer_contribution']:,.0f}\n")
            
            # Add living expenses information
            if params['masters_enrollment_type'] == 'full_time':
                annual_living_expenses = params.get('ft_annual_living_expenses', 30000)
                total_living_expenses = annual_living_expenses * params['masters_degree_years']
                self.results_text.insert(tk.END, f"  Annual Living Expenses: ${annual_living_expenses:,.0f}\n")
                self.results_text.insert(tk.END, f"  Total Living Expenses: ${total_living_expenses:,.0f}\n")
            else:
                annual_living_expenses = params.get('pt_annual_living_expenses', 0)
                total_living_expenses = annual_living_expenses * params['masters_degree_years']
                self.results_text.insert(tk.END, f"  Annual Living Expenses: ${annual_living_expenses:,.0f}\n")
                self.results_text.insert(tk.END, f"  Total Living Expenses: ${total_living_expenses:,.0f}\n")
            
            self.results_text.insert(tk.END, "\n")
    
    def display_comparison_results(self, ft_savings, pt_savings, ft_params, pt_params):
        """Display comparison results for full-time vs part-time"""
        # Display comparison header
        self.results_text.insert(tk.END, "DEGREE TYPE COMPARISON\n", "header")
        self.results_text.insert(tk.END, "=" * 80 + "\n\n")
        
        # Display total savings summary for both scenarios
        self.results_text.insert(tk.END, "TOTAL SAVINGS SUMMARY\n", "bold")
        self.results_text.insert(tk.END, "-" * 80 + "\n")
        
        # Calculate total wealth including 529 after-tax amounts
        ft_total_wealth = ft_savings['ira_nominal'] + ft_savings['401k_nominal'] + ft_savings['brokerage_nominal'] + ft_savings['529_after_tax']
        pt_total_wealth = pt_savings['ira_nominal'] + pt_savings['401k_nominal'] + pt_savings['brokerage_nominal'] + pt_savings['529_after_tax']
        
        ft_total_wealth_real = ft_savings['ira_real'] + ft_savings['401k_real'] + ft_savings['brokerage_real'] + (ft_savings['529_after_tax'] / ft_savings['total_nominal'] * ft_savings['total_real'])
        pt_total_wealth_real = pt_savings['ira_real'] + pt_savings['401k_real'] + pt_savings['brokerage_real'] + (pt_savings['529_after_tax'] / pt_savings['total_nominal'] * pt_savings['total_real'])
        
        self.results_text.insert(tk.END, "FULL-TIME DEGREE TOTAL WEALTH:\n", "total")
        self.results_text.insert(tk.END, f"  Total Wealth (Nominal): ${ft_total_wealth:,.2f}\n", "total")
        self.results_text.insert(tk.END, f"  Total Wealth (Real): ${ft_total_wealth_real:,.2f}\n", "total")
        self.results_text.insert(tk.END, f"  Real Value as % of Nominal: {(ft_total_wealth_real/ft_total_wealth*100):.1f}%\n\n", "total")
        
        self.results_text.insert(tk.END, "PART-TIME DEGREE TOTAL WEALTH:\n", "total")
        self.results_text.insert(tk.END, f"  Total Wealth (Nominal): ${pt_total_wealth:,.2f}\n", "total")
        self.results_text.insert(tk.END, f"  Total Wealth (Real): ${pt_total_wealth_real:,.2f}\n", "total")
        self.results_text.insert(tk.END, f"  Real Value as % of Nominal: {(pt_total_wealth_real/pt_total_wealth*100):.1f}%\n\n", "total")
        
        self.results_text.insert(tk.END, f"PART-TIME ADVANTAGE:\n", "total")
        self.results_text.insert(tk.END, f"  Nominal: ${pt_total_wealth - ft_total_wealth:+,.2f}\n", "total")
        self.results_text.insert(tk.END, f"  Real: ${pt_total_wealth_real - ft_total_wealth_real:+,.2f}\n\n", "total")
        
        # Display comparison table
        self.results_text.insert(tk.END, "COMPARISON SUMMARY\n", "bold")
        self.results_text.insert(tk.END, "-" * 80 + "\n")
        
        # Create comparison table
        comparison_data = [
            ["Metric", "Full-Time", "Part-Time", "Difference"],
            ["Total Nominal", f"${ft_savings['total_nominal']:,.2f}", f"${pt_savings['total_nominal']:,.2f}", 
             f"${pt_savings['total_nominal'] - ft_savings['total_nominal']:+,.2f}"],
            ["Total Real", f"${ft_savings['total_real']:,.2f}", f"${pt_savings['total_real']:,.2f}", 
             f"${pt_savings['total_real'] - ft_savings['total_real']:+,.2f}"],
            ["IRA Nominal", f"${ft_savings['ira_nominal']:,.2f}", f"${pt_savings['ira_nominal']:,.2f}", 
             f"${pt_savings['ira_nominal'] - ft_savings['ira_nominal']:+,.2f}"],
            ["401k Nominal", f"${ft_savings['401k_nominal']:,.2f}", f"${pt_savings['401k_nominal']:,.2f}", 
             f"${pt_savings['401k_nominal'] - ft_savings['401k_nominal']:+,.2f}"],
            ["Brokerage Nominal", f"${ft_savings['brokerage_nominal']:,.2f}", f"${pt_savings['brokerage_nominal']:,.2f}", 
             f"${pt_savings['brokerage_nominal'] - ft_savings['brokerage_nominal']:+,.2f}"],
            ["529 Nominal", f"${ft_savings['529_nominal']:,.2f}", f"${pt_savings['529_nominal']:,.2f}", 
             f"${pt_savings['529_nominal'] - ft_savings['529_nominal']:+,.2f}"],
        ]
        
        # Calculate total expenses for each scenario
        ft_total_tuition = ft_params['masters_annual_tuition'] * ft_params['masters_degree_years']
        ft_total_living = ft_params.get('ft_annual_living_expenses', 30000) * ft_params['masters_degree_years']  # Full-time has living expenses
        ft_total_expenses = ft_total_tuition + ft_total_living
        
        pt_total_tuition = pt_params['masters_annual_tuition'] * pt_params['masters_degree_years']
        pt_total_living = pt_params.get('pt_annual_living_expenses', 0) * pt_params['masters_degree_years']  # Part-time has living expenses too
        pt_total_expenses = pt_total_tuition + pt_total_living
        
        # Add expense summary to comparison table
        comparison_data.extend([
            ["Total Tuition", f"${ft_total_tuition:,.2f}", f"${pt_total_tuition:,.2f}", 
             f"${pt_total_tuition - ft_total_tuition:+,.2f}"],
            ["Total Living Expenses", f"${ft_total_living:,.2f}", f"${pt_total_living:,.2f}", 
             f"${pt_total_living - ft_total_living:+,.2f}"],
            ["Total Expenses", f"${ft_total_expenses:,.2f}", f"${pt_total_expenses:,.2f}", 
             f"${pt_total_expenses - ft_total_expenses:+,.2f}"],
        ])
        
        # Display comparison table
        for row in comparison_data:
            if row[0] == "Metric":
                self.results_text.insert(tk.END, f"{row[0]:<20} {row[1]:<20} {row[2]:<20} {row[3]:<20}\n", "bold")
                self.results_text.insert(tk.END, "-" * 80 + "\n")
            else:
                self.results_text.insert(tk.END, f"{row[0]:<20} {row[1]:<20} {row[2]:<20} {row[3]:<20}\n")
        
        self.results_text.insert(tk.END, "\n")
        
        # Display detailed breakdown for each scenario
        self.results_text.insert(tk.END, "FULL-TIME DEGREE DETAILS\n", "bold")
        self.results_text.insert(tk.END, "-" * 80 + "\n")
        self.display_detailed_breakdown(ft_savings, ft_params)
        
        # Display yearly breakdown for full-time scenario
        if 'yearly_breakdown' in ft_savings:
            self.results_text.insert(tk.END, "\nFULL-TIME DEGREE YEARLY BREAKDOWN\n", "bold")
            self.results_text.insert(tk.END, "-" * 140 + "\n")
            self.display_yearly_breakdown(ft_savings['yearly_breakdown'], "FULL-TIME")
        
        self.results_text.insert(tk.END, "\nPART-TIME DEGREE DETAILS\n", "bold")
        self.results_text.insert(tk.END, "-" * 80 + "\n")
        self.display_detailed_breakdown(pt_savings, pt_params)
        
        # Display yearly breakdown for part-time scenario
        if 'yearly_breakdown' in pt_savings:
            self.results_text.insert(tk.END, "\nPART-TIME DEGREE YEARLY BREAKDOWN\n", "bold")
            self.results_text.insert(tk.END, "-" * 140 + "\n")
            self.display_yearly_breakdown(pt_savings['yearly_breakdown'], "PART-TIME")
    
    def display_yearly_breakdown(self, yearly_data, scenario_type):
        """Display yearly breakdown in a formatted table"""
        if not yearly_data:
            return
            
        # Create headers
        headers = [
            "Year", "Age", "IRA Contrib", "IRA Future", "401k Balance", 
            "Brokerage Contrib", "Brokerage Balance", "Total Balance", "529 Balance", "529 Tuition", "529 Living"
        ]
        
        # Display header
        header_line = f"{'Year':<6} {'Age':<4} {'IRA Contrib':<12} {'IRA Future':<12} {'401k Balance':<12} {'Brokerage Contrib':<16} {'Brokerage Balance':<16} {'Total Balance':<14} {'529 Balance':<12} {'529 Tuition':<12} {'529 Living':<12}\n"
        self.results_text.insert(tk.END, header_line, "bold")
        self.results_text.insert(tk.END, "-" * 140 + "\n")
        
        # Display data rows
        for year_data in yearly_data:
            # Highlight degree years for easy identification
            year = year_data['year']
            age = year_data['age']
            
            # Check if this is a degree year (assuming degree starts in 2025)
            is_degree_year = (year >= 2025 and year < 2025 + 2) if scenario_type == "FULL-TIME" else (year >= 2025 and year < 2025 + 3)
            
            # Format the row
            row = (
                f"{year:<6} "
                f"{age:<4} "
                f"${year_data['ira_contribution']:<11,.0f} "
                f"${year_data['ira_future_value']:<11,.0f} "
                f"${year_data['401k_balance']:<11,.0f} "
                f"${year_data['brokerage_contribution']:<15,.0f} "
                f"${year_data['brokerage_balance']:<15,.0f} "
                f"${year_data['total_balance']:<13,.0f} "
                f"${year_data['529_balance']:<11,.0f} "
                f"${year_data.get('529_tuition_withdrawal', 0):<11,.0f} "
                f"${year_data.get('529_living_withdrawal', 0):<11,.0f}\n"
            )
            
            # Add special formatting for degree years
            if is_degree_year:
                self.results_text.insert(tk.END, f"*** {scenario_type} DEGREE YEAR ***\n", "bold")
                self.results_text.insert(tk.END, row, "bold")
            else:
                self.results_text.insert(tk.END, row)
        
        self.results_text.insert(tk.END, "\n")
    
    def reset_to_defaults(self):
        """Reset all parameters to default values"""
        for param_name, widget in self.widgets.items():
            # Handle parameters that might not be in default_params
            if param_name not in self.default_params:
                # Set reasonable defaults for new parameters
                if param_name == "compare_degree_types":
                    widget.state(['!selected'])  # Default to False
                elif param_name in ["ft_degree_years", "pt_degree_years"]:
                    widget.delete(0, tk.END)
                    widget.insert(0, "2")  # Default to 2 years
                elif param_name in ["ft_annual_tuition", "pt_annual_tuition"]:
                    widget.delete(0, tk.END)
                    widget.insert(0, "50000")  # Default to $50,000
                elif param_name in ["ft_employer_contribution", "pt_employer_contribution"]:
                    widget.delete(0, tk.END)
                    widget.insert(0, "0")  # Default to $0
                elif param_name == "ft_annual_living_expenses":
                    widget.delete(0, tk.END)
                    widget.insert(0, "30000")  # Default to $30,000
                elif param_name == "pt_annual_living_expenses":
                    widget.delete(0, tk.END)
                    widget.insert(0, "0")  # Default to $25,000
                continue
            
            default_value = self.default_params[param_name]
            
            if param_name in ["plan_covered", "masters_degree_enabled", "compare_degree_types"]:
                if default_value:
                    widget.state(['selected'])
                else:
                    widget.state(['!selected'])
            elif param_name in ["magi_growth_rate", "stock_market_return", 
                              "inflation_rate", "_401k_limit_growth_rate", "brokerage_contribution_growth_rate",
                              "_529_contribution_growth_rate"]:
                widget.delete(0, tk.END)
                widget.insert(0, f"{default_value * 100:.1f}")
            elif param_name == "filing_status":
                # Convert internal value to display value
                if default_value == "single":
                    widget.set("Single")
                elif default_value == "joint":
                    widget.set("Joint")
                elif default_value == "separate_lived":
                    widget.set("Separated but not Living Together")
                else:
                    widget.set("Single")
            elif param_name == "masters_enrollment_type":
                # Convert internal value to display value
                if default_value == "full_time":
                    widget.set("Full Time")
                elif default_value == "part_time":
                    widget.set("Part Time")
                else:
                    widget.set("Full Time")
            else:
                widget.delete(0, tk.END)
                widget.insert(0, str(default_value))
        
        # Update visibility after reset
        self.update_degree_section_visibility()
        
        messagebox.showinfo("Reset", "Parameters reset to default values.")
        
        # Auto-calculate after reset
        self.root.after(100, self.auto_calculate)
        
    def clear_results(self):
        """Clear the results text area"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Click 'Calculate' to see results here.\n")
        self.results_text.config(state=tk.DISABLED)

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