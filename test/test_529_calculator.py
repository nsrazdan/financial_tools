#!/usr/bin/env python3
"""
Unit tests for 529 Plan calculator module
"""

import sys
import os
import unittest
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from modules.masters.calc_529_savings import (
    calculate_529_growth,
    print_529_analysis,
    project_529_balance
)


class Test529Calculator(unittest.TestCase):
    """Test cases for 529 Plan calculator functions"""

    def setUp(self):
        """Set up test fixtures"""
        pass

    def test_calculate_529_growth_basic(self):
        """Test basic 529 growth calculation"""
        result = calculate_529_growth(
            start_year=2025,
            years=2,
            starting_balance=10000,
            annual_contribution=5000,
            stock_market_return=0.07,
            inflation_rate=0.03
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('final_balance', result)
        self.assertIn('final_balance_real', result)
        self.assertIn('total_contributions', result)
        self.assertIn('net_growth', result)
        self.assertIn('parameters', result)
        
        # Check that values are reasonable
        self.assertGreater(result['final_balance'], 10000)
        self.assertEqual(result['total_contributions'], 10000)  # 2 years * 5000
        self.assertGreater(result['net_growth'], 0)

    def test_calculate_529_growth_no_contribution(self):
        """Test 529 growth calculation with no contributions"""
        result = calculate_529_growth(
            start_year=2025,
            years=2,
            starting_balance=10000,
            annual_contribution=0,
            stock_market_return=0.07
        )
        
        # Should only grow from investment returns
        expected_balance = 10000 * (1.07 ** 2)
        self.assertAlmostEqual(result['final_balance'], expected_balance, delta=100)
        self.assertEqual(result['total_contributions'], 0)

    def test_calculate_529_growth_with_contributions(self):
        """Test 529 growth calculation with contributions"""
        result = calculate_529_growth(
            start_year=2025,
            years=2,
            starting_balance=10000,
            annual_contribution=5000,
            stock_market_return=0.07
        )
        
        # Year 1: (10000 * 1.07) + 5000 = 15700
        # Year 2: (15700 * 1.07) + 5000 = 21799
        expected_balance = 21799
        self.assertAlmostEqual(result['final_balance'], expected_balance, delta=100)
        self.assertEqual(result['total_contributions'], 10000)

    def test_calculate_529_growth_detailed(self):
        """Test detailed 529 growth calculation"""
        result = calculate_529_growth(
            start_year=2025,
            years=2,
            starting_balance=10000,
            annual_contribution=5000,
            stock_market_return=0.07,
            return_details=True
        )
        
        self.assertIn('year_details', result)
        self.assertIsInstance(result['year_details'], list)
        self.assertEqual(len(result['year_details']), 2)
        
        # Check year details structure
        first_year = result['year_details'][0]
        expected_keys = ['year', 'contribution', 'balance', 'balance_real', 'total_contributions']
        for key in expected_keys:
            self.assertIn(key, first_year)

    def test_calculate_529_growth_zero_years(self):
        """Test 529 growth calculation with zero years"""
        result = calculate_529_growth(
            start_year=2025,
            years=0,
            starting_balance=10000,
            annual_contribution=5000
        )
        
        self.assertEqual(result['final_balance'], 10000)
        self.assertEqual(result['total_contributions'], 0)

    def test_calculate_529_growth_zero_balance(self):
        """Test 529 growth calculation with zero starting balance"""
        result = calculate_529_growth(
            start_year=2025,
            years=2,
            starting_balance=0,
            annual_contribution=5000,
            stock_market_return=0.07
        )
        
        self.assertGreater(result['final_balance'], 0)
        self.assertEqual(result['total_contributions'], 10000)

    def test_calculate_529_growth_negative_return(self):
        """Test 529 growth calculation with negative return"""
        result = calculate_529_growth(
            start_year=2025,
            years=2,
            starting_balance=10000,
            annual_contribution=5000,
            stock_market_return=-0.05  # -5% return
        )
        
        self.assertIsInstance(result, dict)
        self.assertGreater(result['final_balance'], 0)  # Should still be positive due to contributions

    def test_calculate_529_growth_inflation_adjustment(self):
        """Test 529 growth calculation with inflation adjustment"""
        result = calculate_529_growth(
            start_year=2025,
            years=2,
            starting_balance=10000,
            annual_contribution=5000,
            stock_market_return=0.07,
            inflation_rate=0.03
        )
        
        # Real balance should be less than nominal balance due to inflation
        self.assertLess(result['final_balance_real'], result['final_balance'])

    def test_project_529_balance(self):
        """Test 529 balance projection"""
        balances = project_529_balance(
            start_year=2025,
            years=3,
            starting_balance=10000,
            annual_contribution=5000,
            stock_market_return=0.07
        )
        
        self.assertIsInstance(balances, list)
        self.assertEqual(len(balances), 3)
        
        # Each year should be greater than the previous (due to growth + contributions)
        for i in range(1, len(balances)):
            self.assertGreater(balances[i], balances[i-1])

    def test_project_529_balance_no_contribution(self):
        """Test 529 balance projection with no contributions"""
        balances = project_529_balance(
            start_year=2025,
            years=2,
            starting_balance=10000,
            annual_contribution=0,
            stock_market_return=0.07
        )
        
        # Should only grow from investment returns
        expected_balance = 10000 * (1.07 ** 2)
        self.assertAlmostEqual(balances[1], expected_balance, delta=100)

    def test_project_529_balance_zero_years(self):
        """Test 529 balance projection with zero years"""
        balances = project_529_balance(
            start_year=2025,
            years=0,
            starting_balance=10000,
            annual_contribution=5000
        )
        
        self.assertEqual(len(balances), 0)

    def test_529_growth_parameter_types(self):
        """Test that function handles different parameter types correctly"""
        # Test with integer parameters
        result_int = calculate_529_growth(
            start_year=2025,
            years=2,
            starting_balance=10000,
            annual_contribution=5000,
            stock_market_return=0.07
        )
        
        # Test with float parameters
        result_float = calculate_529_growth(
            start_year=2025,
            years=2,
            starting_balance=10000.0,
            annual_contribution=5000.0,
            stock_market_return=0.07
        )
        
        self.assertAlmostEqual(result_int['final_balance'], result_float['final_balance'], places=2)

    def test_529_growth_net_growth_calculation(self):
        """Test that net growth is calculated correctly"""
        result = calculate_529_growth(
            start_year=2025,
            years=2,
            starting_balance=10000,
            annual_contribution=5000,
            stock_market_return=0.07
        )
        
        # Net growth should be final balance minus starting balance minus total contributions
        expected_net_growth = result['final_balance'] - 10000 - 10000
        self.assertAlmostEqual(result['net_growth'], expected_net_growth, places=2)

    def test_529_growth_real_balance_calculation(self):
        """Test that real balance is calculated correctly"""
        result = calculate_529_growth(
            start_year=2025,
            years=2,
            starting_balance=10000,
            annual_contribution=5000,
            stock_market_return=0.07,
            inflation_rate=0.03
        )
        
        # Real balance should be nominal balance divided by inflation factor
        expected_real_balance = result['final_balance'] / (1.03 ** 2)
        self.assertAlmostEqual(result['final_balance_real'], expected_real_balance, places=2)


if __name__ == '__main__':
    unittest.main() 