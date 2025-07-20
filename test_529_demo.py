#!/usr/bin/env python3
"""
Demonstration script for the 529 Plan Calculator
"""

from modules.masters.calc_529_savings import (
    calculate_529_growth,
    print_529_analysis,
    project_529_balance
)

def demonstrate_529_calculator():
    """Demonstrate the 529 plan calculator functionality"""
    
    print("=== 529 PLAN CALCULATOR DEMONSTRATION ===")
    print()
    
    # Example 1: Basic 529 growth with contributions
    print("Example 1: 529 Plan with Annual Contributions")
    print("-" * 50)
    
    result = calculate_529_growth(
        start_year=2025,
        years=10,
        starting_balance=25000,
        annual_contribution=5000,
        stock_market_return=0.07,
        inflation_rate=0.03,
        return_details=True
    )
    
    print_529_analysis(result)
    
    print("\n" + "="*80)
    print()
    
    # Example 2: 529 growth without contributions
    print("Example 2: 529 Plan Growth Only (No Contributions)")
    print("-" * 50)
    
    result_no_contrib = calculate_529_growth(
        start_year=2025,
        years=10,
        starting_balance=25000,
        annual_contribution=0,
        stock_market_return=0.07,
        inflation_rate=0.03,
        return_details=True
    )
    
    print_529_analysis(result_no_contrib)
    
    print("\n" + "="*80)
    print()
    
    # Example 3: Comparison of different scenarios
    print("Example 3: Comparison of Different Scenarios")
    print("-" * 50)
    
    scenarios = [
        ("Conservative (5% return)", 0.05),
        ("Moderate (7% return)", 0.07),
        ("Aggressive (9% return)", 0.09)
    ]
    
    for scenario_name, return_rate in scenarios:
        result = calculate_529_growth(
            start_year=2025,
            years=15,
            starting_balance=20000,
            annual_contribution=3000,
            stock_market_return=return_rate,
            inflation_rate=0.03
        )
        
        print(f"{scenario_name}:")
        print(f"  Final Balance: ${result['final_balance']:,.2f}")
        print(f"  Real Balance: ${result['final_balance_real']:,.2f}")
        print(f"  Total Contributions: ${result['total_contributions']:,.2f}")
        print(f"  Net Growth: ${result['net_growth']:,.2f}")
        print()
    
    print("="*80)
    print()
    
    # Example 4: Balance projection
    print("Example 4: 529 Balance Projection")
    print("-" * 50)
    
    balances = project_529_balance(
        start_year=2025,
        years=5,
        starting_balance=15000,
        annual_contribution=4000,
        stock_market_return=0.07
    )
    
    print("Year-by-Year Balance Projection:")
    for i, balance in enumerate(balances):
        year = 2025 + i
        print(f"  {year}: ${balance:,.2f}")

if __name__ == "__main__":
    demonstrate_529_calculator() 