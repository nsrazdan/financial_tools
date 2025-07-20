# ira_calculator.py
from tabulate import tabulate

BASE_LIMITS = {
    2022: 6000,
    2023: 6500,
    2024: 7000,
    2025: 7000,
}

CATCH_UP = 1000

PHASE_OUT = {
    2025: {
        'roth_single': (150_000, 165_000),
        'roth_joint': (230_000, 240_000),
        'trad_deduct_single': (77_000, 87_000),
        'trad_deduct_joint': (123_000, 143_000),
    }
}

# Historical 401k contribution limits (employee contribution limit)
HISTORICAL_401K_LIMITS = {
    2006: 15000,
    2007: 15500,
    2008: 15500,
    2009: 16500,
    2010: 16500,
    2011: 16500,
    2012: 17000,
    2013: 17500,
    2014: 17500,
    2015: 18000,
    2016: 18000,
    2017: 18000,
    2018: 18500,
    2019: 19000,
    2020: 19500,
    2021: 19500,
    2022: 20500,
    2023: 22500,
    2024: 23000,
    2025: 23500,
}

# Historical catch-up contribution limits (age 50+)
HISTORICAL_401K_CATCHUP = {
    2006: 5000,
    2007: 5000,
    2008: 5000,
    2009: 5500,
    2010: 5500,
    2011: 5500,
    2012: 5500,
    2013: 5500,
    2014: 5500,
    2015: 6000,
    2016: 6000,
    2017: 6000,
    2018: 6000,
    2019: 6000,
    2020: 6500,
    2021: 6500,
    2022: 6750,
    2023: 7500,
    2024: 7500,
    2025: 7500,
}


def calculate_historical_401k_growth_rate() -> float:
    """Calculate average annual growth rate of 401k limits based on historical data."""
    years = sorted(HISTORICAL_401K_LIMITS.keys())
    if len(years) < 2:
        return 0.03  # Default fallback
    
    # Calculate compound annual growth rate (CAGR)
    start_value = HISTORICAL_401K_LIMITS[years[0]]
    end_value = HISTORICAL_401K_LIMITS[years[-1]]
    years_elapsed = years[-1] - years[0]
    
    if start_value <= 0 or years_elapsed <= 0:
        return 0.03  # Default fallback
    
    # Round the start and end values to the nearest 500 before calculating growth rate
    start_value_rounded = round(start_value / 500) * 500
    end_value_rounded = round(end_value / 500) * 500
    
    cagr = (end_value_rounded / start_value_rounded) ** (1 / years_elapsed) - 1
    return cagr


def get_historical_401k_growth_info() -> dict:
    """Get information about historical 401k growth for display purposes."""
    years = sorted(HISTORICAL_401K_LIMITS.keys())
    if len(years) < 2:
        return {"growth_rate": 0.03, "start_year": None, "end_year": None, "start_value": None, "end_value": None}
    
    start_year = years[0]
    end_year = years[-1]
    start_value = HISTORICAL_401K_LIMITS[start_year]
    end_value = HISTORICAL_401K_LIMITS[end_year]
    
    # Round the values to the nearest 500 for display
    start_value_rounded = round(start_value / 500) * 500
    end_value_rounded = round(end_value / 500) * 500
    
    growth_rate = calculate_historical_401k_growth_rate()   
    
    return {
        "growth_rate": growth_rate,
        "start_year": start_year,
        "end_year": end_year,
        "start_value": start_value_rounded,
        "end_value": end_value_rounded,
        "years_elapsed": end_year - start_year
    }


def projected_401k_limit(year: int, base_year: int = 2025, growth_rate: float = None) -> float:
    """Project 401k contribution limit for future years based on historical trends."""
    if growth_rate is None:
        growth_rate = calculate_historical_401k_growth_rate()
    
    if year in HISTORICAL_401K_LIMITS:
        return float(HISTORICAL_401K_LIMITS[year])
    
    years_elapsed = year - base_year
    base_limit = HISTORICAL_401K_LIMITS[base_year]
    projected_limit = base_limit * ((1 + growth_rate) ** years_elapsed)
    
    # Round to the nearest 500
    return float(round(projected_limit / 500) * 500)


def projected_401k_catchup(year: int, base_year: int = 2025, growth_rate: float = None) -> float:
    """Project 401k catch-up contribution limit for future years."""
    if growth_rate is None:
        growth_rate = calculate_historical_401k_growth_rate()
    
    if year in HISTORICAL_401K_CATCHUP:
        return float(HISTORICAL_401K_CATCHUP[year])
    
    years_elapsed = year - base_year
    base_catchup = HISTORICAL_401K_CATCHUP[base_year]
    projected_catchup = base_catchup * ((1 + growth_rate) ** years_elapsed)
    
    # Round to the nearest 500
    return float(round(projected_catchup / 500) * 500)


def max_401k_contribution(year: int, age: int, growth_rate: float = None) -> float:
    """Calculate max 401k contribution for a given year including catch-up if age >= 50."""
    base_limit = projected_401k_limit(year, growth_rate=growth_rate)
    catch_up = projected_401k_catchup(year, growth_rate=growth_rate) if age >= 50 else 0
    return base_limit + catch_up


def project_401k_balance(start_year: int, years: int, starting_age: int, 
                        starting_401k_balance: float, stock_market_return: float = 0.07,
                        _401k_growth_rate: float = None) -> list:
    """
    Project 401k balance over years, returning list of balances for each year.
    This accounts for:
    - Starting balance
    - Annual contributions (growing limits)
    - Catch-up contributions (age 50+)
    - Stock market growth
    """
    balances = []
    current_balance = starting_401k_balance
    
    for i in range(years):
        year = start_year + i
        age = starting_age + i
        
        # Apply growth to current balance
        current_balance *= (1 + stock_market_return)
        
        # Add this year's contribution
        annual_contribution = max_401k_contribution(year, age, _401k_growth_rate)
        current_balance += annual_contribution
        
        balances.append(current_balance)
    
    return balances


def projected_limit(year: int) -> int:
    """Estimate IRA contribution limit for future years."""
    if year in BASE_LIMITS:
        return BASE_LIMITS[year]
    steps = (year - 2022) // 2
    calculated_limit = 6000 + steps * 500
    # Round to the nearest 500
    return round(calculated_limit / 500) * 500


def get_phaseout(year: int, key: str):
    """Get income phase-out range."""
    try:
        return PHASE_OUT[year][key]
    except KeyError:
        # Project flat increase of $10,000 per decade
        base_year = 2025
        base_low, base_high = PHASE_OUT[base_year][key]
        years_ahead = year - base_year
        increase = (years_ahead // 10) * 10_000
        return base_low + increase, base_high + increase


def max_ira_contribution(year: int, age: int, filing_status: str, magi: float, plan_covered: bool = False) -> float:
    """Calculate max IRA contribution based on income and filing status."""
    base = projected_limit(year)
    catch = CATCH_UP if age >= 50 else 0
    max_total = base + catch

    if filing_status == 'single':
        key = 'roth_single'
    elif filing_status == 'joint':
        key = 'roth_joint'
    elif filing_status == 'separate_lived':
        key = None
        low, high = 0, 10_000
    else:
        raise ValueError("Unsupported filing status")

    if key:
        low, high = get_phaseout(year, key)

    if magi < low:
        roth_max = max_total
    elif magi >= high:
        roth_max = 0.0
    else:
        roth_max = max_total * (high - magi) / (high - low)

    if plan_covered:
        if filing_status == 'single':
            low_t, high_t = get_phaseout(year, 'trad_deduct_single')
        elif filing_status == 'joint':
            low_t, high_t = get_phaseout(year, 'trad_deduct_joint')
        elif filing_status == 'separate_lived':
            low_t, high_t = 0, 10_000
        else:
            raise ValueError("Unsupported filing status for traditional IRA")

        if magi < low_t:
            trad_max = max_total
        elif magi >= high_t:
            trad_max = 0.0
        else:
            trad_max = max_total * (high_t - magi) / (high_t - low_t)
    else:
        trad_max = max_total

    return max(trad_max, roth_max)


def total_ira_contributions_over_years(start_year: int, years: int, age: int, filing_status: str,
                                   starting_magi: float, magi_growth_rate: float, plan_covered: bool,
                                   stock_market_return: float, starting_401k_balance: float,
                                   _401k_growth_rate: float, inflation_rate: float,
                                   masters_degree_enabled: bool,
                                   masters_start_year: int,
                                   masters_degree_years: int,
                                   masters_enrollment_type: str,
                                   return_details: bool) -> float:
    """
    Calculate total accumulated savings over years with compound growth from stock market,
    taking into account 401k balance growth, inflation, and real vs nominal returns.
    :param start_year: First year (e.g., 2025)
    :param years: Number of years to calculate (e.g., 30)
    :param age: Starting age
    :param filing_status: 'single', 'joint', etc.
    :param starting_magi: Starting MAGI
    :param magi_growth_rate: Annual MAGI increase (default 3%)
    :param plan_covered: Whether participant is covered by workplace plan
    :param stock_market_return: Annual stock market return rate (default 7%)
    :param starting_401k_balance: Starting 401k balance (default 0)
    :param _401k_growth_rate: Annual growth rate for 401k limits (default: calculated from historical data)
    :param inflation_rate: Annual inflation rate (default 3%)
    :param masters_degree_enabled: Whether master's degree is enabled
    :param masters_start_year: Year when master's degree starts
    :param masters_degree_years: Number of years for master's degree
    :param masters_enrollment_type: "full_time" or "part_time"
    :param return_details: If True, return detailed year-by-year breakdown
    :return: Total accumulated savings with compound growth, or dict with details if return_details=True
    """
    # Use the unified stock market return parameter
    effective_stock_return = stock_market_return
    
    # Calculate real return (nominal return minus inflation)
    real_return = effective_stock_return - inflation_rate
    
    # Project 401k balances over the years
    _401k_balances = project_401k_balance(
        start_year=start_year,
        years=years,
        starting_age=age,
        starting_401k_balance=starting_401k_balance,
        stock_market_return=effective_stock_return,
        _401k_growth_rate=_401k_growth_rate
    )
    
    # Calculate IRA balance year by year (more realistic approach)
    ira_balance = 0.0
    ira_balance_real = 0.0
    magi = starting_magi
    year_details = []
    
    for i in range(years):
        year = start_year + i
        current_age = age + i
        
        # Get current 401k balance for this year
        current_401k_balance = _401k_balances[i] if i < len(_401k_balances) else starting_401k_balance
        
        # Calculate IRA contribution for this year
        contribution = max_ira_contribution(year, current_age, filing_status, magi, plan_covered)
        
        # Apply master's degree logic: full-time enrollment stops IRA contributions
        if masters_degree_enabled and masters_start_year is not None and masters_start_year <= year < masters_start_year + masters_degree_years:
            if masters_enrollment_type == "full_time":
                contribution = 0.0  # No IRA contributions during full-time degree
        
        # Apply growth to existing IRA balance
        ira_balance *= (1 + effective_stock_return)
        ira_balance_real *= (1 + real_return)
        
        # Add this year's contribution
        ira_balance += contribution
        ira_balance_real += contribution
        
        # Store year details if requested
        if return_details:
            year_details.append({
                'year': year,
                'age': current_age,
                'magi': magi,
                'ira_contribution': contribution,
                'future_value': ira_balance,
                'future_value_real': ira_balance_real,
                '401k_balance': current_401k_balance,
                '401k_limit': projected_401k_limit(year, growth_rate=_401k_growth_rate),
                '401k_catchup': projected_401k_catchup(year, growth_rate=_401k_growth_rate) if current_age >= 50 else 0
            })
        
        # Update MAGI for next year
        magi *= (1 + magi_growth_rate)
    
    if return_details:
        return {
            'total_accumulated': ira_balance,
            'total_accumulated_real': ira_balance_real,
            'year_details': year_details,
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
                '_401k_growth_rate': _401k_growth_rate,
                'inflation_rate': inflation_rate,
                'effective_stock_return': effective_stock_return,
                'real_return': real_return,
                'masters_degree_enabled': masters_degree_enabled,
                'masters_start_year': masters_start_year,
                'masters_degree_years': masters_degree_years,
                'masters_enrollment_type': masters_enrollment_type
            }
        }
    
    return ira_balance


def print_ira_analysis_table(analysis_data: dict) -> None:
    """
    Print a formatted table showing year-by-year IRA analysis.
    :param analysis_data: Dictionary returned from total_ira_contributions_over_years with return_details=True
    """
    params = analysis_data['parameters']
    year_details = analysis_data['year_details']
    
    print(f"\nIRA Analysis Table")
    print(f"{'='*80}")
    
    # Print parameters table
    print(f"Parameters:")
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
        ["Real Return", f"{params['real_return']*100:.2f}%"],
        ["Starting 401k Balance", f"${params['starting_401k_balance']:,.0f}"],
        ["401k Limit Growth Rate", f"{params['_401k_growth_rate']*100:.2f}%" if params['_401k_growth_rate'] else "Historical (2.39%)"]
    ]
    
    from tabulate import tabulate
    print(tabulate(param_data, headers=param_headers, tablefmt="simple", numalign="left"))
    
    print(f"\nYear-by-Year Breakdown:")
    
    # Prepare data for tabulate
    table_data = []
    for detail in year_details:
        table_data.append([
            detail['year'],
            detail['age'],
            f"${detail['magi']:,.0f}",
            f"${detail['ira_contribution']:,.0f}",
            detail['years_to_grow'],
            f"${detail['future_value']:,.0f}",
            f"${detail['future_value_real']:,.0f}",
            f"${detail['401k_balance']:,.0f}",
            f"${detail['401k_limit']:,.0f}",
            f"${detail['401k_catchup']:,.0f}"
        ])
    
    headers = [
        "Year", "Age", "MAGI", "IRA Contrib", "Yrs to Grow", 
        "Future Val", "Real Val", "401k Bal", "401k Limit", "401k Catch"
    ]
    
    print(tabulate(table_data, headers=headers, tablefmt="simple", numalign="right"))
    
    # Print summary table
    print(f"\nSummary:")
    summary_headers = ["Metric", "Value"]
    summary_data = [
        ["Total Accumulated IRA Value (Nominal)", f"${analysis_data['total_accumulated']:,.2f}"],
        ["Total Accumulated IRA Value (Real)", f"${analysis_data['total_accumulated_real']:,.2f}"]
    ]
    
    print(tabulate(summary_data, headers=summary_headers, tablefmt="simple", numalign="right"))
    print(f"{'='*80}")
