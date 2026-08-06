"""
analysis.py

Historical Intelligence Engine

Responsible for:
- Market size
- Growth
- Market share
- Competition
- Company summaries
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as plt_sns
import logging

class HistoricalIntelligence:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.outputs_dir = "d:/Cipla AI/outputs"
        os.makedirs(f"{self.outputs_dir}/graphs", exist_ok=True)
        os.makedirs(f"{self.outputs_dir}/tables", exist_ok=True)

    def market_overview(self):
        """Calculate overall market size and growth."""
        logging.info("Calculating market overview...")
        mat_24 = self.df["MAT FEB'24"].sum() if "MAT FEB'24" in self.df.columns else 0
        mat_26 = self.df["MAT FEB'26"].sum() if "MAT FEB'26" in self.df.columns else 0
        
        cagr = ((mat_26 / mat_24) ** (1/2) - 1) if mat_24 > 0 else 0
        
        return {
            "Market Size (MAT FEB'26)": mat_26,
            "Market Size (MAT FEB'24)": mat_24,
            "CAGR": cagr
        }

    def segment_analysis(self):
        """Analyze by Cardiac Segment."""
        logging.info("Calculating segment analysis...")
        segment_col = "CARDIAC SEGMENT" if "CARDIAC SEGMENT" in self.df.columns else "CARDIAC SEGMENT" 
        
        seg_df = self.df.groupby(segment_col).agg({
            "MAT FEB'24": 'sum',
            "MAT FEB'26": 'sum',
            "QTY MAT FEB'26": 'sum'
        }).reset_index()
        
        seg_df["CAGR"] = np.where(seg_df["MAT FEB'24"] > 0, (seg_df["MAT FEB'26"] / seg_df["MAT FEB'24"]) ** (1/2) - 1, 0)
        seg_df["Market Share"] = seg_df["MAT FEB'26"] / seg_df["MAT FEB'26"].sum()
        
        return seg_df

    def company_analysis(self):
        """Analyze by Company."""
        logging.info("Calculating company analysis...")
        comp_df = self.df.groupby("COMPANY").agg({
            "MAT FEB'24": 'sum',
            "MAT FEB'26": 'sum'
        }).reset_index()
        
        comp_df["CAGR"] = np.where(comp_df["MAT FEB'24"] > 0, (comp_df["MAT FEB'26"] / comp_df["MAT FEB'24"]) ** (1/2) - 1, 0)
        comp_df["Market Share"] = comp_df["MAT FEB'26"] / comp_df["MAT FEB'26"].sum()
        
        return comp_df

    def molecule_analysis(self):
        """Analyze by Molecule."""
        logging.info("Calculating molecule analysis...")
        mol_df = self.df.groupby("MOLECULE_DESC").agg({
            "MAT FEB'24": 'sum',
            "MAT FEB'26": 'sum',
            "QTY MAT FEB'26": 'sum'
        }).reset_index()
        
        mol_df["CAGR"] = np.where(mol_df["MAT FEB'24"] > 0, (mol_df["MAT FEB'26"] / mol_df["MAT FEB'24"]) ** (1/2) - 1, 0)
        mol_df["Market Share"] = mol_df["MAT FEB'26"] / mol_df["MAT FEB'26"].sum()
        
        return mol_df

    def competition_analysis(self):
        """Calculate market concentration / competition intensity (HHI-like index or simple count)."""
        logging.info("Calculating competition analysis...")
        # Number of unique companies per segment
        comp_intensity = self.df.groupby("CARDIAC SEGMENT")["COMPANY"].nunique().reset_index()
        comp_intensity.columns = ["CARDIAC SEGMENT", "Num Competitors"]
        return comp_intensity

    def export_summary(self):
        """Generate graphs and summary tables."""
        logging.info("Exporting summaries and graphs...")
        
        seg_df = self.segment_analysis()
        comp_df = self.company_analysis()
        mol_df = self.molecule_analysis()
        
        # Save Tables
        seg_df.to_csv(f"{self.outputs_dir}/tables/segment_summary.csv", index=False)
        comp_df.to_csv(f"{self.outputs_dir}/tables/company_summary.csv", index=False)
        mol_df.to_csv(f"{self.outputs_dir}/tables/molecule_summary.csv", index=False)
        
        # Plot Segment Growth
        plt.figure(figsize=(10, 6))
        top_segs = seg_df.sort_values("MAT FEB'26", ascending=False).head(10)
        plt.bar(top_segs["CARDIAC SEGMENT"], top_segs["MAT FEB'26"])
        plt.title("Top 10 Cardiac Segments by Market Size")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f"{self.outputs_dir}/graphs/Segment_Market_Size.png")
        plt.close()

        # Plot Company Share
        plt.figure(figsize=(8, 8))
        top_comps = comp_df.sort_values("MAT FEB'26", ascending=False).head(5)
        other_sales = comp_df.sort_values("MAT FEB'26", ascending=False).iloc[5:]["MAT FEB'26"].sum()
        
        labels = top_comps["COMPANY"].tolist() + ["Others"]
        sizes = top_comps["MAT FEB'26"].tolist() + [other_sales]
        
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Top 5 Companies Market Share")
        plt.savefig(f"{self.outputs_dir}/graphs/Company_Share.png")
        plt.close()
        
        return {
            "segment": seg_df,
            "company": comp_df,
            "molecule": mol_df
        }

    def run(self):
        return self.export_summary()