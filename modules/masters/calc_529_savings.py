#!/usr/bin/env python3
"""
529 Plan Savings Calculator
Calculates growth in 529 education savings accounts with contributions and withdrawals.
"""

from typing import Dict, Any, List
from tabulate import tabulate


def calculate_529_growth(
    start_year: int,
    years: int,
    starting_balance: float,
    annual_contribution: float,
    stock_market_return: float,
    inflation_rate: float,
    return_details: bool
) -> Dict[str, Any]:
    """
    Calculate 529 plan growth over time with contributions.
    
    Args:
        start_year: First year of calculation
        years: Number of years to calculate
        starting_balance: Initial 529 account balance
        annual_contribution: Annual contribution amount (default 0)
        stock_market_return: Annual stock market return rate (default 7%)
        inflation_rate: Annual inflation rate (default 3%)
        return_details: If True, return detailed year-by-year breakdown
        
    Returns:
        Dictionary containing 529 growth breakdown
    """
    
    current_balance = starting_balance
    total_contributions = 0.0
    year_details = []
    
    # Calculate real return (nominal return minus inflation)
    real_return = stock_market_return - inflation_rate
    
    for i in range(years):
        year = start_year + i
        
        # Apply growth to existing balance
        current_balance *= (1 + stock_market_return)
        
        # Add this year's contribution
        current_balance += annual_contribution
        total_contributions += annual_contribution
        
        # Calculate real balance (inflation-adjusted)
        real_balance = current_balance / ((1 + inflation_rate) ** (i + 1))
        
        # Store year details if requested
        if return_details:
            year_details.append({
                'year': year,
                'contribution': annual_contribution,
                'balance': current_balance,
                'balance_real': real_balance,
                'total_contributions': total_contributions
            })
    
    # Calculate final real balance
    final_balance_real = current_balance / ((1 + inflation_rate) ** years)
    
    results = {
        'final_balance': current_balance,
        'final_balance_real': final_balance_real,
        'total_contributions': total_contributions,
        'net_growth': current_balance - starting_balance - total_contributions,
        'parameters': {
            'start_year': start_year,
            'years': years,
            'starting_balance': starting_balance,
            'annual_contribution': annual_contribution,
            'stock_market_return': stock_market_return,
            'inflation_rate': inflation_rate,
            'real_return': real_return
        }
    }
    
    if return_details:
        results['year_details'] = year_details
    
    return results


def print_529_analysis(analysis_data: dict) -> None:
    """
    Print a formatted table showing 529 plan analysis.
    
    Args:
        analysis_data: Dictionary returned from calculate_529_growth with return_details=True
    """
    params = analysis_data['parameters']
    year_details = analysis_data['year_details']
    
    print("\n" + "="*80)
    print("529 PLAN ANALYSIS")
    print("="*80)
    
    # Print parameters table
    print("Parameters:")
    param_headers = ["Parameter", "Value"]
    param_data = [
        ["Start Year", params['start_year']],
        ["Years", params['years']],
        ["Starting Balance", f"${params['starting_balance']:,.2f}"],
        ["Annual Contribution", f"${params['annual_contribution']:,.2f}"],
        ["Stock Market Return", f"{params['stock_market_return']*100:.2f}%"],
        ["Inflation Rate", f"{params['inflation_rate']*100:.2f}%"],
        ["Real Return", f"{params['real_return']*100:.2f}%"]
    ]
    
    print(tabulate(param_data, headers=param_headers, tablefmt="simple", numalign="left"))
    
    # Print results summary
    print(f"\nResults Summary:")
    results_headers = ["Metric", "Value"]
    results_data = [
        ["Final Balance (Nominal)", f"${analysis_data['final_balance']:,.2f}"],
        ["Final Balance (Real)", f"${analysis_data['final_balance_real']:,.2f}"],
        ["Total Contributions", f"${analysis_data['total_contributions']:,.2f}"],
        ["Net Growth", f"${analysis_data['net_growth']:,.2f}"]
    ]
    
    print(tabulate(results_data, headers=results_headers, tablefmt="simple", numalign="right"))
    
    # Print year-by-year breakdown
    print(f"\nYear-by-Year Breakdown:")
    headers = ["Year", "Contribution", "Balance", "Real Balance", "Total Contributions"]
    
    table_data = []
    for detail in year_details:
        table_data.append([
            detail['year'],
            f"${detail['contribution']:,.0f}",
            f"${detail['balance']:,.0f}",
            f"${detail['balance_real']:,.0f}",
            f"${detail['total_contributions']:,.0f}"
        ])
    
    print(tabulate(table_data, headers=headers, tablefmt="simple", numalign="right"))
    print("="*80)


def project_529_balance(
    start_year: int,
    years: int,
    starting_balance: float,
    annual_contribution: float,
    stock_market_return: float
) -> List[float]:
    """
    Project 529 account balance over years, returning list of balances for each year.
    
    Args:
        start_year: First year of calculation
        years: Number of years to calculate
        starting_balance: Initial 529 account balance
        annual_contribution: Annual contribution amount
        stock_market_return: Annual stock market return rate
        
    Returns:
        List of balances for each year
    """
    balances = []
    current_balance = starting_balance
    
    for i in range(years):
        # Apply growth to existing balance
        current_balance *= (1 + stock_market_return)
        
        # Add this year's contribution
        current_balance += annual_contribution
        
        balances.append(current_balance)
    
    return balances 