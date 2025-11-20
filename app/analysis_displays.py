"""Display functions for comprehensive analysis features."""

import streamlit as st
from typing import Dict, List, Any


def show_key_terms(key_terms: Dict[str, Any]):
    """Display key terms extraction results."""
    st.markdown("""
    <div class="custom-card">
        <h3 style="color: var(--text-main); margin-bottom: 0.5rem;">📌 Key Terms & Definitions</h3>
        <p style="color: var(--text-muted);">Important terms, amounts, and concepts identified in the contract</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not key_terms:
        st.info("No key terms data available")
        return
    
    # Defined Terms
    if key_terms.get("defined_terms"):
        st.markdown("#### 📖 Defined Terms")
        for term in key_terms["defined_terms"]:
            with st.expander(f"📝 {term['term']}", expanded=False):
                st.markdown(f"<div style='color: var(--text-muted);'>{term.get('definition', 'No definition available')}</div>", unsafe_allow_html=True)
    
    # Monetary Amounts
    if key_terms.get("monetary_amounts"):
        st.markdown("#### 💰 Monetary Amounts")
        cols = st.columns(min(3, len(key_terms["monetary_amounts"])))
        for idx, amount in enumerate(key_terms["monetary_amounts"][:9]):
            with cols[idx % min(3, len(key_terms["monetary_amounts"]))]:
                context = amount.get('context', 'Not specified')
                if len(context) > 50:
                    context = context[:50] + "..."
                st.markdown(f"""
                <div class="metric-card">
                    <div style="color: var(--secondary); font-weight: 800; font-size: 1.2rem;">
                        {amount['amount']}
                    </div>
                    <div style="color: var(--text-muted); font-size: 0.8rem; margin-top: 0.3rem;">
                        {context}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Important Entities
    if key_terms.get("important_entities"):
        st.markdown("#### 🏢 Companies & Entities")
        entity_cols = st.columns(2)
        for idx, entity in enumerate(key_terms["important_entities"]):
            with entity_cols[idx % 2]:
                st.markdown(f"""
                <div style="background-color: rgba(30, 41, 59, 0.5); padding: 0.8rem; border-radius: 8px; border-left: 3px solid var(--primary); margin-bottom: 0.5rem;">
                    <span style="color: var(--text-main); font-weight: 600;">🏢 {entity}</span>
                </div>
                """, unsafe_allow_html=True)


def show_parties(parties: List[Dict[str, Any]]):
    """Display identified parties."""
    st.markdown("""
    <div class="custom-card">
        <h3 style="color: var(--text-main); margin-bottom: 0.5rem;">👥 Contract Parties</h3>
        <p style="color: var(--text-muted);">Individuals and entities involved in this agreement</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not parties:
        st.info("💡 No parties could be automatically identified. The contract may use non-standard naming conventions.")
        return
    
    # Display parties as cards
    for idx, party in enumerate(parties):
        party_name = party.get('name', 'Unknown Party')
        party_role = party.get('role', 'Unspecified Role')
        
        st.markdown(f"""
        <div class="custom-card" style="border-left: 4px solid var(--primary);">
            <div style="display: flex; align-items: center;">
                <div style="background-color: var(--primary); color: white; width: 45px; height: 45px;
                            border-radius: 50%; display: flex; align-items: center; 
                            justify-content: center; font-weight: 800; font-size: 1.2rem;
                            margin-right: 1rem;">
                    {idx + 1}
                </div>
                <div style="flex: 1;">
                    <div style="color: var(--text-main); font-weight: 800; font-size: 1.2rem; margin-bottom: 0.3rem;">
                        {party_name}
                    </div>
                    <div style="color: var(--primary); font-weight: 700; font-size: 0.95rem;">
                        📋 {party_role}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def show_dates(important_dates: List[Dict[str, Any]]):
    """Display important dates timeline."""
    st.markdown("""
    <div class="custom-card">
        <h3 style="color: var(--text-main); margin-bottom: 0.5rem;">📅 Important Dates & Deadlines</h3>
        <p style="color: var(--text-muted);">Key dates, deadlines, and time periods in the contract</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not important_dates:
        st.info("💡 No specific dates could be automatically extracted. Review the contract text for date information.")
        return
    
    # Group by type
    date_types = {}
    for date in important_dates:
        dtype = date.get('type', 'date')
        if dtype not in date_types:
            date_types[dtype] = []
        date_types[dtype].append(date)
    
    # Display by category
    type_icons = {
        'effective_date': '🟢',
        'expiration': '🔴',
        'renewal': '🔄',
        'deadline': '⏰',
        'term': '📆',
        'date': '📅'
    }
    
    for dtype, dates in date_types.items():
        icon = type_icons.get(dtype, '📅')
        st.markdown(f"""
        <h4 style="color: var(--primary); font-weight: 700; margin-top: 1.5rem; margin-bottom: 1rem;">
            {icon} {dtype.replace('_', ' ').title()}
        </h4>
        """, unsafe_allow_html=True)
        
        for date in dates:
            date_value = date.get('date', 'Unknown Date')
            date_context = date.get('context', 'No context available')
            
            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid var(--accent); padding: 1rem;">
                <div style="color: var(--text-main); font-weight: 800; font-size: 1.1rem; margin-bottom: 0.5rem;">
                    📌 {date_value}
                </div>
                <div style="color: var(--text-muted); font-size: 0.9rem; font-weight: 600;">
                    {date_context}
                </div>
            </div>
            """, unsafe_allow_html=True)


def show_obligations(obligations: Dict[str, Any]):
    """Display obligations and requirements."""
    st.markdown("""
    <div class="custom-card">
        <h3 style="color: var(--text-main); margin-bottom: 0.5rem;">📋 Obligations & Requirements</h3>
        <p style="color: var(--text-muted);">What you must do, must not do, and your rights</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not obligations:
        st.info("💡 No obligations data available")
        return
    
    # Must Do
    if obligations.get("must_do"):
        st.markdown("#### ✅ Must Do (Obligations)")
        for idx, obligation in enumerate(obligations["must_do"], 1):
            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid var(--secondary); padding: 1rem; margin-bottom: 0.8rem;">
                <div style="color: var(--secondary); font-weight: 800; margin-bottom: 0.5rem; font-size: 1rem;">
                    {idx}. Positive Obligation
                </div>
                <div style="color: var(--text-main); font-size: 0.95rem; font-weight: 600;">
                    {obligation}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Must Not Do
    if obligations.get("must_not_do"):
        st.markdown("#### ❌ Must Not Do (Prohibitions)")
        for idx, prohibition in enumerate(obligations["must_not_do"], 1):
            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid var(--danger); padding: 1rem; margin-bottom: 0.8rem;">
                <div style="color: var(--danger); font-weight: 800; margin-bottom: 0.5rem; font-size: 1rem;">
                    {idx}. Prohibition
                </div>
                <div style="color: var(--text-main); font-size: 0.95rem; font-weight: 600;">
                    {prohibition}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Rights
    if obligations.get("rights"):
        st.markdown("#### 🛡️ Your Rights")
        for idx, right in enumerate(obligations["rights"], 1):
            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid var(--primary); padding: 1rem; margin-bottom: 0.8rem;">
                <div style="color: var(--primary); font-weight: 800; margin-bottom: 0.5rem; font-size: 1rem;">
                    {idx}. Right Granted
                </div>
                <div style="color: var(--text-main); font-size: 0.95rem; font-weight: 600;">
                    {right}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Responsibilities
    if obligations.get("responsibilities"):
        st.markdown("#### 📌 General Responsibilities")
        for idx, resp in enumerate(obligations["responsibilities"], 1):
            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid var(--accent); padding: 1rem; margin-bottom: 0.8rem;">
                <div style="color: var(--accent); font-weight: 800; margin-bottom: 0.5rem; font-size: 1rem;">
                    {idx}. Responsibility
                </div>
                <div style="color: var(--text-main); font-size: 0.95rem; font-weight: 600;">
                    {resp}
                </div>
            </div>
            """, unsafe_allow_html=True)

