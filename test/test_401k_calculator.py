#!/usr/bin/env python3
"""
Unit tests for 401k calculator module
"""

import sys
import os
import unittest
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from modules.masters.calc_401k_savings import total_401k_contributions_over_years


class Test401KCalculator(unittest.TestCase):
    """Test cases for 401k calculator functions"""

    def setUp(self):
        """Set up test fixtures"""
        pass

    def test_total_401k_contributions_basic(self):
        """Test basic 401k contributions calculation"""
        result = total_401k_contributions_over_years(
            start_year=2025,
            years=1,
            starting_age=25,
            starting_principal=0,
            growth_rate=0.03,
            stock_market_growth_rate=0.07
        )
        
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_total_401k_contributions_multiple_years(self):
        """Test 401k contributions over multiple years"""
        result = total_401k_contributions_over_years(
            start_year=2025,
            years=3,
            starting_age=25,
            starting_principal=10000,
            growth_rate=0.03,
            stock_market_growth_rate=0.07
        )
        
        self.assertIsInstance(result, float)
        self.assertGreater(result, 10000)  # Should be greater than starting principal

    def test_total_401k_contributions_with_growth(self):
        """Test 401k contributions with different growth rates"""
        # Test with higher growth rate
        result_high_growth = total_401k_contributions_over_years(
            start_year=2025,
            years=2,
            starting_age=25,
            starting_principal=0,
            growth_rate=0.05,
            stock_market_growth_rate=0.10
        )
        
        # Test with lower growth rate
        result_low_growth = total_401k_contributions_over_years(
            start_year=2025,
            years=2,
            starting_age=25,
            starting_principal=0,
            growth_rate=0.01,
            stock_market_growth_rate=0.05
        )
        
        self.assertGreater(result_high_growth, result_low_growth)

    def test_total_401k_contributions_zero_years(self):
        """Test 401k contributions with zero years"""
        result = total_401k_contributions_over_years(
            start_year=2025,
            years=0,
            starting_age=25,
            starting_principal=10000,
            growth_rate=0.03,
            stock_market_growth_rate=0.07
        )
        
        self.assertEqual(result, 10000)  # Should return starting principal

    def test_total_401k_contributions_zero_principal(self):
        """Test 401k contributions with zero starting principal"""
        result = total_401k_contributions_over_years(
            start_year=2025,
            years=1,
            starting_age=25,
            starting_principal=0,
            growth_rate=0.03,
            stock_market_growth_rate=0.07
        )
        
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)  # Should still have contributions

    def test_total_401k_contributions_negative_growth(self):
        """Test 401k contributions with negative growth rate"""
        result = total_401k_contributions_over_years(
            start_year=2025,
            years=1,
            starting_age=25,
            starting_principal=10000,
            growth_rate=-0.01,
            stock_market_growth_rate=0.07
        )
        
        self.assertIsInstance(result, float)
        # Should still be positive due to stock market growth

    def test_total_401k_contributions_edge_cases(self):
        """Test edge cases for 401k contributions"""
        # Test very high growth rate
        result = total_401k_contributions_over_years(
            start_year=2025,
            years=1,
            starting_age=25,
            starting_principal=0,
            growth_rate=0.50,  # 50% growth
            stock_market_growth_rate=0.20  # 20% stock market growth
        )
        
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

        # Test very low stock market growth
        result = total_401k_contributions_over_years(
            start_year=2025,
            years=1,
            starting_age=25,
            starting_principal=10000,
            growth_rate=0.03,
            stock_market_growth_rate=0.01  # 1% stock market growth
        )
        
        self.assertIsInstance(result, float)
        self.assertGreater(result, 10000)

    def test_total_401k_contributions_long_term(self):
        """Test 401k contributions over a longer period"""
        result = total_401k_contributions_over_years(
            start_year=2025,
            years=20,
            starting_age=25,
            starting_principal=50000,
            growth_rate=0.03,
            stock_market_growth_rate=0.07
        )
        
        self.assertIsInstance(result, float)
        self.assertGreater(result, 50000)  # Should be significantly greater than starting principal

    def test_total_401k_contributions_parameter_types(self):
        """Test that function handles different parameter types correctly"""
        # Test with integer parameters
        result_int = total_401k_contributions_over_years(
            start_year=2025,
            years=1,
            starting_age=25,
            starting_principal=10000,
            growth_rate=0.03,
            stock_market_growth_rate=0.07
        )
        
        # Test with float parameters (only for starting_principal which accepts float)
        result_float = total_401k_contributions_over_years(
            start_year=2025,
            years=1,
            starting_age=25,
            starting_principal=10000.0,  # Only this parameter accepts float
            growth_rate=0.03,
            stock_market_growth_rate=0.07
        )
        
        self.assertAlmostEqual(result_int, result_float, places=2)


if __name__ == '__main__':
    unittest.main() 