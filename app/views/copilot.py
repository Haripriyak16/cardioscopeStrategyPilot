import streamlit as st
import json

def render(opp_df, raw_df):
    st.title("Executive Strategy Copilot")
    st.markdown("Your rule-based, deterministic AI assistant for pharmaceutical strategy.")
    
    questions = [
        "Select a strategic query...",
        "Why is the top molecule ranked first?",
        "Should Cipla invest in this molecule?",
        "Why Partner instead of Build?",
        "What is Cipla's Right-to-Win?",
        "What if competition increases?",
        "What are the highest risks?"
    ]
    
    q = st.selectbox("Ask the Strategy Copilot:", questions)
    
    def render_executive_response(summary, evidence, logic, tradeoffs, risks, rec, conf):
        st.markdown(f"**Executive Summary:** {summary}")
        st.markdown(f"**Supporting Evidence:** {evidence}")
        st.markdown(f"**Business Logic:** {logic}")
        st.markdown(f"**Trade-offs:** {tradeoffs}")
        st.markdown(f"**Risks:** {risks}")
        st.success(f"**Recommendation:** {rec}")
        st.info(f"**Confidence:** {conf}%")
        
    top = opp_df.iloc[0] if not opp_df.empty else None
    
    if q == "Why is the top molecule ranked first?":
        if top is not None:
            exp = top.get('Explanation_Dict', {})
            why = exp.get('Why', ["High composite score"])[0] if exp else "High composite score"
            render_executive_response(
                summary=f"{top['MOLECULE_DESC']} holds the #1 Opportunity Index.",
                evidence=f"Market Score: {top['Market Score']}/10, Growth Score: {top['Growth Score']}/10.",
                logic=why,
                tradeoffs="Focusing here may divert resources from legacy cash-cows.",
                risks=f"Risk Score is {top['Risk Score']}/10.",
                rec=f"Proceed with {top['Strategy']}.",
                conf=top['Confidence Score']
            )
            
    elif q == "Should Cipla invest in this molecule?":
        if top is not None:
            render_executive_response(
                summary="Investment depends on the Right-to-Win vs Opportunity matrix.",
                evidence=f"For {top['MOLECULE_DESC']}, Right-to-Win is {top['Right to Win Score']}/10.",
                logic="High RTW + High Opportunity = Double Down. Low RTW + High Opportunity = Build/Acquire.",
                tradeoffs="High capital expenditure for 'Build' scenarios.",
                risks="Market entry barriers and patent cliffs.",
                rec=top['Strategy'],
                conf=top['Confidence Score']
            )
            
    elif q == "Why Partner instead of Build?":
        partners = opp_df[opp_df['Strategy'] == 'Partner / Selective Approach']
        count = len(partners)
        render_executive_response(
            summary=f"Partnering is recommended for {count} molecules.",
            evidence="These molecules have high Entry Barrier Scores but moderate Right-to-Win.",
            logic="Building from scratch is too slow or capital-intensive in highly competitive spaces.",
            tradeoffs="Lower profit margins due to revenue sharing, but faster time-to-market.",
            risks="Partner dependency and potential IP conflicts.",
            rec="Pursue in-licensing or co-marketing.",
            conf=85.0
        )
        
    elif q == "What is Cipla's Right-to-Win?":
        avg_rtw = opp_df['Right to Win Score'].mean()
        render_executive_response(
            summary=f"Cipla's portfolio average Right-to-Win is {avg_rtw:.1f}/10.",
            evidence="Derived from historical sales dominance and existing capabilities.",
            logic="Cipla excels in established combination therapies but needs to build capabilities in novel biologics.",
            tradeoffs="Over-reliance on historical strengths limits innovation.",
            risks="Disruption by novel mechanisms of action.",
            rec="Leverage existing RTW while acquiring capabilities in adjacent growth areas.",
            conf=92.0
        )
        
    elif q == "What if competition increases?":
        render_executive_response(
            summary="Increased competition aggressively degrades the HHI and Opportunity Index.",
            evidence="The simulation engine uses HHI to exponentially penalize highly saturated markets.",
            logic="As competitors enter, pricing power drops and customer acquisition costs rise.",
            tradeoffs="Maintaining market share will require aggressive pricing (margin erosion).",
            risks="Volume-based legacy molecules will face severe commoditization.",
            rec="Shift focus to molecules with high Entry Barrier Scores (e.g. complex manufacturing or strong IP).",
            conf=88.5
        )
        
    elif q == "What are the highest risks?":
        if not opp_df.empty:
            riskiest = opp_df.sort_values('Risk Score', ascending=False).iloc[0]
            render_executive_response(
                summary=f"The highest strategic risk is {riskiest['MOLECULE_DESC']}.",
                evidence=f"Risk Score: {riskiest['Risk Score']}/10. (Patent Score: {riskiest['Patent Score']}).",
                logic="Impending patent cliffs or extreme red-ocean competition.",
                tradeoffs="Divesting sacrifices short-term cash flow for long-term safety.",
                risks="Sudden revenue drop upon generic entry.",
                rec=f"Consider {riskiest['Strategy']} or immediate risk mitigation.",
                conf=riskiest['Confidence Score']
            )
