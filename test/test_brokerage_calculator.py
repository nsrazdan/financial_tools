#!/usr/bin/env python3
"""
Test module for brokerage account savings calculator.
"""

import unittest
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from modules.masters.calc_brokerage_savings import (
    calculate_brokerage_growth,
    project_brokerage_balance,
    print_brokerage_analysis_table,
    print_brokerage_summary
)


class TestBrokerageCalculator(unittest.TestCase):
    """Test cases for brokerage account calculations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_params = {
            'start_year': 2025,
            'years': 5,
            'starting_balance': 10000,
            'annual_contribution': 5000,
            'contribution_growth_rate': 0.03,
            'stock_market_return': 0.07,
            'inflation_rate': 0.03
        }
    
    def test_calculate_brokerage_growth_basic(self):
        """Test basic brokerage growth calculation."""
        result = calculate_brokerage_growth(
            start_year=self.test_params['start_year'],
            years=self.test_params['years'],
            starting_balance=self.test_params['starting_balance'],
            annual_contribution=self.test_params['annual_contribution'],
            contribution_growth_rate=self.test_params['contribution_growth_rate'],
            stock_market_return=self.test_params['stock_market_return'],
            inflation_rate=self.test_params['inflation_rate'],
            return_details=False
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('total_accumulated', result)
        self.assertIn('total_accumulated_real', result)
        self.assertIn('final_balance', result)
        self.assertIn('final_balance_real', result)
        self.assertIn('parameters', result)
        
        self.assertIsInstance(result['total_accumulated'], float)
        self.assertIsInstance(result['total_accumulated_real'], float)
        self.assertIsInstance(result['final_balance'], float)
        self.assertIsInstance(result['final_balance_real'], float)
        self.assertIsInstance(result['parameters'], dict)
        
        # Values should be positive
        self.assertGreater(result['total_accumulated'], 0)
        self.assertGreater(result['total_accumulated_real'], 0)
        self.assertGreater(result['final_balance'], 0)
        self.assertGreater(result['final_balance_real'], 0)
    
    def test_calculate_brokerage_growth_detailed(self):
        """Test detailed brokerage growth calculation."""
        result = calculate_brokerage_growth(
            start_year=self.test_params['start_year'],
            years=self.test_params['years'],
            starting_balance=self.test_params['starting_balance'],
            annual_contribution=self.test_params['annual_contribution'],
            contribution_growth_rate=self.test_params['contribution_growth_rate'],
            stock_market_return=self.test_params['stock_market_return'],
            inflation_rate=self.test_params['inflation_rate'],
            return_details=True
        )
        
        self.assertIn('year_details', result)
        self.assertIsInstance(result['year_details'], list)
        self.assertEqual(len(result['year_details']), self.test_params['years'])
        
        # Check year details structure
        for year_data in result['year_details']:
            self.assertIn('year', year_data)
            self.assertIn('contribution', year_data)
            self.assertIn('balance', year_data)
            self.assertIn('balance_real', year_data)
            self.assertIn('years_to_grow', year_data)
            self.assertIn('future_value', year_data)
            self.assertIn('future_value_real', year_data)
            
            # Values should be positive
            self.assertGreaterEqual(year_data['contribution'], 0)
            self.assertGreater(year_data['balance'], 0)
            self.assertGreater(year_data['balance_real'], 0)
            self.assertGreaterEqual(year_data['future_value'], 0)
            self.assertGreaterEqual(year_data['future_value_real'], 0)
    
    def test_project_brokerage_balance(self):
        """Test brokerage balance projection."""
        balances = project_brokerage_balance(
            start_year=self.test_params['start_year'],
            years=self.test_params['years'],
            starting_balance=self.test_params['starting_balance'],
            annual_contribution=self.test_params['annual_contribution'],
            contribution_growth_rate=self.test_params['contribution_growth_rate'],
            stock_market_return=self.test_params['stock_market_return']
        )
        
        self.assertIsInstance(balances, list)
        self.assertEqual(len(balances), self.test_params['years'])
        
        # Each year should be greater than the previous (due to growth + contributions)
        for i in range(1, len(balances)):
            self.assertGreater(balances[i], balances[i-1])
        
        # All balances should be positive
        for balance in balances:
            self.assertGreater(balance, 0)
    
    def test_zero_contribution(self):
        """Test with zero annual contribution."""
        result = calculate_brokerage_growth(
            start_year=self.test_params['start_year'],
            years=self.test_params['years'],
            starting_balance=self.test_params['starting_balance'],
            annual_contribution=0,
            contribution_growth_rate=self.test_params['contribution_growth_rate'],
            stock_market_return=self.test_params['stock_market_return'],
            inflation_rate=self.test_params['inflation_rate'],
            return_details=True
        )
        
        # Should still have growth from starting balance
        self.assertGreater(result['final_balance'], self.test_params['starting_balance'])
        
        # All contributions should be zero
        for year_data in result['year_details']:
            self.assertEqual(year_data['contribution'], 0)
    
    def test_zero_starting_balance(self):
        """Test with zero starting balance."""
        result = calculate_brokerage_growth(
            start_year=self.test_params['start_year'],
            years=self.test_params['years'],
            starting_balance=0,
            annual_contribution=self.test_params['annual_contribution'],
            contribution_growth_rate=self.test_params['contribution_growth_rate'],
            stock_market_return=self.test_params['stock_market_return'],
            inflation_rate=self.test_params['inflation_rate'],
            return_details=True
        )
        
        # Should still have growth from contributions
        self.assertGreater(result['final_balance'], 0)
        
        # First year should have contribution but no starting balance growth
        first_year = result['year_details'][0]
        self.assertEqual(first_year['contribution'], self.test_params['annual_contribution'])
    
    def test_contribution_growth(self):
        """Test that contributions grow over time."""
        result = calculate_brokerage_growth(
            start_year=self.test_params['start_year'],
            years=3,
            starting_balance=0,
            annual_contribution=1000,
            contribution_growth_rate=0.05,  # 5% growth
            stock_market_return=0.0,  # No market growth to isolate contribution growth
            inflation_rate=0.0,
            return_details=True
        )
        
        # Contributions should grow by 5% each year
        year_details = result['year_details']
        self.assertAlmostEqual(year_details[0]['contribution'], 1000)
        self.assertAlmostEqual(year_details[1]['contribution'], 1050)  # 1000 * 1.05
        self.assertAlmostEqual(year_details[2]['contribution'], 1102.5)  # 1050 * 1.05
    
    def test_real_vs_nominal_values(self):
        """Test that real values are less than nominal values due to inflation."""
        result = calculate_brokerage_growth(
            start_year=self.test_params['start_year'],
            years=self.test_params['years'],
            starting_balance=self.test_params['starting_balance'],
            annual_contribution=self.test_params['annual_contribution'],
            contribution_growth_rate=self.test_params['contribution_growth_rate'],
            stock_market_return=0.10,  # 10% return (higher than inflation)
            inflation_rate=0.03,  # 3% inflation
            return_details=True
        )
        
        # Real values should be less than nominal values
        self.assertLess(result['final_balance_real'], result['final_balance'])
        self.assertLess(result['total_accumulated_real'], result['total_accumulated'])
        
        # Check year details
        for year_data in result['year_details']:
            self.assertLess(year_data['balance_real'], year_data['balance'])
            # Only check future values when there are years to grow
            if year_data['years_to_grow'] > 0:
                self.assertLess(year_data['future_value_real'], year_data['future_value'])
    
    def test_parameters_consistency(self):
        """Test that parameters are correctly stored and retrieved."""
        result = calculate_brokerage_growth(
            start_year=self.test_params['start_year'],
            years=self.test_params['years'],
            starting_balance=self.test_params['starting_balance'],
            annual_contribution=self.test_params['annual_contribution'],
            contribution_growth_rate=self.test_params['contribution_growth_rate'],
            stock_market_return=self.test_params['stock_market_return'],
            inflation_rate=self.test_params['inflation_rate'],
            return_details=False
        )
        
        params = result['parameters']
        self.assertEqual(params['start_year'], self.test_params['start_year'])
        self.assertEqual(params['years'], self.test_params['years'])
        self.assertEqual(params['starting_balance'], self.test_params['starting_balance'])
        self.assertEqual(params['annual_contribution'], self.test_params['annual_contribution'])
        self.assertEqual(params['contribution_growth_rate'], self.test_params['contribution_growth_rate'])
        self.assertEqual(params['stock_market_return'], self.test_params['stock_market_return'])
        self.assertEqual(params['inflation_rate'], self.test_params['inflation_rate'])
        
        # Check calculated real return
        expected_real_return = self.test_params['stock_market_return'] - self.test_params['inflation_rate']
        self.assertEqual(params['real_return'], expected_real_return)
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test zero years
        result = calculate_brokerage_growth(
            start_year=2025,
            years=0,
            starting_balance=10000,
            annual_contribution=5000,
            return_details=True
        )
        
        self.assertEqual(result['final_balance'], 10000)  # Should be starting balance
        self.assertEqual(len(result['year_details']), 0)
        
        # Test very high growth rates
        result = calculate_brokerage_growth(
            start_year=2025,
            years=2,
            starting_balance=1000,
            annual_contribution=100,
            stock_market_return=0.50,  # 50% return
            return_details=True
        )
        
        # Should have significant growth
        self.assertGreater(result['final_balance'], 1000)
    
    def test_print_functions(self):
        """Test that print functions don't raise exceptions."""
        result = calculate_brokerage_growth(
            start_year=self.test_params['start_year'],
            years=self.test_params['years'],
            starting_balance=self.test_params['starting_balance'],
            annual_contribution=self.test_params['annual_contribution'],
            contribution_growth_rate=self.test_params['contribution_growth_rate'],
            stock_market_return=self.test_params['stock_market_return'],
            inflation_rate=self.test_params['inflation_rate'],
            return_details=True
        )
        
        # These should not raise exceptions
        try:
            print_brokerage_summary(result)
        except Exception as e:
            self.fail(f"print_brokerage_summary raised an exception: {e}")
        
        try:
            print_brokerage_analysis_table(result)
        except Exception as e:
            self.fail(f"print_brokerage_analysis_table raised an exception: {e}")


if __name__ == '__main__':
    unittest.main() 