"""
Memory optimization module for StockStrider.

This module provides functions to reduce DataFrame memory usage by optimizing
data types for large financial datasets.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union
import logging

logger = logging.getLogger(__name__)


def memory_reducer(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load CSV file and optimize DataFrame memory usage.
    
    This function loads a CSV file and reduces memory usage by converting
    numeric columns to the smallest possible data types based on their
    min/max values.
    
    Args:
        file_path: Path to CSV file to load and optimize
        
    Returns:
        Optimized DataFrame with reduced memory usage
        
    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        ValueError: If the file is empty or invalid
        
    Example:
        >>> df = memory_reducer('data/stock_prices.csv')
        >>> print(f"Memory usage reduced by {reduction_pct:.1f}%")
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Load the CSV file
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Loaded {len(df)} rows from {file_path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"File {file_path} is empty")
    except Exception as e:
        raise ValueError(f"Error reading file {file_path}: {e}")
    
    if df.empty:
        logger.warning("DataFrame is empty")
        return df
    
    # Calculate initial memory usage
    initial_memory = df.memory_usage(deep=True).sum()
    logger.info(f"Initial memory usage: {initial_memory / 1024**2:.2f} MB")
    
    # Optimize numeric columns
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            col_min = df[col].min()
            col_max = df[col].max()
            
            # Skip if column has only NaN values
            if pd.isna(col_min) or pd.isna(col_max):
                continue
            
            # Optimize integers
            if df[col].dtype in ['int64', 'int32', 'int16', 'int8']:
                if col_min >= np.iinfo(np.int8).min and col_max <= np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif col_min >= np.iinfo(np.int16).min and col_max <= np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif col_min >= np.iinfo(np.int32).min and col_max <= np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
            
            # Optimize floats to float32
            elif df[col].dtype in ['float64', 'float32']:
                df[col] = pd.to_numeric(df[col], downcast='float')
    
    # Calculate final memory usage
    final_memory = df.memory_usage(deep=True).sum()
    reduction = (initial_memory - final_memory) / initial_memory * 100
    
    logger.info(f"Final memory usage: {final_memory / 1024**2:.2f} MB")
    logger.info(f"Memory reduction: {reduction:.1f}%")
    
    print(f"Memory optimization complete:")
    print(f"  Initial: {initial_memory / 1024**2:.2f} MB")
    print(f"  Final: {final_memory / 1024**2:.2f} MB")
    print(f"  Reduction: {reduction:.1f}%")
    
    return df