"""
Data preprocessing module for StockStrider.

This module provides functions to clean and prepare financial data for analysis.
"""

import pandas as pd
import numpy as np
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


def preprocess_prices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess stock price data with cleaning and feature engineering.
    
    Args:
        df: Raw stock price DataFrame with Date column and ticker columns
        
    Returns:
        Cleaned DataFrame with monthly returns and outlier filtering
    """
    # Convert Date to datetime and set as index
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    # Resample to monthly frequency (keep last value)
    monthly_df = df.resample('M').last()
    
    # Melt to long format for processing
    prices = monthly_df.reset_index().melt(
        id_vars=['Date'], 
        var_name='ticker', 
        value_name='price'
    ).dropna()
    
    # Filter price outliers (remove prices outside $0.1 - $10,000 range)
    prices = prices[(prices['price'] >= 0.1) & (prices['price'] <= 10000.0)]
    
    # Sort by ticker and date for return calculations
    prices = prices.sort_values(['ticker', 'Date'])
    
    # Calculate monthly historical returns: (current - previous) / previous
    prices['monthly_past_return'] = prices.groupby('ticker')['price'].pct_change()
    
    # Calculate monthly future returns: (next - current) / current
    prices['monthly_future_return'] = prices.groupby('ticker')['price'].pct_change().shift(-1)
    
    # Replace return outliers (>1 or <-0.5) except 2008-2009 period
    crisis_mask = (prices['Date'] >= '2008-01-01') & (prices['Date'] <= '2009-12-31')
    outlier_mask = (prices['monthly_past_return'] > 1) | (prices['monthly_past_return'] < -0.5)
    prices.loc[outlier_mask & ~crisis_mask, 'monthly_past_return'] = np.nan
    
    outlier_mask_future = (prices['monthly_future_return'] > 1) | (prices['monthly_future_return'] < -0.5)
    prices.loc[outlier_mask_future & ~crisis_mask, 'monthly_future_return'] = np.nan
    
    # Fill missing values using forward fill per company
    prices['monthly_past_return'] = prices.groupby('ticker')['monthly_past_return'].fillna(method='ffill')
    prices['monthly_future_return'] = prices.groupby('ticker')['monthly_future_return'].fillna(method='ffill')
    
    # Drop remaining unfillable NaN values
    prices = prices.dropna()
    
    # Print final missing values verification
    print(f"Final missing values: {prices.isna().sum().sum()}")
    
    return prices


def preprocess_sp500(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess S&P 500 index data.
    
    Args:
        df: Raw S&P 500 DataFrame with Date and price columns
        
    Returns:
        Cleaned S&P 500 DataFrame with monthly returns
    """
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    # Use Adjusted Close for S&P 500
    if 'Adjusted Close' in df.columns:
        df['price'] = df['Adjusted Close']
    elif 'Close' in df.columns:
        df['price'] = df['Close']
    else:
        raise ValueError("No Close or Adjusted Close column found")
    
    # Resample to monthly frequency
    monthly_sp500 = df[['price']].resample('M').last()
    
    # Calculate returns
    monthly_sp500['monthly_past_return'] = monthly_sp500['price'].pct_change()
    monthly_sp500['monthly_future_return'] = monthly_sp500['price'].pct_change().shift(-1)
    
    # Add ticker column for consistency
    monthly_sp500['ticker'] = 'SPY'
    monthly_sp500 = monthly_sp500.reset_index()
    
    # Drop NaN values
    monthly_sp500 = monthly_sp500.dropna()
    
    return monthly_sp500


if __name__ == "__main__":
    # Test preprocessing functions
    from memory_reducer import memory_reducer
    
    print("Testing stock prices preprocessing:")
    stock_df = memory_reducer('data/stock_prices.csv')
    processed_stocks = preprocess_prices(stock_df)
    print(f"Processed stocks shape: {processed_stocks.shape}")
    print(f"Date range: {processed_stocks['Date'].min()} to {processed_stocks['Date'].max()}")
    
    print("\nTesting S&P 500 preprocessing:")
    sp500_df = memory_reducer('data/sp500.csv')
    processed_sp500 = preprocess_sp500(sp500_df)
    print(f"Processed S&P 500 shape: {processed_sp500.shape}")
    print(f"Date range: {processed_sp500['Date'].min()} to {processed_sp500['Date'].max()}")