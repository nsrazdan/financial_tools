from ira_calculator_module import total_ira_contributions_over_years
from _401k_calculator_module import total_401k_contributions_over_years

# Example: 30 years starting at 2025, age 30, $100k MAGI growing at 3% annually

start_year=2025
years=2
age=25
filing_status='single'
starting_magi=130_000
magi_growth_rate=0.05
plan_covered=True



full_time_ira_total = total_ira_contributions_over_years(
    start_year=start_year,
    years=years,
    age=age,
    filing_status=filing_status,
    starting_magi=starting_magi,
    magi_growth_rate=magi_growth_rate,
    plan_covered=plan_covered
)

print(
    f"Starting in {start_year} at age {age} with an initial MAGI of ${starting_magi:,.0f}, "
    f"filing as {filing_status}, and assuming a {magi_growth_rate*100:.1f}% annual income growth rate "
    f"{'with' if plan_covered else 'without'} a workplace retirement plan, "
    f"you can contribute a total_ira of ${full_time_ira_total:,.2f} to your IRA over {years} years."
)

stock_market_growth_rate = 0.05
_401k_limit_growth_rate = 0.03  # 3% annual growth in 401k limit
starting_401k_principal = 85557

part_time_401k_limit_total = total_401k_contributions_over_years(
    start_year=start_year,
    years=years,
    starting_age=age,
    starting_principal=starting_401k_principal,
    _401k_limit_growth_rate=_401k_limit_growth_rate,
    stock_market_growth_rate=stock_market_growth_rate
)

print(f"Total 401k contributions from age {age} to {age + years} with annual growth in 401k limit {_401k_limit_growth_rate}: ${_401k_limit_total:,.2f}")