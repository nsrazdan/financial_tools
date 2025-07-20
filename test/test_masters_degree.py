#!/usr/bin/env python3
"""
Unit tests for Master's Degree calculator module
"""

import sys
import os
import unittest
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from modules.masters.calc_masters_degree import (
    calculate_masters_degree_cost,
    print_masters_degree_analysis,
    get_enrollment_type_options,
    get_enrollment_type_display_name
)


class TestMastersDegreeCalculator(unittest.TestCase):
    """Test cases for Master's Degree calculator functions"""

    def setUp(self):
        """Set up test fixtures"""
        pass

    def test_calculate_masters_degree_cost_basic(self):
        """Test basic master's degree cost calculation"""
        result = calculate_masters_degree_cost(
            start_year=2025,
            degree_years=2,
            annual_tuition=50000,
            enrollment_type="full_time"
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn('total_tuition_nominal', result)
        self.assertIn('total_tuition_real', result)
        self.assertIn('total_cost_nominal', result)
        self.assertIn('total_cost_real', result)
        self.assertIn('parameters', result)
        
        # Check that values are reasonable
        self.assertGreater(result['total_tuition_nominal'], 0)
        self.assertGreater(result['total_cost_nominal'], result['total_tuition_nominal'])
        self.assertLessEqual(result['total_cost_real'], result['total_cost_nominal'])

    def test_calculate_masters_degree_cost_full_time(self):
        """Test full-time master's degree cost calculation"""
        result = calculate_masters_degree_cost(
            start_year=2025,
            degree_years=2,
            annual_tuition=50000,
            enrollment_type="full_time"
        )
        
        # For 2 years at $50,000 with 3% inflation
        expected_tuition = 50000 + (50000 * 1.03)  # Year 1 + Year 2
        self.assertAlmostEqual(result['total_tuition_nominal'], expected_tuition, delta=100)

    def test_calculate_masters_degree_cost_part_time(self):
        """Test part-time master's degree cost calculation"""
        result = calculate_masters_degree_cost(
            start_year=2025,
            degree_years=2,
            annual_tuition=50000,
            enrollment_type="part_time"
        )
        
        # Part-time should be 70% of full-time cost
        full_time_result = calculate_masters_degree_cost(
            start_year=2025,
            degree_years=2,
            annual_tuition=50000,
            enrollment_type="full_time"
        )
        
        self.assertAlmostEqual(
            result['total_tuition_nominal'], 
            full_time_result['total_tuition_nominal'] * 0.7, 
            delta=100
        )

    def test_calculate_masters_degree_cost_with_inflation(self):
        """Test master's degree cost calculation with inflation"""
        result = calculate_masters_degree_cost(
            start_year=2025,
            degree_years=3,
            annual_tuition=50000,
            enrollment_type="full_time",
            inflation_rate=0.05  # 5% inflation
        )
        
        # Should be higher than without inflation
        no_inflation_result = calculate_masters_degree_cost(
            start_year=2025,
            degree_years=3,
            annual_tuition=50000,
            enrollment_type="full_time",
            inflation_rate=0.0
        )
        
        self.assertGreater(result['total_tuition_nominal'], no_inflation_result['total_tuition_nominal'])

    def test_calculate_masters_degree_cost_detailed(self):
        """Test detailed master's degree cost calculation"""
        result = calculate_masters_degree_cost(
            start_year=2025,
            degree_years=2,
            annual_tuition=50000,
            enrollment_type="full_time",
            return_details=True
        )
        
        self.assertIn('year_details', result)
        self.assertIsInstance(result['year_details'], list)
        self.assertEqual(len(result['year_details']), 2)
        
        # Check year details structure
        first_year = result['year_details'][0]
        expected_keys = ['year', 'tuition_nominal', 'tuition_real', 'cumulative_nominal', 'cumulative_real', 'enrollment_type']
        for key in expected_keys:
            self.assertIn(key, first_year)

    def test_calculate_masters_degree_cost_zero_years(self):
        """Test master's degree cost calculation with zero years"""
        result = calculate_masters_degree_cost(
            start_year=2025,
            degree_years=0,
            annual_tuition=50000,
            enrollment_type="full_time"
        )
        
        self.assertEqual(result['total_tuition_nominal'], 0.0)
        self.assertEqual(result['total_cost_nominal'], 0.0)

    def test_calculate_masters_degree_cost_zero_tuition(self):
        """Test master's degree cost calculation with zero tuition"""
        result = calculate_masters_degree_cost(
            start_year=2025,
            degree_years=2,
            annual_tuition=0,
            enrollment_type="full_time"
        )
        
        self.assertEqual(result['total_tuition_nominal'], 0.0)
        self.assertEqual(result['additional_costs_nominal'], 0.0)
        self.assertEqual(result['total_cost_nominal'], 0.0)

    def test_calculate_masters_degree_cost_negative_inflation(self):
        """Test master's degree cost calculation with negative inflation"""
        result = calculate_masters_degree_cost(
            start_year=2025,
            degree_years=2,
            annual_tuition=50000,
            enrollment_type="full_time",
            inflation_rate=-0.02  # -2% inflation (deflation)
        )
        
        self.assertIsInstance(result, dict)
        self.assertGreater(result['total_tuition_nominal'], 0)

    def test_calculate_masters_degree_cost_long_program(self):
        """Test master's degree cost calculation for longer programs"""
        result = calculate_masters_degree_cost(
            start_year=2025,
            degree_years=5,
            annual_tuition=30000,
            enrollment_type="part_time"
        )
        
        self.assertIsInstance(result, dict)
        self.assertGreater(result['total_tuition_nominal'], 0)
        self.assertGreater(result['total_cost_nominal'], result['total_tuition_nominal'])

    def test_get_enrollment_type_options(self):
        """Test enrollment type options retrieval"""
        options = get_enrollment_type_options()
        
        self.assertIsInstance(options, list)
        self.assertIn("full_time", options)
        self.assertIn("part_time", options)
        self.assertEqual(len(options), 2)

    def test_get_enrollment_type_display_name(self):
        """Test enrollment type display name conversion"""
        self.assertEqual(get_enrollment_type_display_name("full_time"), "Full Time")
        self.assertEqual(get_enrollment_type_display_name("part_time"), "Part Time")
        self.assertEqual(get_enrollment_type_display_name("unknown"), "Unknown")

    def test_masters_degree_cost_parameter_types(self):
        """Test that function handles different parameter types correctly"""
        # Test with integer parameters
        result_int = calculate_masters_degree_cost(
            start_year=2025,
            degree_years=2,
            annual_tuition=50000,
            enrollment_type="full_time"
        )
        
        # Test with float parameters
        result_float = calculate_masters_degree_cost(
            start_year=2025,
            degree_years=2,
            annual_tuition=50000.0,
            enrollment_type="full_time"
        )
        
        self.assertAlmostEqual(result_int['total_cost_nominal'], result_float['total_cost_nominal'], places=2)

    def test_masters_degree_cost_additional_costs(self):
        """Test that additional costs are calculated correctly"""
        result = calculate_masters_degree_cost(
            start_year=2025,
            degree_years=2,
            annual_tuition=50000,
            enrollment_type="full_time"
        )
        
        # Additional costs should be 15% of tuition
        expected_additional_costs = result['total_tuition_nominal'] * 0.15
        self.assertAlmostEqual(result['additional_costs_nominal'], expected_additional_costs, places=2)
        
        # Total cost should be tuition + additional costs
        expected_total = result['total_tuition_nominal'] + result['additional_costs_nominal']
        self.assertAlmostEqual(result['total_cost_nominal'], expected_total, places=2)


if __name__ == '__main__':
    unittest.main() 