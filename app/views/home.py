import streamlit as st

def render(opp_df, raw_df):
    st.title("Executive Dashboard")
    
    # 1. Executive Scorecards
    if not opp_df.empty:
        top_mol = opp_df.iloc[0]
        st.markdown(f"### Top Priority: **{top_mol['MOLECULE_DESC']}**")
        
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Opportunity Index™", f"{top_mol['Opportunity Score']:.1f}/100")
        c2.metric("Confidence Score™", f"{top_mol['Confidence Score']:.1f}%")
        c3.metric("Strategic Fit™", f"{top_mol.get('Strategic Fit Score', 0):.1f}/100")
        c4.metric("Business Impact™", f"{top_mol.get('Business Impact Score', 0):.1f}/100")
        c5.metric("Risk Score™", f"{top_mol.get('Risk Score', 0):.1f}/10")
        
        # 2. Executive Alerts
        st.markdown("### Executive Alerts")
        alerts = []
        if top_mol['Patent Score'] < 4:
            alerts.append(f"**Patent Cliff Risk**: {top_mol['MOLECULE_DESC']} has high patent risk.")
        if top_mol['Num Competitors'] > 15:
            alerts.append(f"**Red Ocean Warning**: {top_mol['MOLECULE_DESC']} faces fierce competition.")
        
        high_risk = opp_df[opp_df['Risk Score'] > 8]
        if not high_risk.empty:
            alerts.append(f"**Strategic Risk**: {len(high_risk)} molecules have a critical risk score > 8.")
            
        if not alerts:
            st.success("No critical alerts today. Pipeline is stable.")
        else:
            for alert in alerts:
                st.error(alert)

    st.markdown("---")
    colA, colB = st.columns(2)
    
    with colA:
        st.markdown("### Top Opportunities")
        st.dataframe(opp_df[['MOLECULE_DESC', 'Strategy', 'Opportunity Score', 'Confidence Score']].head(5), use_container_width=True)

    with colB:
        st.markdown("### Market Snapshot")
        if "CARDIAC SEGMENT" in raw_df.columns:
            st.markdown(f"**Total Segments Analyzed**: {raw_df['CARDIAC SEGMENT'].nunique()}")
        st.markdown(f"**Total Molecules Evaluated**: {len(opp_df)}")
        st.markdown(f"**'Double Down' Investments**: {len(opp_df[opp_df['Strategy'] == 'Double Down'])}")
        st.markdown(f"**'Build' or 'Acquire' Targets**: {len(opp_df[opp_df['Strategy'] == 'Build'])}")
        
        avg_rtw = opp_df['Right to Win Score'].mean()
        st.markdown(f"**Average Cipla Right-to-Win**: {avg_rtw:.1f}/10")
