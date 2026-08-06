import sys, os
sys.path.append(os.path.abspath('app'))
import streamlit_app
import pandas as pd
from app.views import home, market, competition, external, copilot, explorer, simulator, report, comparison, knowledge_graph

def main():
    base_dir = "d:/Cipla AI"
    opp_path = f"{base_dir}/outputs/tables/final_recommendations.csv"
    raw_path = f"{base_dir}/data/processed/cardiac_clean.csv"
    
    opp_df = pd.read_csv(opp_path)
    raw_df = pd.read_csv(raw_path)
    
    # Inject V2 Metrics
    import json
    def safe_parse(x):
        try: return json.loads(x)
        except: return {}
    if 'Explanation' in opp_df.columns:
        opp_df['Explanation_Dict'] = opp_df['Explanation'].apply(safe_parse)
        
    opp_df['HHI'] = 10000 / (opp_df['Num Competitors'] + 1).clip(upper=20)
    opp_df['Entry Barrier Score'] = (opp_df['Patent Score'] + (10 - opp_df['Competition Score'])) / 2
    opp_df['Future Opportunity Score'] = (opp_df['Opportunity Score'] + opp_df['Growth Score']*10) / 2
    def map_investment(strat):
        if strat == 'Double Down': return 'Double Down'
        elif strat == 'Build': return 'Build Capability'
        elif strat == 'Partner / Selective Approach': return 'Partner'
        elif strat == 'Explore/Monitor': return 'Monitor'
        elif strat == 'Divest': return 'Avoid'
        else: return 'Expand'
    opp_df['Investment Matrix'] = opp_df['Strategy'].apply(map_investment)
    
    print("Testing home...")
    home.render(opp_df, raw_df)
    
    print("Testing market...")
    market.render(opp_df, raw_df)
    
    print("Testing competition...")
    competition.render(opp_df, raw_df)
    
    print("Testing external...")
    external.render(opp_df, raw_df)
    
    print("Testing copilot...")
    copilot.render(opp_df, raw_df)
    
    print("Testing explorer...")
    explorer.render(opp_df, raw_df)
    
    print("Testing simulator...")
    simulator.render(opp_df, raw_df)
    
    print("Testing report...")
    report.render(opp_df, raw_df)
    
    print("Testing comparison...")
    comparison.render(opp_df, raw_df)
    
    print("Testing knowledge graph...")
    knowledge_graph.render(opp_df, raw_df)
    
    print("All good!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
