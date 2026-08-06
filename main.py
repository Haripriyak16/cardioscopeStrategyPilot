"""
main.py

Main pipeline script for CardioScope AI.
Runs Preprocessing -> Historical Intelligence -> External Intelligence -> Opportunity Engine -> Recommendation Engine
"""

import logging
from src.preprocessing import DataPreprocessor
from src.analysis import HistoricalIntelligence
from src.external_intelligence import ExternalIntelligence
from src.opportunity_engine import OpportunityEngine
from src.recommendation_engine import RecommendationEngine

def run_pipeline():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting CardioScope AI Pipeline...")
    
    # 1. Preprocessing
    preprocessor = DataPreprocessor("d:/Cipla AI/data/raw/Data Set_Ascend Season 4_2026.csv")
    cleaned_df = preprocessor.run_pipeline("d:/Cipla AI/data/processed/cardiac_clean.csv")
    
    # 2. Historical Intelligence
    hist_engine = HistoricalIntelligence(cleaned_df)
    hist_results = hist_engine.run()
    
    # 3. External Intelligence
    ext_engine = ExternalIntelligence("d:/Cipla AI/data/external/external_signals.csv", historical_df=cleaned_df)
    ext_df = ext_engine.build_external_score()
    
    # 4. Opportunity Engine
    opp_engine = OpportunityEngine(historical_df=cleaned_df, external_df=ext_df)
    ranked_opps = opp_engine.run()
    
    # 5. Recommendation Engine
    rec_engine = RecommendationEngine(ranked_opps)
    final_recommendations = rec_engine.export_report()
    
    # Save the final recommendations
    final_recommendations.to_csv("d:/Cipla AI/outputs/tables/final_recommendations.csv", index=False)
    
    logging.info("Pipeline completed successfully! Outputs saved in outputs/ directory.")

if __name__ == "__main__":
    run_pipeline()
