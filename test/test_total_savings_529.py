#!/usr/bin/env python3
"""
Quick test for total savings calculation with 529 parameters
"""

from modules.masters.calc_total_savings import calculate_total_savings

def test_total_savings_with_529():
    """Test total savings calculation with 529 parameters"""
    
    print("Testing total savings calculation with 529 parameters...")
    
    results = calculate_total_savings(
        start_year=2025,
        years=10,
        age=30,
        filing_status='single',
        starting_magi=80000,
        magi_growth_rate=0.05,
        plan_covered=True,
        stock_market_return=0.07,
        starting_401k_balance=50000,
        starting_401k_principal=50000,
        inflation_rate=0.03,
        starting_brokerage_balance=10000,
        annual_brokerage_contribution=5000,
        # 529 parameters
        starting_529_balance=25000,
        masters_degree_enabled=True,
        masters_start_year=2027,
        masters_degree_years=2,
        masters_annual_tuition=30000,
        masters_enrollment_type="full_time",
        masters_employer_contribution=5000
    )
    
    print("Results keys:", list(results.keys()))
    print()
    
    print("Savings Breakdown:")
    print(f"  IRA Accumulated (Nominal): ${results['ira_nominal']:,.2f}")
    print(f"  IRA Accumulated (Real): ${results['ira_real']:,.2f}")
    print(f"  401k Final Balance (Nominal): ${results['401k_nominal']:,.2f}")
    print(f"  IRA Final Balance (Real): ${results['401k_real']:,.2f}")
    print(f"  401k Total Contributions: ${results['401k_contributions']:,.2f}")
    print(f"  Brokerage Final Balance (Nominal): ${results['brokerage_nominal']:,.2f}")
    print(f"  Brokerage Final Balance (Real): ${results['brokerage_real']:,.2f}")
    print(f"  529 Final Balance (Nominal): ${results['529_nominal']:,.2f}")
    print(f"  529 Final Balance (Real): ${results['529_real']:,.2f}")
    print(f"  Total Savings (Nominal): ${results['total_nominal']:,.2f}")
    print(f"  Total Savings (Real): ${results['total_real']:,.2f}")
    
    print("\n529 Yearly Balances:")
    for i, balance in enumerate(results['529_yearly']):
        year = 2025 + i
        print(f"  {year}: ${balance:,.2f}")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_total_savings_with_529() 