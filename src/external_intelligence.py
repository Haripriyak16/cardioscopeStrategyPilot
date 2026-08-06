"""
external_intelligence.py

Reads external signals and converts them into AI-ready scores.
If the external signals file does not exist, it mocks one for demonstration purposes.
"""

import pandas as pd
import numpy as np
import os
import logging

class ExternalIntelligence:
    def __init__(self, external_file: str, historical_df: pd.DataFrame = None):
        self.external_file = external_file
        self.df = None
        self.historical_df = historical_df

    def _generate_mock_data(self):
        """Generate mock external signals based on unique molecules in the historical data."""
        logging.info("External signals file not found. Generating mock data...")
        os.makedirs(os.path.dirname(self.external_file), exist_ok=True)
        
        if self.historical_df is not None and "MOLECULE_DESC" in self.historical_df.columns:
            entities = self.historical_df["MOLECULE_DESC"].dropna().unique()
            entity_col = "MOLECULE_DESC"
        else:
            # Fallback
            entities = [f"Molecule_{i}" for i in range(10)]
            entity_col = "MOLECULE_DESC"
            
        np.random.seed(42)
        mock_df = pd.DataFrame({
            entity_col: entities,
            'Disease Score': np.random.uniform(2, 10, size=len(entities)).round(1),
            'Patent Score': np.random.uniform(0, 10, size=len(entities)).round(1),
            'Innovation Score': np.random.uniform(1, 10, size=len(entities)).round(1),
            'Guideline Score': np.random.uniform(3, 10, size=len(entities)).round(1),
            'Regulatory Score': np.random.uniform(4, 10, size=len(entities)).round(1)
        })
        
        if self.external_file.endswith('.csv'):
            mock_df.to_csv(self.external_file, index=False)
        else:
            mock_df.to_excel(self.external_file, index=False)
            
        logging.info(f"Mock data saved to {self.external_file}")

    def load_external_data(self):
        if not os.path.exists(self.external_file):
            self._generate_mock_data()
            
        logging.info(f"Loading external intelligence from {self.external_file}")
        if self.external_file.endswith('.csv'):
            self.df = pd.read_csv(self.external_file)
        else:
            self.df = pd.read_excel(self.external_file)

    def normalize_scores(self):
        """Normalize all scores to 0-10 just in case they are not."""
        score_cols = ['Disease Score', 'Patent Score', 'Innovation Score', 'Guideline Score', 'Regulatory Score']
        for col in score_cols:
            if col in self.df.columns:
                max_val = self.df[col].max()
                if max_val > 0:
                    self.df[col] = (self.df[col] / max_val) * 10
                self.df[col] = self.df[col].round(1)

    def build_external_score(self):
        """Aggregate external scores into a single External Intelligence score."""
        self.load_external_data()
        self.normalize_scores()
        
        score_cols = ['Disease Score', 'Patent Score', 'Innovation Score', 'Guideline Score', 'Regulatory Score']
        available_cols = [col for col in score_cols if col in self.df.columns]
        
        # Simple average of available external scores
        self.df['External Score'] = self.df[available_cols].mean(axis=1).round(1)
        return self.df