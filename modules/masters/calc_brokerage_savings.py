#!/usr/bin/env python3
"""
Brokerage Account Savings Calculator
Calculates growth in individual brokerage accounts with both nominal and real values.
"""

from typing import Dict, Any, List


def calculate_brokerage_growth(
    start_year: int,
    years: int,
    starting_balance: float,
    annual_contribution: float,
    contribution_growth_rate: float = 0.03,
    stock_market_return: float = 0.07,
    inflation_rate: float = 0.03,
    # Master's degree parameters
    masters_degree_enabled: bool = False,
    masters_start_year: int = None,
    masters_degree_years: int = 0,
    masters_enrollment_type: str = "full_time",
    return_details: bool = False
) -> Dict[str, Any]:
    """
    Calculate brokerage account growth over time.
    
    Args:
        start_year: First year of calculation
        years: Number of years to calculate
        starting_balance: Initial brokerage account balance
        annual_contribution: Annual contribution amount
        contribution_growth_rate: Annual growth rate for contributions (default 3%)
        stock_market_return: Annual stock market return rate (default 7%)
        inflation_rate: Annual inflation rate (default 3%)
        masters_degree_enabled: Whether master's degree is enabled
        masters_start_year: Year when master's degree starts
        masters_degree_years: Number of years for master's degree
        masters_enrollment_type: "full_time" or "part_time"
        return_details: If True, return detailed year-by-year breakdown
        
    Returns:
        Dictionary containing brokerage growth breakdown
    """
    
    current_balance = starting_balance
    current_balance_real = starting_balance
    year_details = []
    
    # Calculate real return (nominal return minus inflation)
    real_return = stock_market_return - inflation_rate
    
    for i in range(years):
        year = start_year + i
        
        # Calculate contribution for this year (with growth)
        current_contribution = annual_contribution * ((1 + contribution_growth_rate) ** i)
        
        # Apply master's degree logic: full-time enrollment stops brokerage contributions
        if masters_degree_enabled and masters_start_year is not None and masters_start_year <= year < masters_start_year + masters_degree_years:
            if masters_enrollment_type == "full_time":
                current_contribution = 0.0  # No brokerage contributions during full-time degree
        
        # Apply growth to existing balance
        current_balance *= (1 + stock_market_return)
        current_balance_real *= (1 + real_return)
        
        # Add this year's contribution
        current_balance += current_contribution
        current_balance_real += current_contribution
        
        # Store year details if requested
        if return_details:
            year_details.append({
                'year': year,
                'contribution': current_contribution,
                'balance': current_balance,
                'balance_real': current_balance_real,
                'future_value': current_balance,
                'future_value_real': current_balance_real
            })
    
    # Calculate final real balance (inflation-adjusted)
    final_balance_real = current_balance / ((1 + inflation_rate) ** years)
    
    results = {
        'total_accumulated': current_balance,
        'total_accumulated_real': current_balance_real,
        'final_balance': current_balance,
        'final_balance_real': final_balance_real,
        'parameters': {
            'start_year': start_year,
            'years': years,
            'starting_balance': starting_balance,
            'annual_contribution': annual_contribution,
            'contribution_growth_rate': contribution_growth_rate,
            'stock_market_return': stock_market_return,
            'inflation_rate': inflation_rate,
            'real_return': real_return,
            'masters_degree_enabled': masters_degree_enabled,
            'masters_start_year': masters_start_year,
            'masters_degree_years': masters_degree_years,
            'masters_enrollment_type': masters_enrollment_type
        }
    }
    
    if return_details:
        results['year_details'] = year_details
    
    return results


def project_brokerage_balance(
    start_year: int,
    years: int,
    starting_balance: float,
    annual_contribution: float,
    contribution_growth_rate: float = 0.03,
    stock_market_return: float = 0.07
) -> List[float]:
    """
    Project brokerage account balance over years, returning list of balances for each year.
    
    Args:
        start_year: First year of calculation
        years: Number of years to calculate
        starting_balance: Initial brokerage account balance
        annual_contribution: Annual contribution amount
        contribution_growth_rate: Annual growth rate for contributions (default 3%)
        stock_market_return: Annual stock market return rate (default 7%)
        
    Returns:
        List of balances for each year
    """
    balances = []
    current_balance = starting_balance
    
    for i in range(years):
        # Calculate contribution for this year (with growth)
        current_contribution = annual_contribution * ((1 + contribution_growth_rate) ** i)
        
        # Apply growth to existing balance
        current_balance *= (1 + stock_market_return)
        
        # Add this year's contribution
        current_balance += current_contribution
        
        balances.append(current_balance)
    
    return balances


def print_brokerage_analysis_table(analysis_data: dict) -> None:
    """
    Print a formatted table showing year-by-year brokerage analysis.
    
    Args:
        analysis_data: Dictionary returned from calculate_brokerage_growth with return_details=True
    """
    params = analysis_data['parameters']
    year_details = analysis_data['year_details']
    
    print("\n" + "="*100)
    print("BROKERAGE ACCOUNT ANALYSIS")
    print("="*100)
    
    # Print parameters table
    print(f"Parameters:")
    param_headers = ["Parameter", "Value"]
    param_data = [
        ["Start Year", params['start_year']],
        ["Years", params['years']],
        ["Starting Balance", f"${params['starting_balance']:,.2f}"],
        ["Annual Contribution", f"${params['annual_contribution']:,.2f}"],
        ["Contribution Growth Rate", f"{params['contribution_growth_rate']*100:.2f}%"],
        ["Stock Market Return", f"{params['stock_market_return']*100:.2f}%"],
        ["Inflation Rate", f"{params['inflation_rate']*100:.2f}%"],
        ["Real Return", f"{params['real_return']*100:.2f}%"]
    ]
    
    from tabulate import tabulate
    print(tabulate(param_data, headers=param_headers, tablefmt="simple", numalign="left"))
    
    # Print results table
    print(f"\nResults:")
    results_headers = ["Metric", "Value"]
    results_data = [
        ["Final Balance (Nominal)", f"${analysis_data['final_balance']:,.2f}"],
        ["Final Balance (Real)", f"${analysis_data['final_balance_real']:,.2f}"],
        ["Total Accumulated (Nominal)", f"${analysis_data['total_accumulated']:,.2f}"],
        ["Total Accumulated (Real)", f"${analysis_data['total_accumulated_real']:,.2f}"]
    ]
    
    print(tabulate(results_data, headers=results_headers, tablefmt="simple", numalign="right"))
    
    # Create table headers
    headers = [
        "Year", "Contribution", "Balance", "Balance (Real)", 
        "Years to Grow", "Future Value", "Future Value (Real)"
    ]
    
    # Prepare table data
    table_data = []
    for year_data in year_details:
        table_data.append([
            year_data['year'],
            f"${year_data['contribution']:,.0f}",
            f"${year_data['balance']:,.0f}",
            f"${year_data['balance_real']:,.0f}",
            year_data['years_to_grow'],
            f"${year_data['future_value']:,.0f}",
            f"${year_data['future_value_real']:,.0f}"
        ])
    
    # Print table
    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))


def print_brokerage_summary(results: dict) -> None:
    """
    Print a formatted summary of brokerage account growth.
    
    Args:
        results: Results dictionary from calculate_brokerage_growth
    """
    params = results['parameters']
    
    print("\n" + "="*80)
    print("BROKERAGE ACCOUNT SUMMARY")
    print("="*80)
    
    # Print parameters table
    print(f"Parameters:")
    param_headers = ["Parameter", "Value"]
    param_data = [
        ["Start Year", params['start_year']],
        ["Years", params['years']],
        ["Starting Balance", f"${params['starting_balance']:,.0f}"],
        ["Annual Contribution", f"${params['annual_contribution']:,.0f}"],
        ["Contribution Growth Rate", f"{params['contribution_growth_rate']*100:.2f}%"],
        ["Stock Market Return", f"{params['stock_market_return']*100:.2f}%"],
        ["Inflation Rate", f"{params['inflation_rate']*100:.2f}%"]
    ]
    
    from tabulate import tabulate
    print(tabulate(param_data, headers=param_headers, tablefmt="simple", numalign="left"))
    
    # Print results table
    print(f"\nResults:")
    results_headers = ["Metric", "Value"]
    results_data = [
        ["Final Balance (Nominal)", f"${results['final_balance']:,.0f}"],
        ["Final Balance (Real)", f"${results['final_balance_real']:,.0f}"],
        ["Total Accumulated (Nominal)", f"${results['total_accumulated']:,.0f}"],
        ["Total Accumulated (Real)", f"${results['total_accumulated_real']:,.0f}"]
    ]
    
    print(tabulate(results_data, headers=results_headers, tablefmt="simple", numalign="right"))
    print("="*80) 