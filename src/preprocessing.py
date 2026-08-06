"""
preprocessing.py

Responsible for:
- Loading data
- Cleaning data
- Handling missing values
- Standardizing text
- Saving processed dataset
"""

from pathlib import Path
import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataPreprocessor:
    def __init__(self, raw_path: str):
        self.raw_path = Path(raw_path)
        self.df = None

    def load_data(self):
        """Load dataset (CSV or Excel)."""
        logging.info(f"Loading data from {self.raw_path}")
        if self.raw_path.suffix == '.csv':
            self.df = pd.read_csv(self.raw_path)
        elif self.raw_path.suffix in ['.xls', '.xlsx']:
            self.df = pd.read_excel(self.raw_path)
        else:
            raise ValueError("Unsupported file format. Must be .csv or .xlsx")
        logging.info(f"Loaded {len(self.df)} records.")

    def clean_text_columns(self):
        """Trim spaces and standardize text columns, clean column names."""
        logging.info("Cleaning text columns and headers...")
        # Clean column names
        self.df.columns = [col.strip().upper() for col in self.df.columns]
        
        # Clean text in all string columns
        for col in self.df.select_dtypes(include=['object']).columns:
            self.df[col] = self.df[col].astype(str).str.strip()

    def handle_missing_values(self):
        """Handle null values."""
        logging.info("Handling missing values...")
        # Numeric columns fill with 0
        num_cols = self.df.select_dtypes(include=['number']).columns
        self.df[num_cols] = self.df[num_cols].fillna(0)
        
        # Categorical columns fill with 'Unknown'
        cat_cols = self.df.select_dtypes(include=['object']).columns
        self.df[cat_cols] = self.df[cat_cols].fillna('Unknown')

    def convert_datatypes(self):
        """Convert columns to correct datatype."""
        logging.info("Converting datatypes...")
        # Columns starting with 'MAT', 'Sales', 'QTY', 'PR_' should be numeric
        numeric_prefixes = ('MAT', 'SALES', 'QTY', 'PR_')
        for col in self.df.columns:
            if col.startswith(numeric_prefixes):
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)

    def save_processed_data(self, output_path: str):
        """Save cleaned dataset."""
        out_path = Path(output_path)
        os.makedirs(out_path.parent, exist_ok=True)
        self.df.to_csv(out_path, index=False)
        logging.info(f"Saved processed data to {output_path}")

    def run_pipeline(self, output_path: str):
        """Execute full preprocessing pipeline."""
        self.load_data()
        self.clean_text_columns()
        self.handle_missing_values()
        self.convert_datatypes()
        self.save_processed_data(output_path)
        return self.df