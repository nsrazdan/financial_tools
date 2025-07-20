# calc_401k_savings.py

BASE_401K_LIMIT_2025 = 23_500
CATCH_UP_50_PLUS = 7_500


def projected_401k_limit(start_year: int, current_year: int, growth_rate: float) -> float:
    """Project the 401k limit based on annual growth."""
    years_elapsed = current_year - start_year
    return BASE_401K_LIMIT_2025 * ((1 + growth_rate) ** years_elapsed)


def max_401k_contribution(year: int, start_year: int, age: int, growth_rate: float) -> float:
    """Max contribution for a given year including catch-up if age >= 50."""
    base_limit = projected_401k_limit(start_year, year, growth_rate)
    catch_up = CATCH_UP_50_PLUS if age >= 50 else 0
    return base_limit + catch_up


def total_401k_contributions_over_years(start_year: int,
                                         years: int,
                                         starting_age: int,
                                         starting_principal: float,
                                         growth_rate: float = 0.03,
                                         stock_market_growth_rate: float = 0.07) -> float:
    """
    Total projected 401k balance after a number of years, accounting for:
    - starting principal
    - growing contribution limits
    - catch-up contributions
    - annual investment growth
    """
    balance = starting_principal

    for i in range(years):
        year = start_year + i
        age = starting_age + i

        # Projected max contribution for the year
        annual_contribution = max_401k_contribution(year, start_year, age, growth_rate)

        # Apply annual growth to current balance BEFORE new contribution
        balance *= (1 + stock_market_growth_rate)

        # Add this year's contribution
        balance += annual_contribution

    return balance
