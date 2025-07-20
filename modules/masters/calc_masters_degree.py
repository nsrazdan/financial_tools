#!/usr/bin/env python3
"""
Master's Degree Cost Calculator
Calculates the total cost of pursuing a master's degree including tuition and opportunity costs.
"""

from typing import Dict, Any, List
from tabulate import tabulate


def calculate_masters_degree_cost(
    start_year: int,
    degree_years: int,
    annual_tuition: float,
    enrollment_type: str = "full_time",
    inflation_rate: float = 0.03,
    return_details: bool = False
) -> Dict[str, Any]:
    """
    Calculate the total cost of pursuing a master's degree.
    
    Args:
        start_year: Year when the degree program starts
        degree_years: Number of years to complete the degree
        annual_tuition: Annual tuition cost
        enrollment_type: "full_time" or "part_time"
        inflation_rate: Annual inflation rate for tuition increases (default 3%)
        return_details: If True, return detailed year-by-year breakdown
        
    Returns:
        Dictionary containing degree cost breakdown
    """
    
    total_tuition_nominal = 0.0
    total_tuition_real = 0.0
    year_details = []
    
    for i in range(degree_years):
        year = start_year + i
        
        # Calculate tuition for this year (with inflation)
        tuition_this_year = annual_tuition * ((1 + inflation_rate) ** i)
        
        # Adjust for enrollment type
        if enrollment_type == "part_time":
            # Part-time students typically pay 60-80% of full-time tuition
            # and may take longer to complete, but we'll keep the same years
            # and adjust the annual cost
            tuition_this_year *= 0.7  # 70% of full-time tuition
        
        # Calculate real (inflation-adjusted) tuition
        tuition_real = tuition_this_year / ((1 + inflation_rate) ** i)
        
        total_tuition_nominal += tuition_this_year
        total_tuition_real += tuition_real
        
        # Store year details if requested
        if return_details:
            year_details.append({
                'year': year,
                'tuition_nominal': tuition_this_year,
                'tuition_real': tuition_real,
                'cumulative_nominal': total_tuition_nominal,
                'cumulative_real': total_tuition_real,
                'enrollment_type': enrollment_type
            })
    
    # Calculate additional costs (books, fees, etc.)
    # Estimate 15% of tuition for additional costs
    additional_costs_nominal = total_tuition_nominal * 0.15
    additional_costs_real = total_tuition_real * 0.15
    
    # Calculate total costs
    total_cost_nominal = total_tuition_nominal + additional_costs_nominal
    total_cost_real = total_tuition_real + additional_costs_real
    
    results = {
        'total_tuition_nominal': total_tuition_nominal,
        'total_tuition_real': total_tuition_real,
        'additional_costs_nominal': additional_costs_nominal,
        'additional_costs_real': additional_costs_real,
        'total_cost_nominal': total_cost_nominal,
        'total_cost_real': total_cost_real,
        'parameters': {
            'start_year': start_year,
            'degree_years': degree_years,
            'annual_tuition': annual_tuition,
            'enrollment_type': enrollment_type,
            'inflation_rate': inflation_rate
        }
    }
    
    if return_details:
        results['year_details'] = year_details
    
    return results


def print_masters_degree_analysis(analysis_data: dict) -> None:
    """
    Print a formatted table showing master's degree cost analysis.
    
    Args:
        analysis_data: Dictionary returned from calculate_masters_degree_cost with return_details=True
    """
    params = analysis_data['parameters']
    year_details = analysis_data['year_details']
    
    print("\n" + "="*80)
    print("MASTER'S DEGREE COST ANALYSIS")
    print("="*80)
    
    # Print parameters table
    print("Parameters:")
    param_headers = ["Parameter", "Value"]
    param_data = [
        ["Start Year", params['start_year']],
        ["Degree Years", params['degree_years']],
        ["Annual Tuition", f"${params['annual_tuition']:,.2f}"],
        ["Enrollment Type", params['enrollment_type'].replace('_', ' ').title()],
        ["Inflation Rate", f"{params['inflation_rate']*100:.2f}%"]
    ]
    
    print(tabulate(param_data, headers=param_headers, tablefmt="simple", numalign="left"))
    
    # Print results summary
    print(f"\nCost Summary:")
    results_headers = ["Cost Category", "Nominal Value", "Real Value (Inflation-Adjusted)"]
    results_data = [
        ["Total Tuition", f"${analysis_data['total_tuition_nominal']:,.2f}", f"${analysis_data['total_tuition_real']:,.2f}"],
        ["Additional Costs (15%)", f"${analysis_data['additional_costs_nominal']:,.2f}", f"${analysis_data['additional_costs_real']:,.2f}"],
        ["Total Cost", f"${analysis_data['total_cost_nominal']:,.2f}", f"${analysis_data['total_cost_real']:,.2f}"]
    ]
    
    print(tabulate(results_data, headers=results_headers, tablefmt="simple", numalign="right"))
    
    # Print year-by-year breakdown
    print(f"\nYear-by-Year Breakdown:")
    headers = ["Year", "Tuition (Nominal)", "Tuition (Real)", "Cumulative (Nominal)", "Cumulative (Real)"]
    
    table_data = []
    for detail in year_details:
        table_data.append([
            detail['year'],
            f"${detail['tuition_nominal']:,.2f}",
            f"${detail['tuition_real']:,.2f}",
            f"${detail['cumulative_nominal']:,.2f}",
            f"${detail['cumulative_real']:,.2f}"
        ])
    
    print(tabulate(table_data, headers=headers, tablefmt="simple", numalign="right"))
    print("="*80)


def get_enrollment_type_options() -> List[str]:
    """
    Get available enrollment type options.
    
    Returns:
        List of enrollment type options
    """
    return ["full_time", "part_time"]


def get_enrollment_type_display_name(enrollment_type: str) -> str:
    """
    Get display name for enrollment type.
    
    Args:
        enrollment_type: Internal enrollment type value
        
    Returns:
        Display name for the enrollment type
    """
    display_names = {
        "full_time": "Full Time",
        "part_time": "Part Time"
    }
    return display_names.get(enrollment_type, enrollment_type.replace('_', ' ').title()) 