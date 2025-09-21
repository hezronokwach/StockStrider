# Backtesting-SP500 Project Overview

This document provides a comprehensive overview of the **Backtesting-SP500** project, explaining its purpose, components, and the steps required to complete it. The project is designed for aspiring quantitative analysts, simulating a real-world scenario at a hedge fund where you develop and backtest a stock-picking strategy using historical S&P 500 data. Below, we break down what the project is about, what you need to do, and key concepts to make it approachable.

---

## What is the Project About?

The **Backtesting-SP500** project is a hands-on exercise in quantitative finance, focusing on developing and evaluating a stock-picking strategy to outperform the S&P 500 index, which tracks the performance of 500 large U.S. companies. You’ll act as a quantitative analyst tasked with:
1. Cleaning and preprocessing messy financial data (stock prices and S&P 500 index data).
2. Performing exploratory data analysis (EDA) to understand patterns, outliers, and missing values.
3. Creating a stock selection signal based on historical monthly returns.
4. Backtesting the strategy to assess its performance against the S&P 500 benchmark.
5. Visualizing and communicating results effectively.

### Key Objectives
- **Data Quality Management**: Handle missing values, outliers, and errors in financial datasets.
- **Efficient Coding**: Optimize memory usage, avoid loops where possible, and write modular, reusable code.
- **Financial Analysis**: Calculate returns, develop signals, and evaluate strategy performance.
- **Visualization**: Create clear plots to communicate findings to technical and non-technical stakeholders.

The final output is a comparison of your stock-picking strategy (investing $1 in each of the top 20 stocks monthly) against a benchmark strategy (investing $20 monthly in the S&P 500 index).

---

## Project Components

The project is divided into four main parts, orchestrated by a `main.py` script. Here’s an overview of each part:

### 1. Preliminary: Data Loading and Optimization
- **Goal**: Load `sp500.csv` (S&P 500 index data) and `stock_prices.csv` (individual company prices) into Pandas DataFrames and optimize their memory usage.
- **Tasks**:
  - Write a `memory_reducer(paths)` function in `memory_reducer.py` that:
    - Reads CSV files using `pd.read_csv()`.
    - Iterates over columns to check if they’re numeric (`pd.api.types.is_numeric_dtype`).
    - Determines if columns can be integers or floats.
    - Finds min/max values to select the smallest data type (e.g., `np.float32` for floats, `np.int8` for small integers).
    - Applies optimized types using `astype()` or `pd.to_numeric()`.
  - Return optimized `prices` and `sp500` DataFrames.
- **Why It Matters**: Financial datasets are large, and optimizing data types reduces memory usage for faster processing.

### 2. Data Wrangling and Preprocessing
- **Goal**: Perform EDA and preprocess the data to make it suitable for analysis.
- **Tasks**:
  - **Exploratory Data Analysis (EDA)** in `analysis.ipynb`:
    - Load datasets and check missing values (`df.isna().sum()`).
    - Identify outliers (e.g., price spikes) using boxplots or z-scores per company.
    - Visualize trends (e.g., average company prices over time or price consistency across companies).
    - Save plots to the `images` directory.
    - List 5 outliers (ticker, date, price) in `results/outliers.txt`.
  - **Preprocessing `prices.csv`** in `preprocessing.py`:
    - Resample to monthly data, keeping the last value (`resample('M').last()`).
    - Filter prices outside `$0.1` to `$10,000`.
    - Compute:
      - **Historical Returns**: `(price[current month] - price[previous month]) / price[previous month]`.
      - **Future Returns**: `(price[next month] - price[current month]) / price[current month]`.
    - Replace return outliers (> 1 or < -0.5, except during 2008-2009) with the last valid return for the company.
    - Fill missing values with the last available value per company (`ffill`).
    - Drop remaining unfillable NaNs.
    - Print `prices.isna().sum()` to verify.
  - **Preprocessing `sp500.csv`**:
    - Resample to monthly, keeping the last value.
    - Compute historical monthly returns on the adjusted close.
  - **Output**: A `prices` DataFrame with columns: `Price`, `monthly_past_return`, `monthly_future_return`.
- **Why It Matters**: Financial data is messy (missing values, outliers, unadjusted splits). Cleaning ensures reliable analysis, and EDA reveals patterns.

### 3. Create Signal
- **Goal**: Develop a signal to select the top 20 stocks each month based on past performance.
- **Tasks**:
  - Write a `create_signal(prices)` function in `create_signal.py` that:
    - Adds a column `average_return_1y`: the 12-month rolling mean of `monthly_past_return` (`rolling(12).mean()`).
    - Adds a column `signal`: `True` if `average_return_1y` is among the top 20 for that month, `False` otherwise (`groupby('date').nlargest(20, 'average_return_1y')`).
- **Why It Matters**: The signal drives investment decisions, assuming stocks with strong past returns will perform well in the next month.

### 4. Backtesting
- **Goal**: Evaluate the stock-picking strategy and compare it to the S&P 500 benchmark.
- **Tasks**:
  - Write a `backtest(prices, sp500)` function in `backtester.py` that:
    - **Stock-Picking Strategy**:
      - Invest $1 in each of the 20 stocks where `signal = True` each month.
      - Calculate monthly PnL using `monthly_future_return`.
      - Compute cumulative returns over time (`(1 + returns).cumprod() - 1`).
    - **Benchmark Strategy**:
      - Invest $20 monthly in the S&P 500 index.
      - Use `sp500` monthly returns to calculate PnL and cumulative returns.
    - Save PnL and total return for both strategies in `results/results.txt`.
    - Plot cumulative returns for both strategies, saved to `results/plots/w1_weekend_plot_pnl.png`.
  - Use vectorized operations (e.g., `groupby`, `sum`, `cumprod`) instead of loops.
- **Why It Matters**: Backtesting shows how your strategy would have performed historically, validating its effectiveness.

### 5. Main Script
- **Goal**: Orchestrate the entire pipeline in `main.py`.
- **Tasks**:
  - Import functions from `memory_reducer.py`, `preprocessing.py`, `create_signal.py`, and `backtester.py`.
  - Run steps in order: load data, preprocess, create signal, backtest, save results.
  - Ensure `python main.py` produces all outputs (`results.txt`, `outliers.txt`, plots).

---

## Project Structure

The repository should follow this structure:
```
project
│   README.md
│   requirements.txt
│
└───data
│   │   sp500.csv
│   │   prices.csv
│
└───notebook
│   │   analysis.ipynb
|
└───scripts
│   │   memory_reducer.py
│   │   preprocessing.py
│   │   create_signal.py
│   │   backtester.py
│   │   main.py
│
└───results
    │   plots/
    │   results.txt
    │   outliers.txt
```

---

## What You Need to Do: Step-by-Step Guide

Here’s a practical guide to complete the project:

1. **Set Up the Environment**:
   - Create a virtual environment named `ex00` with Python 3.9+:
     ```bash
     python3 -m venv ex00
     source ex00/bin/activate  # On Windows: ex00\Scripts\activate
     ```
   - Install dependencies:
     ```bash
     pip install pandas numpy matplotlib jupyter
     pip freeze > requirements.txt
     ```
   - Launch Jupyter Notebook:
     ```bash
     jupyter notebook
     ```

2. **Preliminary: Memory Optimization**:
   - Write `memory_reducer.py` with a function to optimize DataFrame data types.
   - Test on `sp500.csv` and `stock_prices.csv` (check memory usage with `df.memory_usage().sum()`).

3. **Data Wrangling and Preprocessing**:
   - Create `analysis.ipynb` in the `notebook` folder.
   - Perform EDA:
     - Check missing values (`df.isna().sum()`).
     - Identify outliers per company (e.g., boxplots, z-scores).
     - Visualize average prices over time or across companies using Matplotlib or Pandas.
     - Save 5 outliers to `results/outliers.txt` (format: `ticker,date,price`).
   - Write `preprocessing.py` to:
     - Resample data to monthly.
     - Filter price outliers (`$0.1` to `$10,000`).
     - Compute historical and future returns.
     - Replace return outliers (except 2008-2009).
     - Fill missing values (`ffill`) and drop remaining NaNs.
     - Verify with `prices.isna().sum()`.

4. **Create Signal**:
   - Write `create_signal.py` to:
     - Compute `average_return_1y` (12-month rolling mean).
     - Set `signal = True` for the top 20 stocks per month.

5. **Backtesting**:
   - Write `backtester.py` to:
     - Calculate PnL and cumulative returns for the stock-picking strategy.
     - Compute the same for the S&P 500 benchmark ($20 monthly).
     - Save results to `results/results.txt`.
     - Plot cumulative returns, saved to `results/plots/w1_weekend_plot_pnl.png`.

6. **Main Script**:
   - Write `main.py` to call all functions in order.
   - Test with `python main.py` to ensure outputs are generated.

7. **Test and Validate**:
   - Run `analysis.ipynb` to verify EDA and preprocessing.
   - Test each script individually.
   - Run `main.py` to confirm end-to-end functionality.
   - Check outputs in `results` folder (`results.txt`, `outliers.txt`, plots).

---

## Key Concepts Explained

- **S&P 500**: A stock market index of 500 large U.S. companies. Its components change over time (e.g., Facebook joined in 2013).
- **Stock Picking**: Selecting specific stocks to outperform the index.
- **Returns**: Percentage price change (e.g., `(new_price - old_price) / old_price`).
- **Outliers**: Extreme prices/returns (e.g., data errors, unadjusted splits). Handle per company due to varying price scales.
- **Signal**: A metric (average past 12-month returns) to choose stocks.
- **Backtesting**: Simulating a strategy on historical data to estimate performance.
- **Cumulative Returns**: Compounded returns over time, showing investment growth.
- **Benchmark**: The S&P 500’s performance for comparison.

---

## Example Workflow with Simplified Data

**Sample Data**:
- `prices.csv`:
  ```
  Date,Ticker,Price
  2000-12-31,A,36.73
  2000-12-31,B,25.95
  2000-12-31,AAPL,1.01
  2001-01-31,A,36.60
  2001-01-31,B,28.58
  2001-01-31,AAPL,1.46
  2001-02-28,A,35.00
  2001-02-28,B,1000.00  # Outlier
  2001-02-28,AAPL,1.30
  ```
- `sp500.csv`:
  ```
  Date,Adj Close
  2000-12-31,1320.28
  2001-01-31,1366.01
  2001-02-28,1239.94
  ```

**Workflow**:
1. **Memory Optimization**:
   - Convert `Price` and `Adj Close` to `np.float32`.
2. **Preprocessing**:
   - Filter `B`’s `1000.00` (outlier).
   - Historical Returns (Jan 2001):
     - A: `(36.60 - 36.73) / 36.73 = -0.00354`
     - B: `(28.58 - 25.95) / 25.95 = 0.10135`
     - AAPL: `(1.46 - 1.01) / 1.01 = 0.44554`
   - Future Returns (Jan 2001):
     - A: `(35.00 - 36.60) / 36.60 = -0.04372`
     - B: Replace `1000.00` with `28.58`, so `(28.58 - 28.58) / 28.58 = 0`.
     - AAPL: `(1.30 - 1.46) / 1.46 = -0.10959`
   - S&P 500 Return (Jan 2001): `(1366.01 - 1320.28) / 1320.28 = 0.03467`.
3. **Signal**:
   - For Jan 2001, pick top 2: AAPL (0.44554), B (0.10135). Set `signal = True`.
4. **Backtesting**:
   - Stock-Picking (Jan 2001): PnL = `-0.10959 + 0 = -0.10959`.
   - Benchmark: PnL = `20 * -0.09062 = -1.8124` (Feb 2001).
   - Plot cumulative returns.
5. **Main**: Run all steps and save results.

---

## What You Need to Start

- **Software**:
  - Python 3.9+.
  - Libraries: `pandas`, `numpy`, `matplotlib`, `jupyter`.
  - Install: `pip install pandas numpy matplotlib jupyter`.
- **Skills**:
  - Pandas: Filtering, grouping, resampling, handling NaNs.
  - NumPy: Vectorized operations.
  - Matplotlib: Plotting cumulative returns.
  - Basic financial concepts (returns, backtesting).
- **Files**:
  - `sp500.csv` and `stock_prices.csv` (provided by your instructor).
  - Create the project structure.

---

## Tips for Success

- **Start with EDA**: Explore data in `analysis.ipynb` to understand missing values and outliers.
- **Modularize Code**: Write functions in separate scripts for clarity.
- **Handle Outliers Carefully**: Compare within each company to avoid over-filtering (e.g., preserve 2008-2009 volatility).
- **Avoid Look-Ahead Bias**: Use only past data for signals.
- **Test Incrementally**: Verify each step (e.g., DataFrame shapes, signal counts).
- **Document**: Add comments and explanations in `analysis.ipynb`.

---

## Next Steps

1. **Set Up**: Create the virtual environment and install dependencies.
2. **Explore Data**: Use `analysis.ipynb` for EDA.
3. **Write Scripts**: Implement each part in `memory_reducer.py`, `preprocessing.py`, `create_signal.py`, `backtester.py`.
4. **Test Main**: Run `main.py` to verify outputs.
5. **Submit**: Push to your `StockStrider` repository.

For specific help (e.g., coding `memory_reducer` or plotting), feel free to ask!