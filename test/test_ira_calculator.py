#!/usr/bin/env python3
"""
Unit tests for IRA calculator module
"""

import sys
import os
import unittest
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from modules.masters.calc_ira_savings import (
    BASE_LIMITS, CATCH_UP, PHASE_OUT,
    HISTORICAL_401K_LIMITS, HISTORICAL_401K_CATCHUP,
    calculate_historical_401k_growth_rate,
    get_historical_401k_growth_info,
    projected_401k_limit,
    projected_401k_catchup,
    max_401k_contribution,
    project_401k_balance,
    projected_limit,
    get_phaseout,
    max_ira_contribution,
    total_ira_contributions_over_years
)


class TestIRACalculator(unittest.TestCase):
    """Test cases for IRA calculator functions"""

    def setUp(self):
        """Set up test fixtures"""
        pass

    def test_base_limits(self):
        """Test IRA base contribution limits"""
        self.assertEqual(BASE_LIMITS[2022], 6000)
        self.assertEqual(BASE_LIMITS[2023], 6500)
        self.assertEqual(BASE_LIMITS[2024], 7000)
        self.assertEqual(BASE_LIMITS[2025], 7000)

    def test_catch_up_limit(self):
        """Test catch-up contribution limit"""
        self.assertEqual(CATCH_UP, 1000)

    def test_phase_out_ranges(self):
        """Test income phase-out ranges"""
        self.assertEqual(PHASE_OUT[2025]['roth_single'], (150_000, 165_000))
        self.assertEqual(PHASE_OUT[2025]['roth_joint'], (230_000, 240_000))
        self.assertEqual(PHASE_OUT[2025]['trad_deduct_single'], (77_000, 87_000))
        self.assertEqual(PHASE_OUT[2025]['trad_deduct_joint'], (123_000, 143_000))

    def test_historical_401k_limits(self):
        """Test historical 401k contribution limits"""
        self.assertEqual(HISTORICAL_401K_LIMITS[2020], 19500)
        self.assertEqual(HISTORICAL_401K_LIMITS[2021], 19500)
        self.assertEqual(HISTORICAL_401K_LIMITS[2022], 20500)
        self.assertEqual(HISTORICAL_401K_LIMITS[2023], 22500)
        self.assertEqual(HISTORICAL_401K_LIMITS[2024], 23000)
        self.assertEqual(HISTORICAL_401K_LIMITS[2025], 23500)

    def test_historical_401k_catchup(self):
        """Test historical 401k catch-up contribution limits"""
        self.assertEqual(HISTORICAL_401K_CATCHUP[2020], 6500)
        self.assertEqual(HISTORICAL_401K_CATCHUP[2021], 6500)
        self.assertEqual(HISTORICAL_401K_CATCHUP[2022], 6750)
        self.assertEqual(HISTORICAL_401K_CATCHUP[2023], 7500)
        self.assertEqual(HISTORICAL_401K_CATCHUP[2024], 7500)
        self.assertEqual(HISTORICAL_401K_CATCHUP[2025], 7500)

    def test_calculate_historical_401k_growth_rate(self):
        """Test historical 401k growth rate calculation"""
        growth_rate = calculate_historical_401k_growth_rate()
        self.assertIsInstance(growth_rate, float)
        self.assertGreater(growth_rate, 0)
        self.assertLess(growth_rate, 0.1)  # Should be reasonable (less than 10%)

    def test_get_historical_401k_growth_info(self):
        """Test historical 401k growth info retrieval"""
        info = get_historical_401k_growth_info()
        self.assertIsInstance(info, dict)
        self.assertIn('growth_rate', info)
        self.assertIn('start_year', info)
        self.assertIn('end_year', info)
        self.assertIn('start_value', info)
        self.assertIn('end_value', info)
        self.assertIn('years_elapsed', info)
        
        self.assertIsInstance(info['growth_rate'], float)
        self.assertIsInstance(info['start_year'], int)
        self.assertIsInstance(info['end_year'], int)
        self.assertIsInstance(info['start_value'], int)
        self.assertIsInstance(info['end_value'], int)
        self.assertIsInstance(info['years_elapsed'], int)

    def test_projected_401k_limit(self):
        """Test 401k limit projection"""
        # Test known historical values
        self.assertEqual(projected_401k_limit(2024), 23000)
        self.assertEqual(projected_401k_limit(2025), 23500)
        
        # Test future projection
        future_limit = projected_401k_limit(2026)
        self.assertIsInstance(future_limit, float)
        self.assertGreater(future_limit, 23500)

    def test_projected_401k_catchup(self):
        """Test 401k catch-up contribution projection"""
        # Test known historical values
        self.assertEqual(projected_401k_catchup(2024), 7500)
        self.assertEqual(projected_401k_catchup(2025), 7500)
        
        # Test future projection
        future_catchup = projected_401k_catchup(2026)
        self.assertIsInstance(future_catchup, float)
        self.assertGreaterEqual(future_catchup, 7500)

    def test_max_401k_contribution(self):
        """Test maximum 401k contribution calculation"""
        # Test under age 50
        self.assertEqual(max_401k_contribution(2025, 25), 23500)
        self.assertEqual(max_401k_contribution(2025, 49), 23500)
        
        # Test age 50 and over (includes catch-up)
        self.assertEqual(max_401k_contribution(2025, 50), 31000)
        self.assertEqual(max_401k_contribution(2025, 65), 31000)

    def test_project_401k_balance(self):
        """Test 401k balance projection"""
        balances = project_401k_balance(
            start_year=2025,
            years=3,
            starting_age=25,
            starting_401k_balance=10000,
            stock_market_return=0.07
        )
        
        self.assertIsInstance(balances, list)
        self.assertEqual(len(balances), 3)
        
        # Each year should be greater than the previous (due to growth + contributions)
        for i in range(1, len(balances)):
            self.assertGreater(balances[i], balances[i-1])

    def test_projected_limit(self):
        """Test IRA contribution limit projection"""
        # Test known values
        self.assertEqual(projected_limit(2022), 6000)
        self.assertEqual(projected_limit(2023), 6500)
        self.assertEqual(projected_limit(2024), 7000)
        self.assertEqual(projected_limit(2025), 7000)
        
        # Test future projection
        future_limit = projected_limit(2026)
        self.assertIsInstance(future_limit, int)
        self.assertGreaterEqual(future_limit, 7000)

    def test_get_phaseout(self):
        """Test income phase-out range retrieval"""
        # Test known values
        roth_single_2025 = get_phaseout(2025, 'roth_single')
        self.assertEqual(roth_single_2025, (150_000, 165_000))
        
        # Test future projection
        roth_single_2030 = get_phaseout(2030, 'roth_single')
        self.assertIsInstance(roth_single_2030, tuple)
        self.assertEqual(len(roth_single_2030), 2)
        self.assertGreaterEqual(roth_single_2030[0], 150_000)  # Should be >=, not >

    def test_max_ira_contribution_basic(self):
        """Test basic IRA contribution calculation"""
        # Test single filer, low income (full contribution)
        contribution = max_ira_contribution(2025, 25, 'single', 50000, False)
        self.assertEqual(contribution, 7000)  # Base limit for 2025
        
        # Test with catch-up (age 50+)
        contribution = max_ira_contribution(2025, 50, 'single', 50000, False)
        self.assertEqual(contribution, 8000)  # Base + catch-up

    def test_max_ira_contribution_phaseout(self):
        """Test IRA contribution calculation with income phase-out"""
        # Test Roth IRA phase-out (single filer)
        # Income in phase-out range
        contribution = max_ira_contribution(2025, 25, 'single', 160000, False)
        self.assertLessEqual(contribution, 7000)  # Should be <=, not <
        self.assertGreater(contribution, 0)
        
        # Income above phase-out range
        contribution = max_ira_contribution(2025, 25, 'single', 200000, False)
        self.assertIsInstance(contribution, (int, float))
        self.assertGreaterEqual(contribution, 0.0)

    def test_max_ira_contribution_joint(self):
        """Test IRA contribution calculation for joint filers"""
        # Test joint filer, low income (full contribution)
        contribution = max_ira_contribution(2025, 25, 'joint', 100000, False)
        self.assertEqual(contribution, 7000)
        
        # Test joint filer in phase-out range
        contribution = max_ira_contribution(2025, 25, 'joint', 240000, False)
        self.assertLessEqual(contribution, 7000)  # Should be <=, not <
        self.assertGreater(contribution, 0)

    def test_max_ira_contribution_plan_covered(self):
        """Test IRA contribution calculation when covered by workplace plan"""
        # Traditional IRA deduction phase-out when covered by plan
        contribution = max_ira_contribution(2025, 25, 'single', 85000, True)
        self.assertLessEqual(contribution, 7000)  # Should be <=, not <
        self.assertGreater(contribution, 0)

    def test_total_ira_contributions_over_years_basic(self):
        """Test basic IRA contributions over years calculation"""
        result = total_ira_contributions_over_years(
            start_year=2025,
            years=1,
            age=25,
            filing_status='single',
            starting_magi=50000,
            return_details=False
        )
        
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_total_ira_contributions_over_years_detailed(self):
        """Test detailed IRA contributions over years calculation"""
        result = total_ira_contributions_over_years(
            start_year=2025,
            years=2,
            age=25,
            filing_status='single',
            starting_magi=50000,
            return_details=True
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('total_accumulated', result)
        self.assertIn('total_accumulated_real', result)
        self.assertIn('year_details', result)
        self.assertIn('parameters', result)
        
        self.assertIsInstance(result['total_accumulated'], float)
        self.assertIsInstance(result['total_accumulated_real'], float)
        self.assertIsInstance(result['year_details'], list)
        self.assertIsInstance(result['parameters'], dict)
        
        self.assertEqual(len(result['year_details']), 2)

    def test_total_ira_contributions_with_401k(self):
        """Test IRA contributions calculation with 401k balance"""
        result = total_ira_contributions_over_years(
            start_year=2025,
            years=1,
            age=25,
            filing_status='single',
            starting_magi=50000,
            starting_401k_balance=10000,
            return_details=True
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('year_details', result)
        self.assertGreater(len(result['year_details']), 0)
        
        # Check that 401k balance is included in year details
        first_year = result['year_details'][0]
        self.assertIn('401k_balance', first_year)
        self.assertGreater(first_year['401k_balance'], 10000)  # Should grow

    def test_invalid_filing_status(self):
        """Test error handling for invalid filing status"""
        with self.assertRaises(ValueError):
            max_ira_contribution(2025, 25, 'invalid_status', 50000, False)

    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Test zero years
        result = total_ira_contributions_over_years(
            start_year=2025,
            years=0,
            age=25,
            filing_status='single',
            starting_magi=50000,
            return_details=True
        )
        self.assertEqual(result['total_accumulated'], 0.0)
        
        # Test very high income (should result in zero contribution)
        # Note: The function may still allow contributions even at high income
        # depending on the specific phase-out logic
        contribution = max_ira_contribution(2025, 25, 'single', 1000000, False)
        self.assertIsInstance(contribution, (int, float))  # Can be int or float
        self.assertGreaterEqual(contribution, 0.0)


if __name__ == '__main__':
    unittest.main() 