#!/usr/bin/env python3
"""
Unit tests for GUI module
"""

import sys
import os
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestGUI(unittest.TestCase):
    """Test cases for GUI module"""

    def setUp(self):
        """Set up test fixtures"""
        pass

    def test_gui_import(self):
        """Test that GUI module can be imported"""
        try:
            from gui_calculator import FinancialCalculatorGUI
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import GUI module: {e}")

    @patch('tkinter.Tk')
    def test_gui_creation(self, mock_tk):
        """Test that GUI can be created"""
        try:
            from gui_calculator import FinancialCalculatorGUI
            
            # Mock tkinter root
            mock_root = MagicMock()
            mock_tk.return_value = mock_root
            
            # Create GUI instance
            app = FinancialCalculatorGUI(mock_root)
            
            # Test that widgets were created
            self.assertTrue(hasattr(app, 'widgets'))
            self.assertIsInstance(app.widgets, dict)
            self.assertGreater(len(app.widgets), 0)
            
            # Test that defaults were set
            self.assertTrue(hasattr(app, 'default_params'))
            self.assertIsInstance(app.default_params, dict)
            self.assertGreater(len(app.default_params), 0)
            
        except Exception as e:
            self.fail(f"Failed to create GUI: {e}")

    @patch('tkinter.Tk')
    def test_gui_parameter_extraction(self, mock_tk):
        """Test parameter extraction from GUI widgets"""
        try:
            from gui_calculator import FinancialCalculatorGUI
            
            # Mock tkinter root
            mock_root = MagicMock()
            mock_tk.return_value = mock_root
            
            # Create GUI instance
            app = FinancialCalculatorGUI(mock_root)
            
            # Mock widgets with test values
            mock_widgets = {}
            for param_name in app.default_params.keys():
                mock_widget = MagicMock()
                if param_name == "plan_covered":
                    mock_widget.state.return_value = ['selected']
                elif param_name == "filing_status":
                    mock_widget.get.return_value = "single"
                elif param_name in ["magi_growth_rate", "stock_market_return", 
                                  "inflation_rate", "_401k_limit_growth_rate", "brokerage_contribution_growth_rate"]:
                    mock_widget.get.return_value = "5.0"  # 5%
                elif param_name in ["start_year", "years", "age"]:
                    mock_widget.get.return_value = "2025"
                else:
                    mock_widget.get.return_value = "100000"
                mock_widgets[param_name] = mock_widget
            
            app.widgets = mock_widgets
            
            # Test parameter extraction
            params = app.get_parameter_values()
            
            self.assertIsInstance(params, dict)
            self.assertGreater(len(params), 0)
            
            # Test specific parameter conversions
            self.assertEqual(params['filing_status'], "single")
            self.assertEqual(params['magi_growth_rate'], 0.05)  # 5% -> 0.05
            self.assertEqual(params['start_year'], 2025)
            self.assertTrue(params['plan_covered'])
            
        except Exception as e:
            self.fail(f"Failed to test parameter extraction: {e}")

    @patch('tkinter.Tk')
    def test_gui_reset_functionality(self, mock_tk):
        """Test GUI reset to defaults functionality"""
        try:
            from gui_calculator import FinancialCalculatorGUI
            
            # Mock tkinter root
            mock_root = MagicMock()
            mock_tk.return_value = mock_root
            
            # Create GUI instance
            app = FinancialCalculatorGUI(mock_root)
            
            # Mock widgets
            mock_widgets = {}
            for param_name in app.default_params.keys():
                mock_widget = MagicMock()
                mock_widgets[param_name] = mock_widget
            
            app.widgets = mock_widgets
            
            # Test reset functionality
            app.reset_to_defaults()
            
            # Verify that delete and insert were called for each widget
            for param_name, widget in app.widgets.items():
                if param_name not in ["plan_covered", "filing_status"]:
                    widget.delete.assert_called_once_with(0, 'end')  # tkinter uses lowercase 'end'
                    widget.insert.assert_called_once()
            
        except Exception as e:
            self.fail(f"Failed to test reset functionality: {e}")

    def test_gui_default_values(self):
        """Test that GUI has correct default values"""
        try:
            from gui_calculator import FinancialCalculatorGUI
            
            # Test default values without creating actual GUI
            expected_defaults = {
                'start_year': 2025,
                'years': 20,
                'age': 25,
                'filing_status': 'single',
                'starting_magi': 130000,
                'magi_growth_rate': 0.05,
                'plan_covered': True,
                'stock_market_return': 0.07,
                'starting_401k_balance': 50000,
                'inflation_rate': 0.03,
                'starting_401k_principal': 85000,
                '_401k_limit_growth_rate': 0.03,
                'starting_brokerage_balance': 46000,
                'annual_brokerage_contribution': 5000,
                'brokerage_contribution_growth_rate': 0.03
            }
            
            # Create a minimal test to check defaults
            with patch('tkinter.Tk') as mock_tk:
                mock_root = MagicMock()
                mock_tk.return_value = mock_root
                
                app = FinancialCalculatorGUI(mock_root)
                
                for key, expected_value in expected_defaults.items():
                    self.assertEqual(app.default_params[key], expected_value, 
                                   f"Default value for {key} is incorrect")
            
        except Exception as e:
            self.fail(f"Failed to test default values: {e}")

    @patch('tkinter.Tk')
    def test_gui_calculation_integration(self, mock_tk):
        """Test GUI calculation integration"""
        try:
            from gui_calculator import FinancialCalculatorGUI
            
            # Mock tkinter root
            mock_root = MagicMock()
            mock_tk.return_value = mock_root
            
            # Create GUI instance
            app = FinancialCalculatorGUI(mock_root)
            
            # Mock results text widget
            mock_results_text = MagicMock()
            app.results_text = mock_results_text
            
            # Mock widgets with test values
            mock_widgets = {}
            for param_name in app.default_params.keys():
                mock_widget = MagicMock()
                if param_name == "plan_covered":
                    mock_widget.state.return_value = ['selected']
                elif param_name == "filing_status":
                    mock_widget.get.return_value = "single"
                elif param_name in ["magi_growth_rate", "stock_market_return", 
                                  "inflation_rate", "_401k_limit_growth_rate", "brokerage_contribution_growth_rate"]:
                    mock_widget.get.return_value = "5.0"
                elif param_name in ["start_year", "years", "age"]:
                    mock_widget.get.return_value = "2025"
                else:
                    mock_widget.get.return_value = "50000"
                mock_widgets[param_name] = mock_widget
            
            app.widgets = mock_widgets
            
            # Test calculation method (this will test the integration)
            with patch('gui_calculator.get_historical_401k_growth_info') as mock_hist, \
                 patch('gui_calculator.total_ira_contributions_over_years') as mock_ira, \
                 patch('gui_calculator.calculate_total_savings') as mock_total:
                
                # Mock return values
                mock_hist.return_value = {
                    'start_value': 15000,
                    'end_value': 23500,
                    'start_year': 2006,
                    'end_year': 2025,
                    'years_elapsed': 19,
                    'growth_rate': 0.0239
                }
                
                mock_ira.return_value = {
                    'total_accumulated': 7000.0,
                    'total_accumulated_real': 6800.0,
                    'year_details': [{
                        'year': 2025,
                        'age': 25,
                        'magi': 50000,
                        'ira_contribution': 7000,
                        'years_to_grow': 0,
                        'future_value': 7000,
                        'future_value_real': 6800,
                        '401k_balance': 53500,
                        '401k_limit': 23500,
                        '401k_catchup': 0
                    }],
                    'parameters': {}
                }
                
                mock_total.return_value = {
                    'ira_nominal': 7000.0,
                    'ira_real': 6800.0,
                    '401k_nominal': 100000.0,
                    '401k_real': 97000.0,
                    '401k_contributions': 50000.0,
                    'total_nominal': 107000.0,
                    'total_real': 103800.0,
                    'parameters': {},
                    'yearly_breakdown': [{
                        'year': 2025,
                        'age': 25,
                        'ira_contribution': 7000,
                        'ira_future_value': 7000,
                        'ira_future_value_real': 6800,
                        '401k_balance': 100000,
                        '401k_balance_real': 97000,
                        'total_balance': 107000,
                        'total_balance_real': 103800
                    }]
                }
                
                # Call calculate method
                app.calculate()
                
                # Verify that the calculation methods were called
                mock_hist.assert_called_once()
                mock_ira.assert_called_once()
                mock_total.assert_called_once()
                
                # Verify that results text was updated
                mock_results_text.config.assert_called()
                mock_results_text.delete.assert_called()
                mock_results_text.insert.assert_called()
            
        except Exception as e:
            self.fail(f"Failed to test calculation integration: {e}")


if __name__ == '__main__':
    unittest.main() 