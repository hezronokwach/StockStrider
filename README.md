# StockStrider
A quantitative finance project to backtest a stock-picking strategy on S&P 500 data. Clean, preprocess, and analyze financial datasets, develop trading signals, and compare performance against the market benchmark with modular Python code. Ideal for quants mastering data-driven investing!

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd StockStrider
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
StockStrider/
├── data/                   # Raw data files
│   ├── sp500.csv          # S&P 500 index data
│   └── stock_prices.csv   # Individual stock price data
├── scripts/               # Python modules
│   ├── __init__.py
│   ├── memory_reducer.py  # Memory optimization utilities
│   ├── preprocessing.py   # Data preprocessing functions
│   ├── create_signal.py   # Trading signal generation
│   ├── backtester.py      # Backtesting framework
│   └── main.py           # Main pipeline orchestration
├── notebook/              # Jupyter notebooks
│   └── analysis.ipynb    # Exploratory data analysis
├── results/               # Output files
│   ├── plots/            # Generated visualizations
│   ├── results.txt       # Backtesting results
│   └── outliers.txt      # Identified data outliers
├── images/                # Saved plots
└── tests/                 # Unit tests
```

## Usage

### Memory Optimization

The `memory_reducer` module optimizes DataFrame memory usage for large financial datasets:

```python
from scripts.memory_reducer import memory_reducer

# Load and optimize CSV data
df = memory_reducer('data/stock_prices.csv')
print(f"Optimized DataFrame shape: {df.shape}")
```

### Running the Complete Pipeline

```bash
python scripts/main.py
```

This will:
1. Load and optimize data memory usage
2. Preprocess and clean the data
3. Generate trading signals
4. Run backtesting analysis
5. Save results and visualizations

## Features

- **Memory Optimization**: Automatically reduces DataFrame memory usage by 30-70%
- **Data Preprocessing**: Handles missing values, outliers, and resampling
- **Signal Generation**: Creates trading signals based on historical performance
- **Backtesting**: Compares strategy performance against S&P 500 benchmark
- **Visualization**: Generates comprehensive plots and analysis

## Results

All results are saved to the `results/` directory:
- `results.txt`: Backtesting performance metrics
- `outliers.txt`: Identified data outliers
- `plots/`: Performance comparison visualizations

## Development

This project follows PEP 8 coding standards with comprehensive docstrings and type hints. See `CODING_STANDARDS.md` for detailed development guidelines.