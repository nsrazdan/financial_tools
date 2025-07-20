# Financial Tools

A collection of financial calculators and tools designed to help with budgeting, retirement planning, and investment analysis.

## Features

- **401(k) Contribution Calculators** - Project future 401(k) balances with historical limit growth
- **IRA and Roth IRA Estimators** - Calculate IRA contributions with income phase-out rules
- **Investment Growth Projections** - Model compound growth with inflation adjustments
- **Beautiful Table Output** - Professional formatting with the `tabulate` library

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/financial_tools.git
   cd financial_tools
   ```

2. **Run the setup script:**

   ```bash
   # Option 1: Using the Python setup script
   python3 setup.py

   # Option 2: Using the shell script (Unix/Linux/macOS)
   ./install.sh

   # Option 3: Manual installation
   pip install -r requirements.txt
   ```

The setup script will:

- ✅ Check Python version compatibility
- 📦 Install required dependencies (`tabulate`)
- 📁 Create necessary directories
- 🧪 Run basic tests to verify installation

## Usage

### IRA Calculator

#### Command Line Interface

```bash
# Basic calculation
python3 scripts/run_masters_calc.py

# Detailed year-by-year breakdown
python3 scripts/run_masters_calc.py --verbose

# Interactive mode to customize parameters
python3 scripts/run_masters_calc.py --interactive
```

#### Graphical User Interface

```bash
# Launch the GUI calculator
python3 run_gui.py

# Or run the GUI directly
python3 gui_calculator.py
```

The GUI provides:

- 📊 **Tabbed interface** with Parameters and Results tabs
- 🎛️ **Easy parameter adjustment** with organized sections
- 📋 **Real-time calculations** with detailed breakdowns
- 🔄 **Reset to defaults** functionality
- 📱 **User-friendly design** with modern styling

### Features

- **Historical 401(k) limit analysis** - Uses real IRS data from 2006-2025
- **Income phase-out calculations** - Accounts for Roth IRA and Traditional IRA limits
- **Inflation-adjusted projections** - Shows both nominal and real (inflation-adjusted) values
- **Professional table output** - Clean, aligned tables with proper formatting

## Project Structure

```
financial_tools/
├── modules/
│   └── masters/
│       ├── calc_401k_savings.py    # 401(k) calculations
│       └── calc_ira_savings.py     # IRA calculations
├── scripts/
│   └── run_masters_calc.py         # Main calculator script
├── gui_calculator.py               # GUI calculator application
├── run_gui.py                      # GUI launcher script
├── setup.py                        # Installation script
├── install.sh                      # Shell installation script
├── install.bat                     # Windows installation script
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Contributing

Feel free to open issues or submit pull requests to improve the tools.

## License

This project is open source and available under the MIT License.
