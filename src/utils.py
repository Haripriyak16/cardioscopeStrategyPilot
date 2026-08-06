"""
utils.py

Common helper functions used across the project.
"""

import os
import pandas as pd
import logging

def ensure_directory(path: str):
    """Ensure that a directory exists, create it if it doesn't."""
    os.makedirs(path, exist_ok=True)

def save_csv(df: pd.DataFrame, path: str):
    """Save a DataFrame to CSV, ensuring the directory exists."""
    ensure_directory(os.path.dirname(path))
    df.to_csv(path, index=False)
    logging.info(f"Saved CSV to {path}")

def save_plot(fig, path: str):
    """Save a matplotlib figure, ensuring the directory exists."""
    ensure_directory(os.path.dirname(path))
    fig.savefig(path, bbox_inches='tight')
    logging.info(f"Saved Plot to {path}")