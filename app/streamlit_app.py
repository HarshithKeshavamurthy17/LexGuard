"""LexGuard Enhanced UI - Beautiful, Modern, Comprehensive Contract Analysis."""

import os
import sys
import subprocess
import time
import socket
import re
from datetime import datetime

# Add the root directory to sys.path to allow imports from 'app' and 'lexguard'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import httpx
import plotly.graph_objects as go
import streamlit as st


def _apply_secret_to_env(key: str, value):
    """Set environment variable from a secret value."""
    if key:
        os.environ[key.upper()] = str(value)


def _walk_secrets(prefix: str, payload):
    from collections.abc import Mapping  # local import to avoid global dependency

    if isinstance(payload, Mapping):
        for sub_key, sub_val in payload.items():
            next_prefix = f"{prefix}_{sub_key}" if prefix else sub_key
            _walk_secrets(next_prefix, sub_val)
    else:
        _apply_secret_to_env(prefix, payload)


def sync_streamlit_secrets_to_env():
    """Mirror Streamlit secrets into os.environ so the backend process inherits them."""
    try:
        secrets_obj = st.secrets
    except Exception:
        return

    from collections.abc import Mapping

    if isinstance(secrets_obj, Mapping):
        for top_key, top_value in secrets_obj.items():
            _walk_secrets(top_key, top_value)


sync_streamlit_secrets_to_env()

from analysis_displays import show_key_terms, show_parties, show_dates, show_obligations


# Backend configuration (override via environment variables when deploying)
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", f"http://{BACKEND_HOST}:{BACKEND_PORT}")
API_BASE_URL = os.getenv("API_BASE_URL", f"{BACKEND_BASE_URL}/api")
HEALTH_ENDPOINT = os.getenv("BACKEND_HEALTH_ENDPOINT", f"{BACKEND_BASE_URL}/health")


def is_port_in_use(port: int) -> bool:
    """Check whether a local port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(("127.0.0.1", port)) == 0


def start_backend_process():
    """Ensure the FastAPI backend is running for Streamlit Cloud."""
    if is_port_in_use(BACKEND_PORT):
        print("✅ Backend already running.")
        return

    print(f"🚀 Starting FastAPI backend on port {BACKEND_PORT}...")
    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(BACKEND_PORT),
        ],
        cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
        stdout=sys.stdout,
        stderr=sys.stderr,
    )


def wait_for_backend_ready(timeout_seconds: int = 120) -> bool:
    """Poll the backend health endpoint until it becomes available."""
    print("⏳ Waiting for backend health check...")
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        try:
            response = httpx.get(HEALTH_ENDPOINT, timeout=2.0)
            if response.status_code == 200:
                print("✅ Backend health check passed.")
                return True
        except Exception:
            pass
        time.sleep(1)

    print("❌ Backend failed to become healthy within the timeout window.")
    return False


@st.cache_resource(show_spinner="🚀 Warming up LexGuard API backend...")
def ensure_backend_ready() -> bool:
    """Start the backend (if needed) and wait for it to be reachable."""
    start_backend_process()
    if not wait_for_backend_ready():
        raise RuntimeError("Backend failed to start within the expected time.")
    return True

# Configure page with custom theme
st.set_page_config(
    page_title="LexGuard – AI Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ensure backend is ready before rendering the UI
try:
    ensure_backend_ready()
except RuntimeError:
    st.error(
        "❌ The AI backend did not start in time. Please try re-running the app or "
        "check the deployment logs for details."
    )
    st.stop()

# Enhanced Custom CSS with modern design and theme compatibility
st.markdown(
    """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container - gradient background */
    .main {
        background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
        background-attachment: fixed;
    }
    
    /* Content area - WHITE background with dark text */
    .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
        background: #ffffff !important;
        border-radius: 20px;
        margin: 2rem auto;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    }
    
    /* Force all text to be DARK on white background */
    .block-container * {
        color: #1f2937 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #111827 !important;
    }

    /* Headers */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: center;
        animation: fadeIn 1s ease-in;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #374151 !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }

    /* Custom card for deep analysis - WHITE background */
    .custom-card {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%) !important;
        padding: 1.8rem;
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
        color: #111827 !important;
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: #4b5563 !important;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Risk levels with solid bright colors */
    .risk-high {
        color: #dc2626 !important;
        font-weight: 800;
        text-shadow: 0 2px 4px rgba(220, 38, 38, 0.2);
    }
    
    .risk-medium {
        color: #f59e0b !important;
        font-weight: 800;
        text-shadow: 0 2px 4px rgba(245, 158, 11, 0.2);
    }
    
    .risk-low {
        color: #059669 !important;
        font-weight: 800;
        text-shadow: 0 2px 4px rgba(5, 150, 105, 0.2);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
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
        background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%) !important;
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
    /* FORCE LIGHT THEME VARIABLES */
    :root {
        --primary-color: #4f46e5;
        --background-color: #ffffff;
        --secondary-background-color: #f8fafc;
        --text-color: #1f2937;
        --font: "Inter", sans-serif;
    }

    /* GLOBAL TEXT RESET - Main Content Only */
    .main .block-container {
        color: #1f2937 !important;
    }
    
    /* SIDEBAR SPECIFIC - FORCE WHITE TEXT */
    [data-testid="stSidebar"] {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] div, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] li,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    /* INPUTS & TEXTAREAS - FORCE WHITE BACKGROUND & DARK TEXT */
    input, textarea, .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        caret-color: #000000 !important;
        border: 1px solid #d1d5db !important;
    }
    
    input::placeholder, textarea::placeholder {
        color: #6b7280 !important;
        opacity: 1 !important;
    }

    /* CHAT INPUT SPECIFIC */
    .stChatInputContainer {
        background-color: #f8fafc !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }
    
    .stChatInputContainer textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #e5e7eb !important;
    }

    /* DROPDOWNS & SELECTBOXES - THE HARDEST PART */
    /* The main box you click */
    .stSelectbox > div > div, .stMultiSelect > div > div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-color: #d1d5db !important;
    }
    
    /* The text inside the main box */
    .stSelectbox div[data-baseweb="select"] span,
    .stMultiSelect div[data-baseweb="select"] span {
        color: #000000 !important;
    }

    /* The dropdown menu list container */
    div[data-baseweb="popover"], 
    div[data-baseweb="menu"],
    ul[data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
    }

    /* The items in the dropdown list */
    li[data-baseweb="menu-item"], 
    div[data-baseweb="menu"] li {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Hover state for dropdown items */
    li[data-baseweb="menu-item"]:hover,
    div[data-baseweb="menu"] li:hover,
    li[aria-selected="true"] {
        background-color: #f3f4f6 !important;
        color: #000000 !important;
    }

    /* MultiSelect Tags (Chips) */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #e0e7ff !important;
        color: #3730a3 !important;
        border: 1px solid #c7d2fe !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] span {
        color: #3730a3 !important;
    }
    
    /* Close button on tags */
    .stMultiSelect [data-baseweb="tag"] svg {
        fill: #3730a3 !important;
        color: #3730a3 !important;
    }

    /* LABELS */
    label, .stSelectbox label, .stMultiSelect label, .stTextInput label {
        color: #111827 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }

    /* FILE UPLOADER */
    .stFileUploader {
        background-color: #f8fafc !important;
        border: 2px dashed #cbd5e1 !important;
        padding: 1rem !important;
        border-radius: 12px !important;
    }
    
    .stFileUploader section {
        background-color: #ffffff !important;
    }
    
    .stFileUploader span, .stFileUploader small {
        color: #4b5563 !important;
    }

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
    progress_bar = None
    status_text = None
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
    except httpx.HTTPStatusError as exc:
        server_message = exc.response.text.strip() if exc.response else "No details provided."
        st.error(
            f"❌ Upload failed ({exc.response.status_code}): {server_message}"
        )
        return None
    except httpx.RequestError as exc:
        st.error(f"❌ Upload failed: Could not reach backend ({exc}).")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        return None
    finally:
        if progress_bar is not None:
            progress_bar.empty()
        if status_text is not None:
            status_text.empty()


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
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", 
        "📋 Clauses", 
        "💬 AI Chat", 
        "📄 Report",
        "🔍 Deep Analysis"
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
    """Display comprehensive contract analysis report."""
    
    # Header
    st.markdown("""
    <h2 style="color: #111827; font-weight: 800; font-size: 2rem; margin-bottom: 0.5rem;">📄 Comprehensive Contract Report</h2>
    <p style="color: #6b7280; font-size: 1.1rem; margin-bottom: 2rem;">
        A complete analysis of your contract with risk assessments, insights, and actionable recommendations.
    </p>
    """, unsafe_allow_html=True)
    
    # Fetch all necessary data
    with st.spinner("📊 Generating comprehensive report..."):
        contract_data = get_contract_details(contract_id)
        risk_data = get_risk_data(contract_id)
        clauses = get_clauses(contract_id)
        analysis = get_comprehensive_analysis(contract_id)
    
    if not contract_data or not risk_data:
        st.error("❌ Failed to load contract data. Please try again.")
        return
    
    # Executive Summary
    st.markdown("""
    <div style="background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem; border-left: 6px solid #4f46e5;">
        <h3 style="color: #111827; font-weight: 800; margin: 0 0 1rem 0;">📋 Executive Summary</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Contract Overview
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 2px solid #e5e7eb; margin-bottom: 1rem;">
            <h4 style="color: #4f46e5; font-weight: 700; margin: 0 0 0.5rem 0;">Contract Information</h4>
            <p style="color: #1f2937; margin: 0.5rem 0;"><strong>Title:</strong> {contract_data.get('title', 'N/A')}</p>
            <p style="color: #1f2937; margin: 0.5rem 0;"><strong>Total Clauses:</strong> {risk_data.get('total_clauses', 0)}</p>
            <p style="color: #1f2937; margin: 0.5rem 0;"><strong>Analysis Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 2px solid #e5e7eb; margin-bottom: 1rem;">
            <h4 style="color: #dc2626; font-weight: 700; margin: 0 0 0.5rem 0;">Risk Overview</h4>
            <p style="color: #dc2626; margin: 0.5rem 0; font-size: 1.1rem;"><strong>🔴 High Risk:</strong> {risk_data.get('high_risk_count', 0)} clauses</p>
            <p style="color: #f59e0b; margin: 0.5rem 0; font-size: 1.1rem;"><strong>🟡 Medium Risk:</strong> {risk_data.get('medium_risk_count', 0)} clauses</p>
            <p style="color: #059669; margin: 0.5rem 0; font-size: 1.1rem;"><strong>🟢 Low Risk:</strong> {risk_data.get('low_risk_count', 0)} clauses</p>
        </div>
        """, unsafe_allow_html=True)
    
    # AI-Generated Summary
    if contract_data.get('summary'):
        st.markdown("""
        <div style="background: #f8fafc; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #3b82f6; margin-bottom: 2rem;">
            <h4 style="color: #111827; font-weight: 700; margin: 0 0 1rem 0;">🤖 AI Summary</h4>
        """, unsafe_allow_html=True)
        st.markdown(f"<p style='color: #1f2937; line-height: 1.8;'>{contract_data.get('summary')}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Risk Analysis Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem; border-left: 6px solid #dc2626;">
        <h3 style="color: #111827; font-weight: 800; margin: 0 0 0.5rem 0;">⚠️ Detailed Risk Analysis</h3>
        <p style="color: #4b5563; margin: 0; font-size: 0.95rem;">
            Understanding the risks in your contract and why they matter
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # High Risk Clauses - Detailed Analysis
    if clauses:
        high_risk_clauses = [c for c in clauses if c.get('risk_level') == 'high']
        medium_risk_clauses = [c for c in clauses if c.get('risk_level') == 'medium']
        
        if high_risk_clauses:
            st.markdown("""
            <div style="background: #fef2f2; padding: 1.5rem; border-radius: 12px; border: 2px solid #fca5a5; margin-bottom: 1.5rem;">
                <h4 style="color: #dc2626; font-weight: 700; margin: 0 0 1rem 0;">🔴 High Risk Areas - Immediate Attention Required</h4>
                <p style="color: #4b5563; margin-bottom: 1rem;">These clauses pose significant risks and should be carefully reviewed or renegotiated:</p>
            </div>
            """, unsafe_allow_html=True)
            
            for i, clause in enumerate(high_risk_clauses, 1):
                with st.expander(f"⚠️ High Risk Clause {i}: {clause['clause_type'].replace('_', ' ').title()}", expanded=(i <= 2)):
                    st.markdown(f"""
                    <div style="background: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
                        <h5 style="color: #dc2626; font-weight: 700;">Why This is High Risk:</h5>
                        <p style="color: #1f2937; line-height: 1.8;">
                            This <strong>{clause['clause_type'].replace('_', ' ')}</strong> clause has been flagged as high risk 
                            (score: {clause.get('risk_score', 0):.2f}/10) because it may expose you to significant liability, 
                            unfavorable terms, or potential legal complications.
                        </p>
                        
                        <h5 style="color: #111827; font-weight: 700; margin-top: 1rem;">Clause Text:</h5>
                        <div style="background: #f9fafb; padding: 1rem; border-radius: 6px; border-left: 3px solid #dc2626;">
                            <p style="color: #374151; font-style: italic; line-height: 1.6;">{clause['text'][:500]}{'...' if len(clause['text']) > 500 else ''}</p>
                        </div>
                        
                        <h5 style="color: #111827; font-weight: 700; margin-top: 1rem;">💡 What You Should Do:</h5>
                        <ul style="color: #1f2937; line-height: 1.8;">
                            <li>Review this clause with your legal team immediately</li>
                            <li>Consider negotiating more favorable terms</li>
                            <li>Understand the full implications before signing</li>
                            <li>Ask for clarifications or modifications if needed</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
        
        if medium_risk_clauses:
            st.markdown("""
            <div style="background: #fffbeb; padding: 1.5rem; border-radius: 12px; border: 2px solid #fcd34d; margin-bottom: 1.5rem; margin-top: 2rem;">
                <h4 style="color: #f59e0b; font-weight: 700; margin: 0 0 1rem 0;">🟡 Medium Risk Areas - Review Recommended</h4>
                <p style="color: #4b5563; margin-bottom: 0;">These clauses have moderate risk levels and should be reviewed carefully:</p>
            </div>
            """, unsafe_allow_html=True)
            
            for i, clause in enumerate(medium_risk_clauses[:3], 1):  # Show top 3
                with st.expander(f"⚡ Medium Risk Clause {i}: {clause['clause_type'].replace('_', ' ').title()}"):
                    st.markdown(f"""
                    <div style="background: white; padding: 1.5rem; border-radius: 8px;">
                        <p style="color: #1f2937; line-height: 1.8; margin-bottom: 1rem;">
                            <strong>Risk Score:</strong> {clause.get('risk_score', 0):.2f}/10
                        </p>
                        <div style="background: #fffbeb; padding: 1rem; border-radius: 6px; border-left: 3px solid #f59e0b;">
                            <p style="color: #374151; font-style: italic; line-height: 1.6;">{clause['text'][:300]}{'...' if len(clause['text']) > 300 else ''}</p>
                        </div>
                        <p style="color: #6b7280; margin-top: 1rem; font-size: 0.9rem;">
                            💡 While not critical, this clause should be reviewed to ensure it aligns with your interests.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Insights Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem; border-left: 6px solid #3b82f6;">
        <h3 style="color: #111827; font-weight: 800; margin: 0 0 0.5rem 0;">💡 Key Insights & Recommendations</h3>
        <p style="color: #4b5563; margin: 0; font-size: 0.95rem;">
            Important things to keep in mind about this contract
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate insights based on risk distribution
    total_clauses = risk_data.get('total_clauses', 0)
    high_risk_pct = (risk_data.get('high_risk_count', 0) / total_clauses * 100) if total_clauses > 0 else 0
    
    insights = []
    
    if high_risk_pct > 30:
        insights.append({
            "icon": "🚨",
            "title": "High Risk Concentration",
            "text": f"This contract has {risk_data.get('high_risk_count', 0)} high-risk clauses ({high_risk_pct:.1f}% of total). This is above average and requires careful legal review before signing.",
            "color": "#dc2626"
        })
    elif high_risk_pct > 10:
        insights.append({
            "icon": "⚠️",
            "title": "Moderate Risk Level",
            "text": f"With {high_risk_pct:.1f}% high-risk clauses, this contract has moderate risk. Review the flagged sections carefully.",
            "color": "#f59e0b"
        })
    else:
        insights.append({
            "icon": "✅",
            "title": "Relatively Low Risk",
            "text": f"Only {high_risk_pct:.1f}% of clauses are high-risk, which is relatively low. However, still review all terms carefully.",
            "color": "#059669"
        })
    
    # Add more insights
    insights.extend([
        {
            "icon": "📝",
            "title": "Negotiation Opportunities",
            "text": "High-risk clauses are often negotiable. Don't hesitate to propose modifications or request clarifications from the other party.",
            "color": "#3b82f6"
        },
        {
            "icon": "👥",
            "title": "Get Expert Review",
            "text": "For contracts with significant obligations or high-risk clauses, always consult with a qualified attorney before signing.",
            "color": "#8b5cf6"
        },
        {
            "icon": "🔍",
            "title": "Read Everything",
            "text": "Even low-risk clauses can have important implications. Make sure you understand every section before agreeing to the terms.",
            "color": "#06b6d4"
        }
    ])
    
    for insight in insights:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid {insight['color']}; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <h4 style="color: {insight['color']}; font-weight: 700; margin: 0 0 0.5rem 0;">{insight['icon']} {insight['title']}</h4>
            <p style="color: #1f2937; line-height: 1.7; margin: 0;">{insight['text']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Action Items
    st.markdown("""
    <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); padding: 2rem; border-radius: 16px; margin-bottom: 2rem; border-left: 6px solid #10b981;">
        <h3 style="color: #111827; font-weight: 800; margin: 0 0 1rem 0;">✅ Recommended Next Steps</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 12px; border: 2px solid #e5e7eb;">
        <ol style="color: #1f2937; line-height: 2; font-size: 1.05rem;">
            <li><strong>Review all high-risk clauses</strong> identified in this report with your legal team</li>
            <li><strong>Use the AI Chat tab</strong> to ask specific questions about any clause or term</li>
            <li><strong>Check the Deep Analysis tab</strong> for detailed breakdowns of parties, dates, and obligations</li>
            <li><strong>Prepare negotiation points</strong> for clauses that don't align with your interests</li>
            <li><strong>Consult with an attorney</strong> before signing, especially for high-value or complex agreements</li>
            <li><strong>Keep this analysis</strong> for your records and future reference</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.info("💬 **Have questions?** Use the AI Chat tab to ask anything about this contract!")



def show_deep_analysis(contract_id):
    """Show comprehensive deep analysis with clear explanations."""
    
    # Header with explanation
    st.markdown("""
    <h2 style="color: #111827; font-weight: 800; font-size: 2rem; margin-bottom: 0.5rem;">🔍 Deep Contract Analysis</h2>
    <p style="color: #6b7280; font-size: 1.1rem; margin-bottom: 2rem;">
        Our AI performs a comprehensive analysis of your contract, extracting key information, identifying parties, tracking important dates, and analyzing obligations. This helps you understand the contract's structure and critical elements at a glance.
    </p>
    """, unsafe_allow_html=True)
    
    # Fetch comprehensive analysis
    with st.spinner("🔍 Analyzing contract structure and extracting key information..."):
        analysis = get_comprehensive_analysis(contract_id)
    
    if not analysis:
        st.error("❌ Failed to load comprehensive analysis. Please try again or contact support.")
        return
    
    st.success("✅ Analysis complete! Explore the sections below to understand your contract better.")
    
    st.markdown("---")
    
    # Section 1: Key Terms
    st.markdown("""
    <div style="background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border-left: 4px solid #4f46e5;">
        <h3 style="color: #111827; font-weight: 700; margin: 0 0 0.5rem 0;">📌 Key Terms & Entities</h3>
        <p style="color: #4b5563; margin: 0; font-size: 0.95rem;">
            Important terms, monetary values, and entities mentioned in your contract. These are the critical elements that define the agreement.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    show_key_terms(analysis.get("key_terms", {}))
    
    st.markdown("---")
    
    # Section 2: Parties
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border-left: 4px solid #f59e0b;">
        <h3 style="color: #111827; font-weight: 700; margin: 0 0 0.5rem 0;">👥 Contract Parties</h3>
        <p style="color: #4b5563; margin: 0; font-size: 0.95rem;">
            All parties involved in this agreement, including their roles and responsibilities.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    show_parties(analysis.get("parties", []))
    
    st.markdown("---")
    
    # Section 3: Important Dates
    st.markdown("""
    <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border-left: 4px solid #3b82f6;">
        <h3 style="color: #111827; font-weight: 700; margin: 0 0 0.5rem 0;">📅 Critical Dates & Deadlines</h3>
        <p style="color: #4b5563; margin: 0; font-size: 0.95rem;">
            Important dates, deadlines, and time-sensitive obligations you need to track.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    show_dates(analysis.get("important_dates", []))
    
    st.markdown("---")
    
    # Section 4: Obligations
    st.markdown("""
    <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border-left: 4px solid #10b981;">
        <h3 style="color: #111827; font-weight: 700; margin: 0 0 0.5rem 0;">📋 Obligations & Responsibilities</h3>
        <p style="color: #4b5563; margin: 0; font-size: 0.95rem;">
            What you must do, what you cannot do, and what rights you have under this contract.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    show_obligations(analysis.get("obligations", {}))
    
    # Summary footer
    st.markdown("---")
    st.info("💡 **Tip**: Use the AI Chat tab to ask specific questions about any of these elements!")



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
