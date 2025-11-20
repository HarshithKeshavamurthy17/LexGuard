"""LexGuard Enhanced UI - Beautiful, Modern, Comprehensive Contract Analysis."""

import streamlit as st
import httpx
import pandas as pd
from datetime import datetime
import time
import re
import plotly.graph_objects as go
import plotly.express as px
from app.analysis_displays import show_key_terms, show_parties, show_dates, show_obligations

# Configure page with custom theme
st.set_page_config(
    page_title="LexGuard – AI Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API base URL
API_BASE_URL = "http://localhost:8000/api"

# Enhanced Custom CSS with modern design and theme compatibility
st.markdown(
    """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Global Variables */
    :root {
        --primary: #4f46e5;
        --primary-dark: #4338ca;
        --secondary: #10b981;
        --accent: #f59e0b;
        --danger: #ef4444;
        --background: #0f172a;
        --surface: #1e293b;
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
    }

    /* Base Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    /* Custom Containers with Theme-Aware Colors */
    .custom-card {
        background-color: var(--surface);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    .metric-card {
        border-radius: 16px;
        border: 2px solid #818cf8;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.15);
        transition: all 0.3s ease;
        margin: 0.5rem 0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.3);
        border-color: #4f46e5;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        margin: 0.5rem 0;
        color: #111827;
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: #4b5563;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Risk levels with solid bright colors */
    .risk-high {
        color: #dc2626;
        font-weight: 800;
        text-shadow: 0 2px 4px rgba(220, 38, 38, 0.2);
    }
    
    .risk-medium {
        color: #f59e0b;
        font-weight: 800;
        text-shadow: 0 2px 4px rgba(245, 158, 11, 0.2);
    }
    
    .risk-low {
        color: #059669;
        font-weight: 800;
        text-shadow: 0 2px 4px rgba(5, 150, 105, 0.2);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white !important;
        font-weight: 700;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        border: none;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.5);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.7);
        background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%);
    }
    
    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    .css-1d391kg .stMarkdown, [data-testid="stSidebar"] .stMarkdown {
        color: #f1f5f9 !important;
    }
    
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {
        color: #ffffff !important;
        font-weight: 700;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
        border-bottom: 2px solid #e5e7eb;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f8fafc;
        border-radius: 12px 12px 0 0;
        padding: 12px 24px;
        font-weight: 700;
        border: 2px solid #e5e7eb;
        border-bottom: none;
        transition: all 0.3s ease;
        color: #4b5563 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white !important;
        border-color: #4f46e5;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    
    /* Chat messages */
    .stChatMessage {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid #e5e7eb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        border-radius: 10px;
        height: 12px;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border-radius: 12px;
        font-weight: 700;
        border: 2px solid #cbd5e1;
        transition: all 0.3s ease;
        color: #1e293b !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #4f46e5;
        background: #eef2ff;
        box-shadow: 0 2px 8px rgba(79, 70, 229, 0.2);
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid #4f46e5;
        background: #eef2ff;
        color: #1e293b !important;
        font-weight: 500;
    }
    
    /* Success boxes */
    .stSuccess {
        border-radius: 12px;
        border-left: 5px solid #059669;
        background: #d1fae5;
        color: #064e3b !important;
        font-weight: 500;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Global text visibility fixes */
    p, span, div, label {
        color: #1f2937 !important;
    }
    
    /* Streamlit markdown text */
    .stMarkdown p {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
    
    /* Captions */
    .stCaption, small {
        color: #4b5563 !important;
        font-weight: 600 !important;
    }
    
    /* Expander content */
    .streamlit-expanderContent {
        background: #ffffff;
        color: #1f2937 !important;
    }
    
    .streamlit-expanderContent p, .streamlit-expanderContent div {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
    
    /* Input text */
    input, textarea {
        color: #111827 !important;
        font-weight: 600 !important;
    }
    
    /* Selectbox text */
    .stSelectbox label, .stMultiSelect label {
        color: #111827 !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
    }
    
    /* Multiselect selected items */
    .stMultiSelect [data-baseweb="tag"] {
        background: #dc2626 !important;
        color: white !important;
        font-weight: 700 !important;
    }
    
    /* Expander header text */
    .streamlit-expanderHeader p {
        color: #111827 !important;
        font-weight: 800 !important;
    }
    
    /* Expander header */
    .streamlit-expanderHeader {
        color: #111827 !important;
    }
    
    /* File uploader text */
    .stFileUploader label {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
    }
    
    /* Chat message text */
    .stChatMessage p, .stChatMessage div {
        color: #111827 !important;
        font-weight: 600 !important;
    }
    
    /* Badge styles */
    .badge {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 800;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0.2rem;
    }
    
    .badge-high {
        background: #dc2626;
        color: white;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.5);
    }
    
    .badge-medium {
        background: #f59e0b;
        color: white;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.5);
    }
    
    .badge-low {
        background: #059669;
        color: white;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.5);
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* File uploader */
    .stFileUploader {
        border: 3px dashed #667eea;
        border-radius: 16px;
        padding: 2rem;
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_session_state():
    """Initialize session state variables."""
    if "contract_id" not in st.session_state:
        st.session_state.contract_id = None
    if "contract_data" not in st.session_state:
        st.session_state.contract_data = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "selected_clause" not in st.session_state:
        st.session_state.selected_clause = None


# API functions (same as before but with better error handling)
def upload_file(file):
    """Upload a contract file to the API."""
    try:
        with st.spinner("🔄 Analyzing your contract with AI..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("📄 Uploading document...")
            progress_bar.progress(20)
            
            with httpx.Client(timeout=180.0) as client:
                files = {"file": (file.name, file, "application/pdf")}
                
                status_text.text("🤖 Extracting text and clauses...")
                progress_bar.progress(40)
                
                response = client.post(f"{API_BASE_URL}/upload", files=files)
                response.raise_for_status()
                
                status_text.text("🎯 Classifying clauses...")
                progress_bar.progress(60)
                time.sleep(0.5)
                
                status_text.text("⚠️ Analyzing risks...")
                progress_bar.progress(80)
                time.sleep(0.5)
                
                status_text.text("✅ Generating insights...")
                progress_bar.progress(100)
                time.sleep(0.3)
                
                progress_bar.empty()
                status_text.empty()
                
                return response.json()
    except httpx.HTTPError as e:
        st.error(f"❌ Upload failed: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return None


def get_contract_details(contract_id):
    """Fetch contract details from API."""
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(f"{API_BASE_URL}/contracts/{contract_id}")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        st.error(f"Error fetching contract: {str(e)}")
        return None


def get_risk_data(contract_id):
    """Fetch risk assessment data."""
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(f"{API_BASE_URL}/contracts/{contract_id}/risk")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        st.error(f"Error fetching risk data: {str(e)}")
        return None


def get_clauses(contract_id):
    """Fetch all clauses."""
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(f"{API_BASE_URL}/contracts/{contract_id}/clauses")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        st.error(f"Error fetching clauses: {str(e)}")
        return None


def get_comprehensive_analysis(contract_id):
    """Fetch comprehensive analysis data."""
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(f"{API_BASE_URL}/contracts/{contract_id}/analysis")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        st.error(f"Error fetching comprehensive analysis: {str(e)}")
        return None


def chat_with_contract(contract_id, query):
    """Send a chat query to the API."""
    try:
        with httpx.Client(timeout=90.0) as client:
            response = client.post(
                f"{API_BASE_URL}/contracts/{contract_id}/chat", json={"query": query}
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        st.error(f"Error in chat: {str(e)}")
        return None


def download_report(contract_id):
    """Get download URL for PDF report."""
    return f"{API_BASE_URL}/contracts/{contract_id}/report"


def download_docx_report(contract_id):
    """Get download URL for Word report."""
    return f"{API_BASE_URL}/contracts/{contract_id}/report/docx"


def update_clause(contract_id, clause_id, text):
    """Update and re-analyze a clause."""
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{API_BASE_URL}/contracts/{contract_id}/clauses/{clause_id}/analyze",
                json={"text": text}
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        st.error(f"Error updating clause: {str(e)}")
        return None


def get_all_contracts():
    """Fetch all contracts."""
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.get(f"{API_BASE_URL}/contracts")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        st.error(f"Error fetching contracts: {str(e)}")
        return []


def main():
    """Main Streamlit application."""
    initialize_session_state()

    # Animated header
    st.markdown(
        '<div class="main-header">⚖️ LexGuard AI</div>', 
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sub-header">Professional Contract Analysis Powered by AI</div>',
        unsafe_allow_html=True,
    )

    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Quick Actions")
        st.markdown("---")

        # Upload Section
        st.markdown("#### 📤 Upload Contract")
        uploaded_file = st.file_uploader(
            "Drop your PDF here",
            type=["pdf"],
            help="Upload a legal contract for instant AI analysis",
            label_visibility="collapsed"
        )

        if uploaded_file is not None:
            if st.button("🚀 Analyze Document", type="primary"):
                result = upload_file(uploaded_file)
                if result:
                    st.session_state.contract_id = result["contract_id"]
                    st.success(f"✅ Found {result['clause_count']} clauses!")
                    st.balloons()
                    time.sleep(0.5)
                    st.rerun()

        st.markdown("---")

        if st.session_state.contract_id:
            st.success("📄 Contract Loaded")
            
            if st.button("🔄 New Analysis"):
                st.session_state.contract_id = None
                st.session_state.contract_data = None
                st.session_state.chat_history = []
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 🌟 Features")
        st.markdown("✅ AI-Powered Analysis")
        st.markdown("✅ Risk Scoring")
        st.markdown("✅ Smart Q&A")
        st.markdown("✅ PDF Reports")
        st.markdown("✅ 100% Private")

    # Main content
    if st.session_state.contract_id:
        show_contract_analysis()
    else:
        show_welcome_screen()


def show_welcome_screen():
    """Display enhanced welcome screen."""
    st.markdown("---")

    # Feature cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <div style="font-size: 3rem;">📄</div>
            <h3 style="color: #111827; font-weight: 800;">Upload</h3>
            <p style="color: #1f2937; font-weight: 600; font-size: 1rem;">Drag & drop your contracts for instant analysis</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <div style="font-size: 3rem;">🎯</div>
            <h3 style="color: #111827; font-weight: 800;">Analyze</h3>
            <p style="color: #1f2937; font-weight: 600; font-size: 1rem;">AI classifies clauses & identifies risks</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <div style="font-size: 3rem;">💬</div>
            <h3 style="color: #111827; font-weight: 800;">Chat</h3>
            <p style="color: #1f2937; font-weight: 600; font-size: 1rem;">Ask questions in natural language</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card" style="text-align: center;">
            <div style="font-size: 3rem;">📊</div>
            <h3 style="color: #111827; font-weight: 800;">Report</h3>
            <p style="color: #1f2937; font-weight: 600; font-size: 1rem;">Download professional PDF reports</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Benefits section with dark text
    st.markdown("""
    <h3 style="color: #111827; font-weight: 800; font-size: 1.8rem;">🚀 Why LexGuard?</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="color: #1f2937; font-weight: 600; font-size: 1.1rem; line-height: 2rem;">
        • ⚡ <strong style="color: #111827;">Lightning Fast</strong> - Analysis in seconds<br>
        • 🔒 <strong style="color: #111827;">100% Private</strong> - Data stays on your computer<br>
        • 🎯 <strong style="color: #111827;">Accurate</strong> - AI-powered classification<br>
        • 💰 <strong style="color: #111827;">Free</strong> - Unlimited analyses with Ollama
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="color: #1f2937; font-weight: 600; font-size: 1.1rem; line-height: 2rem;">
        • 📊 <strong style="color: #111827;">Comprehensive</strong> - Detailed risk breakdowns<br>
        • 💬 <strong style="color: #111827;">Interactive</strong> - Chat with your contracts<br>
        • 📄 <strong style="color: #111827;">Professional</strong> - Export lawyer-quality reports<br>
        • 🎨 <strong style="color: #111827;">Beautiful</strong> - Modern, intuitive interface
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    st.markdown("""
    <div style="background: #4f46e5; padding: 1.5rem; border-radius: 12px; text-align: center; margin: 2rem 0;">
        <h3 style="color: white; font-weight: 800; font-size: 1.5rem; margin: 0;">
            👈 Get Started: Upload a contract using the sidebar!
        </h3>
    </div>
    """, unsafe_allow_html=True)


def show_contract_analysis():
    """Display enhanced contract analysis dashboard."""
    contract_id = st.session_state.contract_id

    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard", 
        "📋 Clauses", 
        "💬 AI Chat", 
        "📄 Report",
        "🔍 Deep Analysis",
        "⚔️ Compare"
    ])

    with tab1:
        show_enhanced_dashboard(contract_id)

    with tab2:
        show_enhanced_clauses(contract_id)

    with tab3:
        show_enhanced_chat(contract_id)

    with tab4:
        show_report_section(contract_id)
    
    with tab5:
        show_deep_analysis(contract_id)

    with tab6:
        show_comparison_interface(contract_id)


def show_enhanced_dashboard(contract_id):
    """Show enhanced dashboard with beautiful visualizations."""
    st.markdown("""
    <h2 style="color: #111827; font-weight: 800; font-size: 2rem;">📊 Contract Dashboard</h2>
    """, unsafe_allow_html=True)
    
    # Fetch data
    risk_data = get_risk_data(contract_id)
    contract_data = get_contract_details(contract_id)

    if not risk_data or not contract_data:
        st.error("Failed to load data")
        return

    # Top metrics with enhanced design
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Clauses</div>
            <div class="metric-value" style="color: #667eea;">{risk_data["total_clauses"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🔴 High Risk</div>
            <div class="metric-value risk-high">{risk_data["high_risk_count"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🟡 Medium Risk</div>
            <div class="metric-value risk-medium">{risk_data["medium_risk_count"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🟢 Low Risk</div>
            <div class="metric-value risk-low">{risk_data["low_risk_count"]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Create beautiful visualizations
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        <h3 style="color: #111827; font-weight: 800; font-size: 1.3rem;">📈 Risk Distribution</h3>
        """, unsafe_allow_html=True)
        
        # Donut chart
        fig = go.Figure(data=[go.Pie(
            labels=['High Risk', 'Medium Risk', 'Low Risk'],
            values=[risk_data["high_risk_count"], risk_data["medium_risk_count"], risk_data["low_risk_count"]],
            hole=.6,
            marker=dict(colors=['#ef4444', '#f59e0b', '#10b981']),
            textinfo='label+percent',
            textfont=dict(size=14, family='Inter', weight='bold')
        )])
        
        fig.update_layout(
            showlegend=True,
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', size=12, color='#111827'),
            legend=dict(
                font=dict(size=12, color='#111827', family='Inter'),
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#e5e7eb',
                borderwidth=1
            ),
            annotations=[dict(
                text=f'{risk_data["total_clauses"]}<br>Clauses', 
                x=0.5, y=0.5, 
                font_size=24, 
                font_color='#111827',
                showarrow=False
            )]
        )
        
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("""
        <h3 style="color: #111827; font-weight: 800; font-size: 1.3rem;">🎯 Risk Score by Clause Type</h3>
        """, unsafe_allow_html=True)
        
        # Get clause data for visualization
        clauses = get_clauses(contract_id)
        if clauses:
            clause_types = {}
            for clause in clauses:
                ctype = clause['clause_type'].replace('_', ' ').title()
                risk = clause.get('risk_score', 0)
                if ctype not in clause_types:
                    clause_types[ctype] = []
                clause_types[ctype].append(risk)
            
            avg_risks = {k: sum(v)/len(v) for k, v in clause_types.items()}
            
            fig = go.Figure(data=[go.Bar(
                x=list(avg_risks.keys()),
                y=list(avg_risks.values()),
                marker=dict(
                    color=list(avg_risks.values()),
                    colorscale=[[0, '#10b981'], [0.5, '#f59e0b'], [1, '#ef4444']],
                    showscale=False
                ),
                text=[f'{v:.2f}' for v in avg_risks.values()],
                textposition='outside',
            )])
            
            fig.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', size=12, color='#111827'),
                xaxis=dict(
                    title=dict(text='Clause Type', font=dict(size=13, color='#111827', family='Inter')),
                    tickfont=dict(size=11, color='#111827', family='Inter'),
                    gridcolor='#e5e7eb',
                    gridwidth=1
                ),
                yaxis=dict(
                    title=dict(text='Avg Risk Score', font=dict(size=13, color='#111827', family='Inter')),
                    tickfont=dict(size=11, color='#111827', family='Inter'),
                    range=[0, 1],
                    gridcolor='#e5e7eb',
                    gridwidth=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Contract summary
    st.markdown("""
    <h3 style="color: #111827; font-weight: 800; font-size: 1.5rem;">📝 AI-Generated Summary</h3>
    """, unsafe_allow_html=True)
    with st.container():
        st.markdown(f"""
        <div style="background: #f8fafc; 
                    padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4f46e5;
                    color: #1f2937; font-weight: 500; font-size: 1.05rem; line-height: 1.8;">
            {contract_data.get("summary", "Generating summary...")}
        </div>
        """, unsafe_allow_html=True)


def show_enhanced_clauses(contract_id):
    """Show enhanced clause viewer."""
    st.markdown("""
    <h2 style="color: #111827; font-weight: 800; font-size: 2rem;">📋 Clause Analysis</h2>
    """, unsafe_allow_html=True)

    clauses = get_clauses(contract_id)

    if not clauses:
        st.error("Failed to load clauses")
        return

    # Filters
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        risk_filter = st.multiselect(
            "Filter by Risk Level",
            options=["high", "medium", "low"],
            default=["high", "medium", "low"],
        )
    
    with col2:
        type_filter = st.multiselect(
            "Filter by Type",
            options=list(set([c['clause_type'] for c in clauses])),
            default=list(set([c['clause_type'] for c in clauses]))
        )
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Risk (High to Low)", "Risk (Low to High)", "Index"])

    # Filter and sort
    filtered_clauses = [
        c for c in clauses 
        if c.get("risk_level") in risk_filter and c['clause_type'] in type_filter
    ]
    
    if sort_by == "Risk (High to Low)":
        filtered_clauses = sorted(filtered_clauses, key=lambda x: x.get('risk_score', 0), reverse=True)
    elif sort_by == "Risk (Low to High)":
        filtered_clauses = sorted(filtered_clauses, key=lambda x: x.get('risk_score', 0))

    st.markdown(f"""
    <p style="color: #111827; font-weight: 700; font-size: 1.1rem;">
        Showing {len(filtered_clauses)} of {len(clauses)} clauses
    </p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Display clauses beautifully
    for i, clause in enumerate(filtered_clauses, 1):
        risk_level = clause.get("risk_level", "unknown")
        risk_score = clause.get('risk_score', 0)
        
        # Risk badge
        badge_class = f"badge-{risk_level}"
        risk_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(risk_level, "⚪")
        
        with st.expander(
            f"{risk_emoji} Clause {i}: {clause['clause_type'].replace('_', ' ').title()} - Risk: {risk_level.upper()}",
            expanded=(i <= 2 and risk_level == "high"),
        ):
            # Header row with type, risk score, and badge
            header_col1, header_col2, header_col3 = st.columns([2, 2, 1])
            
            with header_col1:
                st.markdown(f"""
                <div style="margin-bottom: 0.5rem;">
                    <span style="color: #4b5563; font-weight: 700; font-size: 0.9rem;">Type:</span>
                    <span style="color: #111827; font-weight: 700; font-size: 1rem; margin-left: 0.5rem;">
                        {clause['clause_type'].replace('_', ' ').title()}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            with header_col2:
                st.markdown(f"""
                <div style="margin-bottom: 0.5rem;">
                    <span style="color: #4b5563; font-weight: 700; font-size: 0.9rem;">Risk Score:</span>
                    <span style="color: #111827; font-weight: 800; font-size: 1rem; margin-left: 0.5rem;">
                        {risk_score:.2f}/1.00
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            with header_col3:
                st.markdown(f'<div style="text-align: right;"><span class="badge {badge_class}">{risk_level.upper()}</span></div>', 
                          unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Clause text with proper alignment
            st.markdown("""
            <div style="margin-bottom: 0.5rem;">
                <span style="color: #111827; font-weight: 800; font-size: 1.1rem;">Clause Text:</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Clean and format clause text - replace multiple spaces/newlines with single space
            cleaned_text = re.sub(r'\s+', ' ', clause["text"].strip())
            
            st.markdown(f"""
            <div style="background: #f0f9ff; padding: 1.5rem; border-radius: 12px; 
                        border-left: 4px solid #3b82f6; margin: 0.5rem 0 1rem 0;
                        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);">
                <p style="color: #1e293b; font-size: 1.05rem; font-weight: 600; 
                         line-height: 1.8; margin: 0; text-align: left; 
                         word-wrap: break-word; white-space: normal; 
                         display: block; text-overflow: ellipsis;">
                    {cleaned_text}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bar for risk
            st.markdown("""
            <div style="margin-top: 0.5rem; margin-bottom: 0.5rem;">
                <span style="color: #4b5563; font-weight: 700; font-size: 0.9rem;">Risk Level:</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress(risk_score)

            # Edit button
            if st.button("✏️ Edit Clause", key=f"edit_{clause['id']}"):
                st.session_state[f"editing_{clause['id']}"] = True
            
            if st.session_state.get(f"editing_{clause['id']}", False):
                new_text = st.text_area("Edit Clause Text", value=clause["text"], key=f"text_{clause['id']}")
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button("💾 Save & Re-analyze", key=f"save_{clause['id']}"):
                        with st.spinner("Re-analyzing..."):
                            updated_clause = update_clause(contract_id, clause['id'], new_text)
                            if updated_clause:
                                st.success("Clause updated!")
                                st.session_state[f"editing_{clause['id']}"] = False
                                time.sleep(1)
                                st.rerun()
                with col_cancel:
                    if st.button("❌ Cancel", key=f"cancel_{clause['id']}"):
                        st.session_state[f"editing_{clause['id']}"] = False
                        st.rerun()


def show_enhanced_chat(contract_id):
    """Show enhanced chat interface."""
    st.markdown("""
    <h2 style="color: #111827; font-weight: 800; font-size: 2rem;">💬 Chat with Your Contract</h2>
    """, unsafe_allow_html=True)

    # Suggested questions
    with st.expander("💡 Suggested Questions", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📌 What are the main obligations?"):
                st.session_state.chat_query = "What are the main obligations in this contract?"
            if st.button("⏰ What are the key deadlines?"):
                st.session_state.chat_query = "What are the important dates and deadlines?"
            if st.button("💰 What are the payment terms?"):
                st.session_state.chat_query = "What are the payment terms and amounts?"
        
        with col2:
            if st.button("⚠️ What are the biggest risks?"):
                st.session_state.chat_query = "What are the highest risk clauses I should worry about?"
            if st.button("🚪 How can I terminate this?"):
                st.session_state.chat_query = "What are the termination conditions and notice periods?"
            if st.button("🛡️ What liability do I have?"):
                st.session_state.chat_query = "What liability and indemnification obligations do I have?"

    # Chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    query = st.chat_input("Ask anything about your contract...")
    
    # Handle suggested question
    if "chat_query" in st.session_state:
        query = st.session_state.chat_query
        del st.session_state.chat_query

    if query:
        st.session_state.chat_history.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.write(query)

        with st.chat_message("assistant"):
            with st.spinner("🤔 Analyzing..."):
                response = chat_with_contract(contract_id, query)

                if response:
                    st.write(response["answer"])

                    if response.get("relevant_clauses"):
                        with st.expander("📚 Related Clauses"):
                            for clause in response["relevant_clauses"]:
                                risk_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(clause['risk_level'], "⚪")
                                st.markdown(f"{risk_emoji} **{clause['type'].replace('_', ' ').title()}** [{clause['risk_level']}]")
                                # Clean and format clause text
                                cleaned_clause_text = re.sub(r'\s+', ' ', clause["text"].strip())
                                st.markdown(f"""
                                <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; 
                                            margin: 0.5rem 0; border-left: 3px solid #94a3b8;">
                                    <p style="color: #1e293b; font-size: 1rem; font-weight: 600; margin: 0; 
                                             line-height: 1.7; white-space: normal; word-wrap: break-word;">
                                        {cleaned_clause_text}
                                    </p>
                                </div>
                                """, unsafe_allow_html=True)
                                st.markdown("---")

                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": response["answer"]}
                    )


def show_report_section(contract_id):
    """Display enhanced report section."""
    st.markdown("""
    <h2 style="color: #111827; font-weight: 800; font-size: 2rem;">📄 Professional Report</h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📊 What's Included:")
        
        # Use Streamlit container with native markdown for better rendering
        with st.container():
            st.markdown("""
            <div style="background: #f8fafc; padding: 2rem; border-radius: 12px; 
                        border: 2px solid #e5e7eb; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
            """, unsafe_allow_html=True)
            
            # Use native markdown for list items
            st.markdown("✅ **Executive Summary** - High-level overview")
            st.markdown("✅ **Risk Breakdown** - Detailed risk analysis with charts")
            st.markdown("✅ **Clause Analysis** - Every clause with risk assessment")
            st.markdown("✅ **Recommendations** - Actionable negotiation points")
            st.markdown("✅ **Visual Charts** - Professional data visualizations")
            
            st.markdown("---")
            st.markdown("**Perfect for sharing with:**")
            st.markdown("• Legal teams")
            st.markdown("• Business stakeholders")
            st.markdown("• External counsel")
            st.markdown("• Management")
            
            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<h3 style="color: #111827; font-weight: 800;">📥 Download</h3>', unsafe_allow_html=True)
        
        # PDF Button
        report_url = download_report(contract_id)
        st.markdown(
            f'<a href="{report_url}" target="_blank" style="text-decoration: none;">'
            f'<button style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'
            f'color:white;padding:16px 32px;border:none;border-radius:12px;'
            f'font-size:18px;font-weight:700;cursor:pointer;width:100%;margin-bottom:1rem;'
            f'box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);">'
            f'📥 Download PDF Report</button></a>',
            unsafe_allow_html=True
        )

        # Word Button
        docx_url = download_docx_report(contract_id)
        st.markdown(
            f'<a href="{docx_url}" target="_blank" style="text-decoration: none;">'
            f'<button style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);'
            f'color:white;padding:16px 32px;border:none;border-radius:12px;'
            f'font-size:18px;font-weight:700;cursor:pointer;width:100%;'
            f'box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);">'
            f'📝 Download Word Report</button></a>',
            unsafe_allow_html=True
        )


def show_deep_analysis(contract_id):
    """Show comprehensive deep analysis."""
    st.markdown("""
    <h2 style="color: #111827; font-weight: 800; font-size: 2rem;">🔍 Deep Analysis</h2>
    """, unsafe_allow_html=True)
    
    # Fetch comprehensive analysis
    with st.spinner("🔍 Running comprehensive analysis..."):
        analysis = get_comprehensive_analysis(contract_id)
    
    if not analysis:
        st.error("Failed to load comprehensive analysis")
        return
    
    # Create tabs for different analysis types
    analysis_tab1, analysis_tab2, analysis_tab3, analysis_tab4 = st.tabs([
        "📌 Key Terms",
        "👥 Parties",
        "📅 Important Dates",
        "📋 Obligations"
    ])
    
    with analysis_tab1:
        show_key_terms(analysis.get("key_terms", {}))
    
    with analysis_tab2:
        show_parties(analysis.get("parties", []))
    
    with analysis_tab3:
        show_dates(analysis.get("important_dates", []))
    
    with analysis_tab4:
        show_obligations(analysis.get("obligations", {}))


def show_comparison_interface(contract_id):
    """Show contract comparison interface."""
    st.markdown("""
    <h2 style="color: #111827; font-weight: 800; font-size: 2rem;">⚔️ Contract Comparison</h2>
    """, unsafe_allow_html=True)

    # Get all contracts
    contracts = get_all_contracts()
    
    if not contracts:
        st.warning("No other contracts found to compare with.")
        return

    # Filter out current contract
    other_contracts = [c for c in contracts if c['id'] != contract_id]
    
    if not other_contracts:
        st.info("Upload another contract to enable comparison.")
        return

    # Select contract to compare
    selected_contract_id = st.selectbox(
        "Select contract to compare with:",
        options=[c['id'] for c in other_contracts],
        format_func=lambda x: next((c['title'] for c in other_contracts if c['id'] == x), x)
    )

    if selected_contract_id:
        col1, col2 = st.columns(2)
        
        # Fetch data for both
        current_risk = get_risk_data(contract_id)
        other_risk = get_risk_data(selected_contract_id)
        
        current_contract = get_contract_details(contract_id)
        other_contract = get_contract_details(selected_contract_id)

        if current_risk and other_risk:
            with col1:
                st.markdown(f"### 📄 {current_contract['original_filename']}")
                st.metric("Risk Score", f"{current_risk['high_risk_count']} High Risks")
                st.metric("Total Clauses", current_risk['total_clauses'])
                
                # Risk distribution
                st.bar_chart({
                    "High": current_risk['high_risk_count'],
                    "Medium": current_risk['medium_risk_count'],
                    "Low": current_risk['low_risk_count']
                })

            with col2:
                st.markdown(f"### 📄 {other_contract['original_filename']}")
                st.metric("Risk Score", f"{other_risk['high_risk_count']} High Risks", 
                         delta=other_risk['high_risk_count'] - current_risk['high_risk_count'],
                         delta_color="inverse")
                st.metric("Total Clauses", other_risk['total_clauses'])
                
                # Risk distribution
                st.bar_chart({
                    "High": other_risk['high_risk_count'],
                    "Medium": other_risk['medium_risk_count'],
                    "Low": other_risk['low_risk_count']
                })
            
            st.markdown("---")
            st.markdown("### 🔍 Key Differences")
            st.info("Comparison logic would go here (e.g. missing clauses, conflicting terms).")


if __name__ == "__main__":
    main()

