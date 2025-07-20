#!/usr/bin/env python3
"""
Unit tests for Total Savings calculator module
"""

import sys
import os
import unittest
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from modules.masters.calc_total_savings import (
    calculate_total_savings,
    print_total_savings_summary,
    print_detailed_breakdown
)


class TestTotalSavings(unittest.TestCase):
    """Test cases for Total Savings calculator functions"""

    def setUp(self):
        """Set up test fixtures"""
        pass

    def test_calculate_total_savings_basic(self):
        """Test basic total savings calculation"""
        result = calculate_total_savings(
            start_year=2025,
            years=1,
            age=25,
            filing_status='single',
            starting_magi=50000,
            return_details=False
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('ira_nominal', result)
        self.assertIn('ira_real', result)
        self.assertIn('401k_nominal', result)
        self.assertIn('401k_real', result)
        self.assertIn('401k_contributions', result)
        self.assertIn('total_nominal', result)
        self.assertIn('total_real', result)
        self.assertIn('parameters', result)
        
        # Check that values are reasonable
        self.assertGreater(result['total_nominal'], 0)
        self.assertGreater(result['total_real'], 0)
        self.assertLessEqual(result['total_real'], result['total_nominal'])  # Real should be <= nominal

    def test_calculate_total_savings_detailed(self):
        """Test detailed total savings calculation"""
        result = calculate_total_savings(
            start_year=2025,
            years=2,
            age=25,
            filing_status='single',
            starting_magi=50000,
            return_details=True
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('yearly_breakdown', result)
        self.assertIsInstance(result['yearly_breakdown'], list)
        self.assertEqual(len(result['yearly_breakdown']), 2)
        
        # Check yearly breakdown structure
        first_year = result['yearly_breakdown'][0]
        expected_keys = [
            'year', 'age', 'ira_contribution', 'ira_future_value', 
            'ira_future_value_real', '401k_balance', '401k_balance_real',
            'total_balance', 'total_balance_real'
        ]
        for key in expected_keys:
            self.assertIn(key, first_year)

    def test_calculate_total_savings_with_401k_balance(self):
        """Test total savings calculation with existing 401k balance"""
        result = calculate_total_savings(
            start_year=2025,
            years=1,
            age=25,
            filing_status='single',
            starting_magi=50000,
            starting_401k_balance=10000,
            return_details=True
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('yearly_breakdown', result)
        self.assertGreater(len(result['yearly_breakdown']), 0)
        
        # Check that 401k balance is included and grows
        first_year = result['yearly_breakdown'][0]
        self.assertIn('401k_balance', first_year)
        self.assertGreater(first_year['401k_balance'], 10000)  # Should grow

    def test_calculate_total_savings_joint_filing(self):
        """Test total savings calculation for joint filers"""
        result = calculate_total_savings(
            start_year=2025,
            years=1,
            age=25,
            filing_status='joint',
            starting_magi=100000,
            return_details=False
        )
        
        self.assertIsInstance(result, dict)
        self.assertGreater(result['total_nominal'], 0)
        self.assertGreater(result['total_real'], 0)

    def test_calculate_total_savings_separate_lived(self):
        """Test total savings calculation for separated but not living together"""
        result = calculate_total_savings(
            start_year=2025,
            years=1,
            age=25,
            filing_status='separate_lived',
            starting_magi=50000,
            return_details=False
        )
        
        self.assertIsInstance(result, dict)
        self.assertGreater(result['total_nominal'], 0)
        self.assertGreater(result['total_real'], 0)

    def test_calculate_total_savings_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Test zero years
        result = calculate_total_savings(
            start_year=2025,
            years=0,
            age=25,
            filing_status='single',
            starting_magi=50000,
            return_details=True
        )
        self.assertEqual(result['total_nominal'], 0.0)
        self.assertEqual(result['total_real'], 0.0)
        
        # Test very high income (should still calculate, but IRA contributions may be limited)
        result = calculate_total_savings(
            start_year=2025,
            years=1,
            age=25,
            filing_status='single',
            starting_magi=1000000,
            return_details=False
        )
        self.assertIsInstance(result, dict)
        self.assertGreaterEqual(result['total_nominal'], 0.0)

    def test_print_functions(self):
        """Test that print functions don't crash"""
        result = calculate_total_savings(
            start_year=2025,
            years=1,
            age=25,
            filing_status='single',
            starting_magi=50000,
            return_details=True
        )
        
        # These should not raise exceptions
        try:
            print_total_savings_summary(result)
            print_detailed_breakdown(result)
        except Exception as e:
            self.fail(f"Print functions raised an exception: {e}")

    def test_parameter_consistency(self):
        """Test that parameters are correctly passed through"""
        result = calculate_total_savings(
            start_year=2025,
            years=5,
            age=30,
            filing_status='joint',
            starting_magi=75000,
            magi_growth_rate=0.04,
            plan_covered=True,
            stock_market_return=0.08,
            starting_401k_balance=25000,
            starting_401k_principal=50000,
            inflation_rate=0.025,
            _401k_limit_growth_rate=0.02,
            return_details=False
        )
        
        params = result['parameters']
        self.assertEqual(params['start_year'], 2025)
        self.assertEqual(params['years'], 5)
        self.assertEqual(params['age'], 30)
        self.assertEqual(params['filing_status'], 'joint')
        self.assertEqual(params['starting_magi'], 75000)
        self.assertEqual(params['magi_growth_rate'], 0.04)
        self.assertTrue(params['plan_covered'])
        self.assertEqual(params['stock_market_return'], 0.08)
        self.assertEqual(params['starting_401k_balance'], 25000)
        self.assertEqual(params['starting_401k_principal'], 50000)
        self.assertEqual(params['inflation_rate'], 0.025)
        self.assertEqual(params['_401k_limit_growth_rate'], 0.02)


if __name__ == '__main__':
    unittest.main() 