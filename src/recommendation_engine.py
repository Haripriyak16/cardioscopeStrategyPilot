"""
recommendation_engine.py

Generates explainable recommendations based on the Opportunity Engine output.
"""

import pandas as pd
import logging
import json

class RecommendationEngine:
    def __init__(self, opportunity_df: pd.DataFrame):
        self.df = opportunity_df

    def explain(self, row: pd.Series) -> str:
        """
        Explain WHY an opportunity received its score using rule-based logic.
        Outputs a JSON string containing the AI Reasoning Chain.
        """
        why = []
        why_not = []
        trade_offs = []
        risks = []
        assumptions = ["Market sizes based on MAT FEB'26 data"]
        outlook = []

        # Market
        if row['Market Score'] >= 7.5:
            why.append("Very large established market size")
        elif row['Market Score'] <= 3.0:
            why_not.append("Niche or nascent market size")

        # Growth
        if row['Growth Score'] >= 7.5:
            why.append("Exceptionally high market growth (CAGR)")
            outlook.append("High expected future expansion")
        elif row['Growth Score'] <= 3.0:
            why_not.append("Stagnant or declining market growth")
            
        # Competition
        if row['Competition Score'] >= 7.5:
            why.append("Low competitive intensity")
        elif row['Competition Score'] <= 3.0:
            why_not.append("High competitive intensity (Red Ocean)")
            risks.append("Price erosion due to hyper-competition")

        # Future
        if row['Future Score'] >= 7.5:
            why.append("Strong future potential based on external indicators (Disease burden, Patents, Guidelines)")
            outlook.append("Regulatory and demographic tailwinds")
        elif row['Future Score'] <= 4.0:
            why_not.append("Weak external signaling or impending patent cliffs")
            risks.append("External disruptions")

        # RTW
        if row['Right to Win Score'] >= 7.5:
            why.append("Strong strategic fit and existing Cipla market presence")
            assumptions.append("Cipla can leverage existing distribution channels")
        elif row['Right to Win Score'] <= 3.0:
            why_not.append("Requires building new capabilities or market presence for Cipla")
            risks.append("High barrier to entry for Cipla currently")

        # Trade-offs
        if row['Market Score'] >= 7.5 and row['Competition Score'] <= 3.0:
            trade_offs.append("High Market Size vs High Competition")
        if row['Growth Score'] >= 7.5 and row['Right to Win Score'] <= 3.0:
            trade_offs.append("Hyper Growth vs Zero Existing Market Share (Build vs Buy)")

        if not why:
            why.append("Balanced across all metrics without major positive outliers")
        if not why_not:
            why_not.append("No major detractors identified")
        if not trade_offs:
            trade_offs.append("Straightforward opportunity without extreme conflicting metrics")
        if not risks:
            risks.append("Standard market risks apply")
        if not outlook:
            outlook.append("Stable market trajectory expected")

        reasoning_chain = {
            "Why": why,
            "Why Not": why_not,
            "Trade-offs": trade_offs,
            "Risks": risks,
            "Assumptions": assumptions,
            "Outlook": outlook
        }
        
        return json.dumps(reasoning_chain)
        
    def generate_decision_tree(self, row: pd.Series) -> str:
        tree = []
        tree.append("Decision Tree Trace:")
        if row['Opportunity Score'] >= 70:
            tree.append("├── Is Opportunity Score >= 70? [YES]")
            if row['Right to Win Score'] >= 6:
                tree.append("│   ├── Is Right to Win >= 6? [YES] -> DOUBLE DOWN")
            else:
                tree.append("│   ├── Is Right to Win >= 6? [NO] -> BUILD")
        elif 50 <= row['Opportunity Score'] < 70:
            tree.append("├── Is Opportunity Score >= 70? [NO]")
            tree.append("├── Is Opportunity Score >= 50? [YES]")
            if row['Right to Win Score'] >= 5:
                tree.append("│   ├── Is Right to Win >= 5? [YES] -> PARTNER")
            else:
                tree.append("│   ├── Is Right to Win >= 5? [NO] -> AVOID / MONITOR")
        else:
            tree.append("├── Is Opportunity Score >= 70? [NO]")
            tree.append("├── Is Opportunity Score >= 50? [NO] -> AVOID / MONITOR")
            
        return "\n".join(tree)

    def strategic_recommendations(self):
        """Classify into Double Down, Build, Partner, Avoid based on scores."""
        logging.info("Generating strategic recommendations...")
        
        def categorize(row):
            opp_score = row['Opportunity Score']
            rtw = row['Right to Win Score']
            
            if opp_score >= 70 and rtw >= 6:
                return "Double Down"
            elif opp_score >= 70 and rtw < 6:
                return "Build" # Great opportunity, but low current right-to-win
            elif 50 <= opp_score < 70 and rtw >= 5:
                return "Partner / Selective Approach"
            else:
                return "Avoid / Monitor"
                
        self.df['Strategy'] = self.df.apply(categorize, axis=1)
        self.df['Explanation'] = self.df.apply(self.explain, axis=1)
        self.df['Decision Tree'] = self.df.apply(self.generate_decision_tree, axis=1)
        
        return self.df

    def top_opportunities(self, n=5):
        """Return the top N opportunities."""
        if 'Strategy' not in self.df.columns:
            self.strategic_recommendations()
        return self.df.head(n)

    def export_report(self):
        return self.strategic_recommendations()