#!/usr/bin/env python3
"""
Total Savings Calculator
Calculates combined savings from IRA, 401k, and brokerage accounts with both nominal and real values.
"""

from typing import Dict, Any
from .calc_ira_savings import total_ira_contributions_over_years, get_historical_401k_growth_info
from .calc_brokerage_savings import calculate_brokerage_growth


def calculate_529_withdrawal_tax(balance_529: float, filing_status: str) -> float:
    """
    Calculate tax on 529 withdrawal based on 2025 California and Federal tax brackets plus 10% penalty.
    
    Args:
        balance_529: The 529 balance to be withdrawn
        filing_status: Filing status for tax calculation
        
    Returns:
        Total tax amount (California + Federal + 10% penalty)
    """
    # 2025 Federal Tax Brackets (Single)
    federal_brackets_single = [
        (0, 11600, 0.10),
        (11600, 47150, 0.12),
        (47150, 100525, 0.22),
        (100525, 191950, 0.24),
        (191950, 243725, 0.32),
        (243725, 609350, 0.35),
        (609350, float('inf'), 0.37)
    ]
    
    # 2025 Federal Tax Brackets (Joint)
    federal_brackets_joint = [
        (0, 23200, 0.10),
        (23200, 94300, 0.12),
        (94300, 201050, 0.22),
        (201050, 383900, 0.24),
        (383900, 487450, 0.32),
        (487450, 731200, 0.35),
        (731200, float('inf'), 0.37)
    ]
    
    # 2025 California Tax Brackets (Single)
    california_brackets_single = [
        (0, 10099, 0.01),
        (10099, 23942, 0.02),
        (23942, 37788, 0.04),
        (37788, 52455, 0.06),
        (52455, 66295, 0.08),
        (66295, 338639, 0.093),
        (338639, 406364, 0.103),
        (406364, 677275, 0.113),
        (677275, float('inf'), 0.123)
    ]
    
    # 2025 California Tax Brackets (Joint)
    california_brackets_joint = [
        (0, 20198, 0.01),
        (20198, 47884, 0.02),
        (47884, 75576, 0.04),
        (75576, 104910, 0.06),
        (104910, 132590, 0.08),
        (132590, 677278, 0.093),
        (677278, 812728, 0.103),
        (812728, 1354550, 0.113),
        (1354550, float('inf'), 0.123)
    ]
    
    # Select appropriate brackets based on filing status
    if filing_status == "joint":
        federal_brackets = federal_brackets_joint
        california_brackets = california_brackets_joint
    else:
        federal_brackets = federal_brackets_single
        california_brackets = california_brackets_single
    
    # Calculate Federal tax
    federal_tax = 0
    remaining_income = balance_529
    for bracket_min, bracket_max, rate in federal_brackets:
        if remaining_income <= 0:
            break
        taxable_in_bracket = min(remaining_income, bracket_max - bracket_min)
        federal_tax += taxable_in_bracket * rate
        remaining_income -= taxable_in_bracket
    
    # Calculate California tax
    california_tax = 0
    remaining_income = balance_529
    for bracket_min, bracket_max, rate in california_brackets:
        if remaining_income <= 0:
            break
        taxable_in_bracket = min(remaining_income, bracket_max - bracket_min)
        california_tax += taxable_in_bracket * rate
        remaining_income -= taxable_in_bracket
    
    # 10% penalty for non-qualified withdrawal
    penalty = balance_529 * 0.10
    
    total_tax = federal_tax + california_tax + penalty
    return total_tax


def calculate_total_savings(
    start_year: int,
    years: int,
    age: int,
    filing_status: str,
    starting_magi: float,
    magi_growth_rate: float,
    plan_covered: bool,
    stock_market_return: float,
    starting_401k_balance: float,
    starting_401k_principal: float,
    inflation_rate: float,
    _401k_limit_growth_rate: float,
    starting_brokerage_balance: float,
    annual_brokerage_contribution: float,
    brokerage_contribution_growth_rate: float,
    # New 529 and master's degree params
    starting_529_balance: float,
    annual_529_contribution: float,
    _529_contribution_growth_rate: float,
    annual_living_expenses: float,
    masters_degree_enabled: bool,
    masters_start_year: int,
    masters_degree_years: int,
    masters_annual_tuition: float,
    masters_enrollment_type: str,
    masters_employer_contribution: float,
    ft_annual_living_expenses: float,
    pt_annual_living_expenses: float,
    return_details: bool,
) -> Dict[str, Any]:
    """
    Calculate total accumulated savings from IRA, 401k, brokerage, and 529 (with master's tuition subtraction).
    
    Args:
        start_year: First year of calculation
        years: Number of years to calculate
        age: Starting age
        filing_status: Tax filing status ('single', 'joint', 'separate_lived')
        starting_magi: Starting Modified Adjusted Gross Income
        magi_growth_rate: Annual MAGI growth rate (default 5%)
        plan_covered: Whether covered by workplace retirement plan
        stock_market_return: Annual stock market return rate (default 7%)
        starting_401k_balance: Starting 401k balance
        starting_401k_principal: Starting 401k principal for contribution calculations
        inflation_rate: Annual inflation rate (default 3%)
        _401k_limit_growth_rate: 401k limit growth rate (default: historical)
        starting_brokerage_balance: Starting brokerage account balance
        annual_brokerage_contribution: Annual brokerage contribution amount
        brokerage_contribution_growth_rate: Annual growth rate for brokerage contributions (default 3%)
        return_details: If True, return detailed breakdown
        
    Returns:
        Dictionary containing total savings breakdown
    """
    
    # Calculate IRA savings with master's degree consideration
    ira_results = total_ira_contributions_over_years(
        start_year=start_year,
        years=years,
        age=age,
        filing_status=filing_status,
        starting_magi=starting_magi,
        magi_growth_rate=magi_growth_rate,
        plan_covered=plan_covered,
        stock_market_return=stock_market_return,
        starting_401k_balance=starting_401k_balance,
        inflation_rate=inflation_rate,
        _401k_growth_rate=_401k_limit_growth_rate,
        # Master's degree parameters
        masters_degree_enabled=masters_degree_enabled,
        masters_start_year=masters_start_year,
        masters_degree_years=masters_degree_years,
        masters_enrollment_type=masters_enrollment_type,
        return_details=True
    )
    
    # Calculate 401k contributions with master's degree consideration
    # Use historical growth rate if none provided
    if _401k_limit_growth_rate is None:
        from .calc_ira_savings import calculate_historical_401k_growth_rate
        _401k_limit_growth_rate = calculate_historical_401k_growth_rate()
    
    # Calculate total 401k contributions considering master's degree impact
    _401k_contributions = 0.0
    for i in range(years):
        year = start_year + i
        current_age = age + i
        
        # Get this year's 401k contribution limit
        from .calc_ira_savings import projected_401k_limit, projected_401k_catchup
        base_limit = projected_401k_limit(year, growth_rate=_401k_limit_growth_rate)
        catch_up = projected_401k_catchup(year, growth_rate=_401k_limit_growth_rate) if current_age >= 50 else 0
        annual_contribution = base_limit + catch_up
        
        # Apply master's degree logic: full-time enrollment stops contributions
        if masters_degree_enabled and masters_start_year is not None and masters_start_year <= year < masters_start_year + masters_degree_years:
            if masters_enrollment_type == "full_time":
                annual_contribution = 0.0  # No contributions during full-time degree
        
        _401k_contributions += annual_contribution
    
    # Calculate 401k final balance (including growth on contributions)
    # We need to calculate the future value of 401k contributions with compound growth
    _401k_final_balance = starting_401k_balance
    
    # Project 401k balance year by year with master's degree consideration
    for i in range(years):
        year = start_year + i
        current_age = age + i
        
        # Get this year's 401k contribution limit
        from .calc_ira_savings import projected_401k_limit, projected_401k_catchup
        base_limit = projected_401k_limit(year, growth_rate=_401k_limit_growth_rate)
        catch_up = projected_401k_catchup(year, growth_rate=_401k_limit_growth_rate) if current_age >= 50 else 0
        annual_contribution = base_limit + catch_up
        
        # Apply master's degree logic: full-time enrollment stops contributions
        if masters_degree_enabled and masters_start_year is not None and masters_start_year <= year < masters_start_year + masters_degree_years:
            if masters_enrollment_type == "full_time":
                annual_contribution = 0.0  # No contributions during full-time degree
        
        # Apply growth to existing balance
        _401k_final_balance *= (1 + stock_market_return)
        
        # Add this year's contribution
        _401k_final_balance += annual_contribution
    
    # Calculate real (inflation-adjusted) 401k balance
    _401k_final_balance_real = _401k_final_balance / ((1 + inflation_rate) ** years)
    
    # Calculate brokerage account growth with master's degree consideration
    brokerage_results = calculate_brokerage_growth(
        start_year=start_year,
        years=years,
        starting_balance=starting_brokerage_balance,
        annual_contribution=annual_brokerage_contribution,
        contribution_growth_rate=brokerage_contribution_growth_rate,
        stock_market_return=stock_market_return,
        inflation_rate=inflation_rate,
        # Master's degree parameters
        masters_degree_enabled=masters_degree_enabled,
        masters_start_year=masters_start_year,
        masters_degree_years=masters_degree_years,
        masters_enrollment_type=masters_enrollment_type,
        return_details=True
    )
    
    # Extract values
    ira_nominal = ira_results['total_accumulated']
    ira_real = ira_results['total_accumulated_real']
    brokerage_nominal = brokerage_results['final_balance']
    brokerage_real = brokerage_results['final_balance_real']
    
    # 529 plan logic with master's degree tuition subtraction
    _529_balance = starting_529_balance
    _529_yearly = []
    for i in range(years):
        year = start_year + i
        
        # Calculate contribution for this year (with growth)
        current_contribution = annual_529_contribution * ((1 + _529_contribution_growth_rate) ** i)
        
        # Apply growth to existing 529 balance
        _529_balance *= (1 + stock_market_return)
        
        # Add this year's contribution
        _529_balance += current_contribution
        
        # Subtract master's tuition if enabled and within degree years
        tuition_this_year = 0.0
        living_expenses_this_year = 0.0
        if masters_degree_enabled and masters_start_year is not None and masters_start_year <= year < masters_start_year + masters_degree_years:
            # Calculate tuition for this year (with inflation)
            tuition_this_year = masters_annual_tuition * ((1 + inflation_rate) ** (year - masters_start_year))
            # Adjust for enrollment type
            if masters_enrollment_type == "part_time":
                tuition_this_year *= 0.7
            # Subtract employer contribution
            tuition_this_year -= masters_employer_contribution
            tuition_this_year = max(tuition_this_year, 0.0)
            
            # Calculate living expenses based on enrollment type
            if masters_enrollment_type == "full_time":
                living_expenses_this_year = ft_annual_living_expenses * ((1 + inflation_rate) ** (year - masters_start_year))  # Full-time has living expenses
            else:
                living_expenses_this_year = pt_annual_living_expenses * ((1 + inflation_rate) ** (year - masters_start_year))  # Part-time has living expenses too
        
        _529_balance -= tuition_this_year
        _529_balance -= living_expenses_this_year
        _529_balance = max(_529_balance, 0.0)  # Cannot go below zero
        _529_yearly.append(_529_balance)
    
    # Calculate totals (exclude 529 from annual totals, add at end minus taxes)
    total_nominal = ira_nominal + _401k_final_balance + brokerage_nominal
    total_real = ira_real + _401k_final_balance_real + brokerage_real
    
    # Calculate 529 withdrawal tax
    _529_tax = calculate_529_withdrawal_tax(_529_balance, filing_status)
    _529_after_tax = _529_balance - _529_tax
    
    # Add 529 after-tax amount to totals
    total_nominal += _529_after_tax
    total_real += _529_after_tax / ((1 + inflation_rate) ** years)
    
    # Prepare results
    results = {
        'ira_nominal': ira_nominal,
        'ira_real': ira_real,
        '401k_nominal': _401k_final_balance,
        '401k_real': _401k_final_balance_real,
        '401k_contributions': _401k_contributions,
        'brokerage_nominal': brokerage_nominal,
        'brokerage_real': brokerage_real,
        '529_nominal': _529_balance,
        '529_real': _529_balance / ((1 + inflation_rate) ** years),
        '529_tax': _529_tax,
        '529_after_tax': _529_after_tax,
        '529_yearly': _529_yearly,
        'total_nominal': total_nominal,
        'total_real': total_real,
        'parameters': {
            'start_year': start_year,
            'years': years,
            'age': age,
            'filing_status': filing_status,
            'starting_magi': starting_magi,
            'magi_growth_rate': magi_growth_rate,
            'plan_covered': plan_covered,
            'stock_market_return': stock_market_return,
            'starting_401k_balance': starting_401k_balance,
            'starting_401k_principal': starting_401k_principal,
            'inflation_rate': inflation_rate,
            '_401k_limit_growth_rate': _401k_limit_growth_rate,
            'starting_brokerage_balance': starting_brokerage_balance,
            'annual_brokerage_contribution': annual_brokerage_contribution,
            'brokerage_contribution_growth_rate': brokerage_contribution_growth_rate,
            'starting_529_balance': starting_529_balance,
            'annual_529_contribution': annual_529_contribution,
            '_529_contribution_growth_rate': _529_contribution_growth_rate,
            'annual_living_expenses': annual_living_expenses,
            'masters_degree_enabled': masters_degree_enabled,
            'masters_start_year': masters_start_year,
            'masters_degree_years': masters_degree_years,
            'masters_annual_tuition': masters_annual_tuition,
            'masters_enrollment_type': masters_enrollment_type,
            'masters_employer_contribution': masters_employer_contribution
        }
    }
    
    if return_details:
        results['ira_details'] = ira_results
        results['brokerage_details'] = brokerage_results
        results['yearly_breakdown'] = []
        
        # Create yearly breakdown combining IRA, 401k, and brokerage
        for i, ira_year in enumerate(ira_results['year_details']):
            year = start_year + i
            current_age = age + i
            
            # Calculate 401k balance for this year
            if i == 0:
                # For first year, start with initial balance, apply growth, then add contribution
                _401k_balance = starting_401k_balance * (1 + stock_market_return)
            else:
                # Start with the previous year's balance
                prev_year_data = results['yearly_breakdown'][i - 1]
                _401k_balance = prev_year_data['401k_balance']
                
                # Apply growth to existing balance
                _401k_balance *= (1 + stock_market_return)
            
            # Add this year's contribution
            contrib_year = start_year + i
            contrib_age = age + i
            base_limit = projected_401k_limit(contrib_year, growth_rate=_401k_limit_growth_rate)
            catch_up = projected_401k_catchup(contrib_year, growth_rate=_401k_limit_growth_rate) if contrib_age >= 50 else 0
            annual_contribution = base_limit + catch_up
            
            # Apply master's degree logic: full-time enrollment stops contributions
            if masters_degree_enabled and masters_start_year is not None and masters_start_year <= contrib_year < masters_start_year + masters_degree_years:
                if masters_enrollment_type == "full_time":
                    annual_contribution = 0.0  # No contributions during full-time degree
            
            _401k_balance += annual_contribution
            
            # Get brokerage data for this year
            brokerage_year = brokerage_results['year_details'][i]
            
            # Calculate 529 withdrawals for this year
            tuition_this_year = 0.0
            living_expenses_this_year = 0.0
            if masters_degree_enabled and masters_start_year is not None and masters_start_year <= year < masters_start_year + masters_degree_years:
                # Calculate tuition for this year (with inflation)
                tuition_this_year = masters_annual_tuition * ((1 + inflation_rate) ** (year - masters_start_year))
                # Adjust for enrollment type
                if masters_enrollment_type == "part_time":
                    tuition_this_year *= 0.7
                # Subtract employer contribution
                tuition_this_year -= masters_employer_contribution
                tuition_this_year = max(tuition_this_year, 0.0)
                
                # Calculate living expenses based on enrollment type
                if masters_enrollment_type == "full_time":
                    living_expenses_this_year = ft_annual_living_expenses * ((1 + inflation_rate) ** (year - masters_start_year))  # Full-time has living expenses
                else:
                    living_expenses_this_year = pt_annual_living_expenses * ((1 + inflation_rate) ** (year - masters_start_year))  # Part-time has living expenses too
            
            results['yearly_breakdown'].append({
                'year': year,
                'age': current_age,
                'ira_contribution': ira_year['ira_contribution'],
                'ira_future_value': ira_year['future_value'],
                'ira_future_value_real': ira_year['future_value_real'],
                '401k_balance': _401k_balance,
                '401k_balance_real': _401k_balance / ((1 + inflation_rate) ** (i + 1)),
                'brokerage_contribution': brokerage_year['contribution'],
                'brokerage_balance': brokerage_year['balance'],
                'brokerage_balance_real': brokerage_year['balance_real'],
                'total_balance': ira_year['future_value'] + _401k_balance + brokerage_year['balance'],
                'total_balance_real': ira_year['future_value_real'] + (_401k_balance / ((1 + inflation_rate) ** (i + 1))) + brokerage_year['balance_real'],
                '529_balance': _529_yearly[i],
                '529_tuition_withdrawal': tuition_this_year,
                '529_living_withdrawal': living_expenses_this_year
            })
    
    return results


def print_total_savings_summary(results: Dict[str, Any]) -> None:
    """
    Print a formatted summary of total savings.
    
    Args:
        results: Results dictionary from calculate_total_savings
    """
    params = results['parameters']
    
    print("\n" + "="*80)
    print("TOTAL SAVINGS SUMMARY")
    print("="*80)
    
    # Print parameters table
    print("\nParameters:")
    param_headers = ["Parameter", "Value"]
    param_data = [
        ["Start Year", params['start_year']],
        ["Years", params['years']],
        ["Starting Age", params['age']],
        ["Filing Status", params['filing_status']],
        ["Starting MAGI", f"${params['starting_magi']:,.0f}"],
        ["MAGI Growth Rate", f"{params['magi_growth_rate']*100:.2f}%"],
        ["Plan Covered", str(params['plan_covered'])],
        ["Stock Market Return", f"{params['stock_market_return']*100:.2f}%"],
        ["Inflation Rate", f"{params['inflation_rate']*100:.2f}%"],
        ["Starting 401k Balance", f"${params['starting_401k_balance']:,.0f}"],
        ["Starting 401k Principal", f"${params['starting_401k_principal']:,.0f}"],
        ["Starting Brokerage Balance", f"${params['starting_brokerage_balance']:,.0f}"],
        ["Annual Brokerage Contribution", f"${params['annual_brokerage_contribution']:,.0f}"],
        ["Brokerage Contribution Growth Rate", f"{params['brokerage_contribution_growth_rate']*100:.2f}%"],
        ["Starting 529 Balance", f"${params['starting_529_balance']:,.0f}"],
        ["Masters Degree Enabled", str(params['masters_degree_enabled'])],
        ["Masters Start Year", params['masters_start_year']],
        ["Masters Degree Years", params['masters_degree_years']],
        ["Masters Annual Tuition", f"${params['masters_annual_tuition']:,.0f}"],
        ["Masters Enrollment Type", params['masters_enrollment_type']],
        ["Masters Employer Contribution", f"${params['masters_employer_contribution']:,.0f}"]
    ]
    
    from tabulate import tabulate
    print(tabulate(param_data, headers=param_headers, tablefmt="simple", numalign="left"))
    
    # Print savings breakdown table
    print("\nSavings Breakdown:")
    savings_headers = ["Account Type", "Nominal Value", "Real Value"]
    savings_data = [
        ["IRA Accumulated", f"${results['ira_nominal']:,.2f}", f"${results['ira_real']:,.2f}"],
        ["401k Final Balance", f"${results['401k_nominal']:,.2f}", f"${results['401k_real']:,.2f}"],
        ["401k Total Contributions", f"${results['401k_contributions']:,.2f}", "N/A"],
        ["Brokerage Final Balance", f"${results['brokerage_nominal']:,.2f}", f"${results['brokerage_real']:,.2f}"],
        ["529 Final Balance", f"${results['529_nominal']:,.2f}", f"${results['529_real']:,.2f}"]
    ]
    
    print(tabulate(savings_data, headers=savings_headers, tablefmt="simple", numalign="right"))
    
    # Print total summary
    print(f"\nTOTAL SAVINGS:")
    total_headers = ["Metric", "Value"]
    total_data = [
        ["Nominal Value", f"${results['total_nominal']:,.2f}"],
        ["Real Value (Inflation-Adjusted)", f"${results['total_real']:,.2f}"],
        ["Real Value as % of Nominal", f"{(results['total_real']/results['total_nominal']*100):.1f}%"]
    ]
    
    print(tabulate(total_data, headers=total_headers, tablefmt="simple", numalign="right"))
    print("="*80)


def print_detailed_breakdown(results: Dict[str, Any]) -> None:
    """
    Print detailed year-by-year breakdown of total savings.
    
    Args:
        results: Results dictionary from calculate_total_savings with return_details=True
    """
    if 'yearly_breakdown' not in results:
        print("Detailed breakdown not available. Set return_details=True.")
        return
    
    print("\n" + "="*140)
    print("DETAILED YEAR-BY-YEAR BREAKDOWN")
    print("="*140)
    
    # Prepare table data
    headers = [
        "Year", "Age", "IRA Contrib", "IRA Future", "IRA Real", 
        "401k Balance", "401k Real", "Brokerage Contrib", "Brokerage Balance", "Brokerage Real",
        "Total Nominal", "Total Real", "529 Balance"
    ]
    
    table_data = []
    for year_data in results['yearly_breakdown']:
        table_data.append([
            year_data['year'],
            year_data['age'],
            f"${year_data['ira_contribution']:,.0f}",
            f"${year_data['ira_future_value']:,.0f}",
            f"${year_data['ira_future_value_real']:,.0f}",
            f"${year_data['401k_balance']:,.0f}",
            f"${year_data['401k_balance_real']:,.0f}",
            f"${year_data['brokerage_contribution']:,.0f}",
            f"${year_data['brokerage_balance']:,.0f}",
            f"${year_data['brokerage_balance_real']:,.0f}",
            f"${year_data['total_balance']:,.0f}",
            f"${year_data['total_balance_real']:,.0f}",
            f"${year_data['529_balance']:,.0f}"
        ])
    
    # Print table using tabulate
    from tabulate import tabulate
    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid", numalign="right"))
    print("="*140) 