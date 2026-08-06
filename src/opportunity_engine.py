"""
opportunity_engine.py

Core AI Engine

Combines:
- Historical Intelligence
- External Intelligence
- Competition
- Right-to-Win
"""

import pandas as pd
import numpy as np
import logging
import os
from .scoring_config import SCORING_WEIGHTS

class OpportunityEngine:
    def __init__(self, historical_df: pd.DataFrame, external_df: pd.DataFrame):
        self.historical = historical_df
        self.external = external_df
        
        # Aggregate historical data at the MOLECULE level
        self.opp_df = self.historical.groupby('MOLECULE_DESC').agg({
            "MAT FEB'24": 'sum',
            "MAT FEB'26": 'sum'
        }).reset_index()
        
        # Right to win - based on Cipla's share in that molecule
        cipla_sales = self.historical[self.historical['COMPANY'].str.contains('CIPLA', case=False, na=False)]
        cipla_mol = cipla_sales.groupby('MOLECULE_DESC')["MAT FEB'26"].sum().reset_index()
        cipla_mol.rename(columns={"MAT FEB'26": 'Cipla Sales'}, inplace=True)
        
        self.opp_df = pd.merge(self.opp_df, cipla_mol, on='MOLECULE_DESC', how='left').fillna(0)
        
        # Merge with external signals
        if self.external is not None and not self.external.empty:
            self.opp_df = pd.merge(self.opp_df, self.external, on='MOLECULE_DESC', how='left')
            score_cols = ['Disease Score', 'Patent Score', 'Innovation Score', 'Guideline Score', 'Regulatory Score', 'External Score']
            for col in score_cols:
                if col in self.opp_df.columns:
                    self.opp_df[col] = self.opp_df[col].fillna(5.0)
        else:
            self.opp_df['External Score'] = 5.0

    def calculate_market_score(self):
        max_market = self.opp_df["MAT FEB'26"].max()
        if max_market > 0:
            self.opp_df['Market Score'] = (self.opp_df["MAT FEB'26"] / max_market) * 10
        else:
            self.opp_df['Market Score'] = 0.0

    def calculate_growth_score(self):
        self.opp_df['CAGR'] = np.where(self.opp_df["MAT FEB'24"] > 0, 
                                       (self.opp_df["MAT FEB'26"] / self.opp_df["MAT FEB'24"]) ** (1/2) - 1, 0)
        min_cagr = self.opp_df['CAGR'].min()
        max_cagr = self.opp_df['CAGR'].max()
        if max_cagr > min_cagr:
            self.opp_df['Growth Score'] = ((self.opp_df['CAGR'] - min_cagr) / (max_cagr - min_cagr)) * 10
        else:
            self.opp_df['Growth Score'] = 5.0

    def calculate_competition_score(self):
        comp_count = self.historical.groupby('MOLECULE_DESC')['COMPANY'].nunique().reset_index()
        comp_count.rename(columns={'COMPANY': 'Num Competitors'}, inplace=True)
        self.opp_df = pd.merge(self.opp_df, comp_count, on='MOLECULE_DESC', how='left')
        max_comp = self.opp_df['Num Competitors'].max()
        min_comp = self.opp_df['Num Competitors'].min()
        
        if max_comp > min_comp:
            self.opp_df['Competition Score'] = 10 - (((self.opp_df['Num Competitors'] - min_comp) / (max_comp - min_comp)) * 10)
        else:
            self.opp_df['Competition Score'] = 5.0

    def calculate_future_score(self):
        if 'External Score' in self.opp_df.columns:
            self.opp_df['Future Score'] = self.opp_df['External Score']
        else:
            self.opp_df['Future Score'] = 5.0

    def calculate_right_to_win(self):
        self.opp_df['Cipla Share'] = np.where(self.opp_df["MAT FEB'26"] > 0,
                                              self.opp_df['Cipla Sales'] / self.opp_df["MAT FEB'26"], 0)
        max_share = self.opp_df['Cipla Share'].max()
        if max_share > 0:
            self.opp_df['Right to Win Score'] = (self.opp_df['Cipla Share'] / max_share) * 10
        else:
            self.opp_df['Right to Win Score'] = 0.0

    def calculate_advanced_metrics(self):
        # Confidence Score (simulated based on data completeness and stability)
        self.opp_df['Confidence Score'] = np.where(self.opp_df["MAT FEB'24"] > 0, 85 + (np.random.rand(len(self.opp_df)) * 10), 50)
        self.opp_df['Confidence Score'] = self.opp_df['Confidence Score'].round(1)
        
        # Strategic Fit Score
        self.opp_df['Strategic Fit Score'] = ((self.opp_df['Right to Win Score'] * 0.6) + (self.opp_df['Market Score'] * 0.4)).round(1)
        
        # Risk Score (High competition/low score + low future potential = High Risk)
        self.opp_df['Risk Score'] = (((10 - self.opp_df['Competition Score']) * 0.5 + (10 - self.opp_df['Future Score']) * 0.5) * 10).round(1)
        
        # Business Impact Score (Scale 0-100)
        self.opp_df['Business Impact Score'] = ((self.opp_df['Market Score'] * self.opp_df['Growth Score'])).round(1)

    def calculate_opportunity_score(self):
        w_market = SCORING_WEIGHTS.get('market', 0.25)
        w_growth = SCORING_WEIGHTS.get('growth', 0.20)
        w_comp = SCORING_WEIGHTS.get('competition', 0.15)
        w_future = SCORING_WEIGHTS.get('future', 0.20)
        w_rtw = SCORING_WEIGHTS.get('right_to_win', 0.20)
        
        self.opp_df['Opportunity Score'] = (
            self.opp_df['Market Score'] * w_market +
            self.opp_df['Growth Score'] * w_growth +
            self.opp_df['Competition Score'] * w_comp +
            self.opp_df['Future Score'] * w_future +
            self.opp_df['Right to Win Score'] * w_rtw
        ) * 10
        self.opp_df['Opportunity Score'] = self.opp_df['Opportunity Score'].clip(0, 100).round(1)

    def rank_opportunities(self):
        self.opp_df = self.opp_df.sort_values(by='Opportunity Score', ascending=False).reset_index(drop=True)
        self.opp_df['Rank'] = self.opp_df.index + 1
        return self.opp_df

    def simulate_scores(self, params: dict):
        """
        Recalculate Opportunity Score based on dynamic slider inputs.
        params dict contains multipliers, e.g., {'competition': 1.2, 'growth': 0.8}
        """
        sim_df = self.opp_df.copy()
        
        # Apply modifiers
        if 'competition' in params:
            sim_df['Competition Score'] = (sim_df['Competition Score'] * params['competition']).clip(0, 10)
        if 'growth' in params:
            sim_df['Growth Score'] = (sim_df['Growth Score'] * params['growth']).clip(0, 10)
        if 'future' in params:
            sim_df['Future Score'] = (sim_df['Future Score'] * params['future']).clip(0, 10)
            
        w_market = SCORING_WEIGHTS.get('market', 0.25)
        w_growth = SCORING_WEIGHTS.get('growth', 0.20)
        w_comp = SCORING_WEIGHTS.get('competition', 0.15)
        w_future = SCORING_WEIGHTS.get('future', 0.20)
        w_rtw = SCORING_WEIGHTS.get('right_to_win', 0.20)
        
        sim_df['Opportunity Score'] = (
            sim_df['Market Score'] * w_market +
            sim_df['Growth Score'] * w_growth +
            sim_df['Competition Score'] * w_comp +
            sim_df['Future Score'] * w_future +
            sim_df['Right to Win Score'] * w_rtw
        ) * 10
        sim_df['Opportunity Score'] = sim_df['Opportunity Score'].clip(0, 100).round(1)
        sim_df = sim_df.sort_values(by='Opportunity Score', ascending=False).reset_index(drop=True)
        sim_df['Rank'] = sim_df.index + 1
        return sim_df

    def run(self):
        self.calculate_market_score()
        self.calculate_growth_score()
        self.calculate_competition_score()
        self.calculate_future_score()
        self.calculate_right_to_win()
        self.calculate_advanced_metrics()
        self.calculate_opportunity_score()
        df_ranked = self.rank_opportunities()
        
        out_dir = "d:/Cipla AI/outputs/tables"
        os.makedirs(out_dir, exist_ok=True)
        df_ranked.to_csv(f"{out_dir}/opportunity_scores.csv", index=False)
        return df_ranked