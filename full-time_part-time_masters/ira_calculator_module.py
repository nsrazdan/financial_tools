# ira_calculator.py

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
        'roth_joint': (236_000, 246_000),
        'trad_deduct_single': (79_000, 89_000),
        'trad_deduct_joint': (126_000, 146_000),
    }
}


def projected_limit(year: int) -> int:
    """Estimate IRA contribution limit for future years."""
    if year in BASE_LIMITS:
        return BASE_LIMITS[year]
    steps = (year - 2022) // 2
    return 6000 + steps * 500


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

    if filing_status in ('single', 'hoh', 'separate_not_lived'):
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
        if filing_status in ('single', 'hoh'):
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


def total_ira_contributions_over_years(start_year: int, years: int, age: int, filing_status: str, starting_magi: float,
                                   magi_growth_rate: float = 0.03, plan_covered: bool = False) -> float:
    """
    Calculate total contributions over years with annual MAGI increase.
    :param start_year: First year (e.g., 2025)
    :param years: Number of years to calculate (e.g., 30)
    :param age: Starting age
    :param filing_status: 'single', 'joint', etc.
    :param starting_magi: Starting MAGI
    :param magi_growth_rate: Annual MAGI increase (default 3%)
    :param plan_covered: Whether participant is covered by workplace plan
    :return: Sum of allowed IRA contributions over period
    """
    total = 0.0
    magi = starting_magi
    for i in range(years):
        year = start_year + i
        current_age = age + i
        contribution = max_ira_contribution(year, current_age, filing_status, magi, plan_covered)
        total += contribution
        magi *= (1 + magi_growth_rate)
    return total
