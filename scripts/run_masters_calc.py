import argparse
import sys
import os

# Add the project root to the Python path so imports work from any directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from modules.masters.masters_constants import *
from modules.masters.calc_ira_savings import total_ira_contributions_over_years, get_historical_401k_growth_info, print_ira_analysis_table
from modules.masters.calc_total_savings import calculate_total_savings, print_total_savings_summary, print_detailed_breakdown

def get_user_input():
    """Get user input for calculation parameters"""
    print("IRA, 401k, and Brokerage Savings Calculator")
    print("=" * 40)
    
    # Default values
    defaults = {
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
    
    # Display current values
    print("Current Parameters:")
    print("-" * 80)
    
    # Prepare table data
    headers = ["#", "Parameter", "Value", "Type"]
    table_data = [
        ["1", "Start Year", defaults['start_year'], "Integer"],
        ["2", "Number of Years", defaults['years'], "Integer"],
        ["3", "Starting Age", defaults['age'], "Integer"],
        ["4", "Filing Status", defaults['filing_status'], "Text"],
        ["5", "Starting MAGI", f"${defaults['starting_magi']:,.0f}", "Currency"],
        ["6", "MAGI Growth Rate", f"{defaults['magi_growth_rate']*100:.2f}%", "Percentage"],
        ["7", "Plan Covered", "Yes" if defaults['plan_covered'] else "No", "Yes/No"],
        ["8", "Stock Market Return", f"{defaults['stock_market_return']*100:.2f}%", "Percentage"],
        ["9", "Starting 401k Balance", f"${defaults['starting_401k_balance']:,.0f}", "Currency"],
        ["10", "Inflation Rate", f"{defaults['inflation_rate']*100:.2f}%", "Percentage"],
        ["11", "Starting 401k Principal", f"${defaults['starting_401k_principal']:,.0f}", "Currency"],
        ["12", "401k Limit Growth Rate", f"{defaults['_401k_limit_growth_rate']*100:.2f}%", "Percentage"],
        ["13", "Starting Brokerage Balance", f"${defaults['starting_brokerage_balance']:,.0f}", "Currency"],
        ["14", "Annual Brokerage Contrib", f"${defaults['annual_brokerage_contribution']:,.0f}", "Currency"],
        ["15", "Brokerage Contrib Growth", f"{defaults['brokerage_contribution_growth_rate']*100:.2f}%", "Percentage"]
    ]
    
    from tabulate import tabulate
    print(tabulate(table_data, headers=headers, tablefmt="simple", numalign="left"))
    print()
    
    # Ask if user wants to change anything
    change_input = input("Do you want to change any values? (y/n, default: n): ").strip().lower()
    if change_input not in ['y', 'yes']:
        print("Using default values.")
        return defaults
    
    print("\nEnter the number of the parameter you want to change, or 'done' to finish:")
    
    # Copy defaults to working values
    values = defaults.copy()
    
    while True:
        try:
            choice = input("Parameter number (1-15) or 'done': ").strip().lower()
            
            if choice == 'done':
                break
            
            choice_num = int(choice)
            if choice_num < 1 or choice_num > 15:
                print("Please enter a number between 1 and 15.")
                continue
            
            # Map choice number to parameter name
            param_map = {
                1: 'start_year',
                2: 'years', 
                3: 'age',
                4: 'filing_status',
                5: 'starting_magi',
                6: 'magi_growth_rate',
                7: 'plan_covered',
                8: 'stock_market_return',
                9: 'starting_401k_balance',
                10: 'inflation_rate',
                11: 'starting_401k_principal',
                12: '_401k_limit_growth_rate',
                13: 'starting_brokerage_balance',
                14: 'annual_brokerage_contribution',
                15: 'brokerage_contribution_growth_rate'
            }
            
            param_name = param_map[choice_num]
            current_value = values[param_name]
            
            # Get new value based on parameter type
            if param_name == 'filing_status':
                new_value = input(f"Filing Status (current: {current_value}) - single/joint: ").strip()
                if new_value:
                    values[param_name] = new_value
            elif param_name == 'plan_covered':
                new_value = input(f"Plan Covered (current: {'Yes' if current_value else 'No'}) - y/n: ").strip().lower()
                if new_value:
                    values[param_name] = new_value in ['y', 'yes']
            elif param_name in ['magi_growth_rate', 'stock_market_return', 'inflation_rate', '_401k_limit_growth_rate', 'brokerage_contribution_growth_rate']:
                new_value = input(f"{param_name.replace('_', ' ').title()} (current: {current_value*100:.2f}%) - new value %: ").strip()
                if new_value:
                    values[param_name] = float(new_value) / 100
            elif param_name in ['starting_magi', 'starting_401k_balance', 'starting_401k_principal', 'starting_brokerage_balance', 'annual_brokerage_contribution']:
                new_value = input(f"{param_name.replace('_', ' ').title()} (current: ${current_value:,.0f}) - new value: ").strip()
                if new_value:
                    values[param_name] = float(new_value)
            else:
                new_value = input(f"{param_name.replace('_', ' ').title()} (current: {current_value}) - new value: ").strip()
                if new_value:
                    values[param_name] = int(new_value) if param_name in ['start_year', 'years', 'age'] else float(new_value)
            
            # Show updated value
            if param_name in ['magi_growth_rate', 'stock_market_return', 'inflation_rate', '_401k_limit_growth_rate', 'brokerage_contribution_growth_rate']:
                print(f"Updated {param_name.replace('_', ' ')}: {values[param_name]*100:.2f}%")
            elif param_name in ['starting_magi', 'starting_401k_balance', 'starting_401k_principal', 'starting_brokerage_balance', 'annual_brokerage_contribution']:
                print(f"Updated {param_name.replace('_', ' ')}: ${values[param_name]:,.0f}")
            elif param_name == 'plan_covered':
                print(f"Updated Plan Covered: {'Yes' if values[param_name] else 'No'}")
            else:
                print(f"Updated {param_name.replace('_', ' ')}: {values[param_name]}")
            print()
            
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nCancelled. Using default values.")
            return defaults
    
    print("Final Parameters:")
    print("-" * 80)
    
    # Prepare final table data
    final_table_data = [
        ["1", "Start Year", values['start_year'], "Integer"],
        ["2", "Number of Years", values['years'], "Integer"],
        ["3", "Starting Age", values['age'], "Integer"],
        ["4", "Filing Status", values['filing_status'], "Text"],
        ["5", "Starting MAGI", f"${values['starting_magi']:,.0f}", "Currency"],
        ["6", "MAGI Growth Rate", f"{values['magi_growth_rate']*100:.2f}%", "Percentage"],
        ["7", "Plan Covered", "Yes" if values['plan_covered'] else "No", "Yes/No"],
        ["8", "Stock Market Return", f"{values['stock_market_return']*100:.2f}%", "Percentage"],
        ["9", "Starting 401k Balance", f"${values['starting_401k_balance']:,.0f}", "Currency"],
        ["10", "Inflation Rate", f"{values['inflation_rate']*100:.2f}%", "Percentage"],
        ["11", "Starting 401k Principal", f"${values['starting_401k_principal']:,.0f}", "Currency"],
        ["12", "401k Limit Growth Rate", f"{values['_401k_limit_growth_rate']*100:.2f}%", "Percentage"],
        ["13", "Starting Brokerage Balance", f"${values['starting_brokerage_balance']:,.0f}", "Currency"],
        ["14", "Annual Brokerage Contrib", f"${values['annual_brokerage_contribution']:,.0f}", "Currency"],
        ["15", "Brokerage Contrib Growth", f"{values['brokerage_contribution_growth_rate']*100:.2f}%", "Percentage"]
    ]
    
    print(tabulate(final_table_data, headers=headers, tablefmt="simple", numalign="left"))
    print()
    
    return values

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Calculate IRA, 401k, and brokerage savings projections')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Print detailed year-by-year analysis table')
    args = parser.parse_args()

    # Always use interactive mode to get parameters
    params = get_user_input()
    print()  # Add spacing after user input

    # Get historical 401k growth information
    historical_info = get_historical_401k_growth_info()
    print(f"Historical 401k limit growth: {historical_info['start_value']:,} in {historical_info['start_year']} to {historical_info['end_value']:,} in {historical_info['end_year']} ({historical_info['years_elapsed']} years)")
    print(f"Calculated annual growth rate: {historical_info['growth_rate']*100:.2f}%")
    print()

    # Get IRA analysis (with or without details based on verbose flag)
    ira_analysis = total_ira_contributions_over_years(
        start_year=params['start_year'],
        years=params['years'],
        age=params['age'],
        filing_status=params['filing_status'],
        starting_magi=params['starting_magi'],
        magi_growth_rate=params['magi_growth_rate'],
        plan_covered=params['plan_covered'],
        stock_market_return=params['stock_market_return'],
        starting_401k_balance=params['starting_401k_balance'],
        _401k_growth_rate=params['_401k_limit_growth_rate'],
        inflation_rate=params['inflation_rate'],
        return_details=args.verbose
    )

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
        return_details=args.verbose
    )

    # Print total savings summary
    print_total_savings_summary(total_savings)
    
    # Print detailed breakdown if verbose
    if args.verbose:
        print_detailed_breakdown(total_savings)
        
        # Also print the original IRA analysis table
        print("\n" + "="*80)
        print("ORIGINAL IRA ANALYSIS")
        print("="*80)
        print_ira_analysis_table(ira_analysis)

if __name__ == "__main__":
    main()