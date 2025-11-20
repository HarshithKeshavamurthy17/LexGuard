"""LexGuard Streamlit UI - Modern contract analysis dashboard."""

import streamlit as st
import httpx
import pandas as pd
from datetime import datetime
import time

# Configure page
st.set_page_config(
    page_title="LexGuard – AI Legal Helper",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API base URL
API_BASE_URL = "http://localhost:8000/api"

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #2c5aa0;
    }
    .risk-high {
        color: #dc3545;
        font-weight: 600;
    }
    .risk-medium {
        color: #ffc107;
        font-weight: 600;
    }
    .risk-low {
        color: #28a745;
        font-weight: 600;
    }
    .stButton>button {
        width: 100%;
        background-color: #2c5aa0;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1e3d6f;
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


def upload_file(file):
    """Upload a contract file to the API."""
    try:
        with st.spinner("🔄 Uploading and analyzing your contract..."):
            with httpx.Client(timeout=120.0) as client:
                files = {"file": (file.name, file, "application/pdf")}
                response = client.post(f"{API_BASE_URL}/upload", files=files)
                response.raise_for_status()
                return response.json()
    except httpx.HTTPError as e:
        st.error(f"Upload failed: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
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


def chat_with_contract(contract_id, query):
    """Send a chat query to the API."""
    try:
        with httpx.Client(timeout=60.0) as client:
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


def main():
    """Main Streamlit application."""
    initialize_session_state()

    # Header
    st.markdown('<div class="main-header">⚖️ LexGuard – AI Legal Helper</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Upload contracts, analyze risks, and chat with your documents</div>',
        unsafe_allow_html=True,
    )

    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/2c5aa0/ffffff?text=LexGuard", use_container_width=True)
        st.markdown("---")

        # Upload Section
        st.header("📤 Upload Contract")
        uploaded_file = st.file_uploader(
            "Choose a PDF file", type=["pdf"], help="Upload a legal contract in PDF format"
        )

        if uploaded_file is not None:
            if st.button("🚀 Analyze Contract", type="primary"):
                result = upload_file(uploaded_file)
                if result:
                    st.session_state.contract_id = result["contract_id"]
                    st.success(f"✅ Analysis complete! Found {result['clause_count']} clauses.")
                    time.sleep(1)
                    st.rerun()

        st.markdown("---")

        # Contract selector
        if st.session_state.contract_id:
            st.success(f"📄 Contract loaded")
            if st.button("🔄 Upload New Contract"):
                st.session_state.contract_id = None
                st.session_state.contract_data = None
                st.session_state.chat_history = []
                st.rerun()

    # Main content area
    if st.session_state.contract_id:
        show_contract_analysis()
    else:
        show_welcome_screen()


def show_welcome_screen():
    """Display welcome screen when no contract is loaded."""
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📄 Upload Documents")
        st.write("Upload legal contracts in PDF format for instant analysis")

    with col2:
        st.markdown("### 🎯 Risk Analysis")
        st.write("Get AI-powered risk scoring and clause classification")

    with col3:
        st.markdown("### 💬 Interactive Chat")
        st.write("Ask questions about your contract in natural language")

    st.markdown("---")
    st.info("👈 Upload a contract using the sidebar to get started!")


def show_contract_analysis():
    """Display contract analysis dashboard."""
    contract_id = st.session_state.contract_id

    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Risk Overview", "📋 Clause Details", "💬 Chat", "📄 Report"])

    with tab1:
        show_risk_overview(contract_id)

    with tab2:
        show_clause_details(contract_id)

    with tab3:
        show_chat_interface(contract_id)

    with tab4:
        show_report_section(contract_id)


def show_risk_overview(contract_id):
    """Display risk overview tab."""
    st.header("Risk Assessment Overview")

    # Fetch data
    risk_data = get_risk_data(contract_id)
    contract_data = get_contract_details(contract_id)

    if not risk_data or not contract_data:
        st.error("Failed to load data")
        return

    # Risk metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Clauses", risk_data["total_clauses"])

    with col2:
        st.metric("🔴 High Risk", risk_data["high_risk_count"])

    with col3:
        st.metric("🟡 Medium Risk", risk_data["medium_risk_count"])

    with col4:
        st.metric("🟢 Low Risk", risk_data["low_risk_count"])

    # Risk distribution chart
    st.markdown("---")
    st.subheader("Risk Distribution")

    risk_df = pd.DataFrame(
        {
            "Risk Level": ["High", "Medium", "Low"],
            "Count": [
                risk_data["high_risk_count"],
                risk_data["medium_risk_count"],
                risk_data["low_risk_count"],
            ],
        }
    )

    st.bar_chart(risk_df.set_index("Risk Level"))

    # Contract summary
    st.markdown("---")
    st.subheader("Contract Summary")
    st.write(contract_data.get("summary", "No summary available"))


def show_clause_details(contract_id):
    """Display clause details tab."""
    st.header("Clause Analysis")

    clauses = get_clauses(contract_id)

    if not clauses:
        st.error("Failed to load clauses")
        return

    # Filter by risk level
    risk_filter = st.multiselect(
        "Filter by Risk Level",
        options=["high", "medium", "low"],
        default=["high", "medium", "low"],
    )

    # Filter clauses
    filtered_clauses = [
        c for c in clauses if c.get("risk_level") in risk_filter
    ]

    st.write(f"Showing {len(filtered_clauses)} of {len(clauses)} clauses")

    # Display clauses
    for i, clause in enumerate(filtered_clauses, 1):
        risk_level = clause.get("risk_level", "unknown")
        risk_class = f"risk-{risk_level}"

        with st.expander(
            f"Clause {i}: {clause['clause_type'].replace('_', ' ').title()} "
            f"[{risk_level.upper()}]",
            expanded=(i <= 3 and risk_level == "high"),
        ):
            st.markdown(f"**Type:** {clause['clause_type'].replace('_', ' ').title()}")
            st.markdown(f"**Risk Level:** <span class='{risk_class}'>{risk_level.upper()}</span>", unsafe_allow_html=True)
            st.markdown(f"**Risk Score:** {clause.get('risk_score', 0):.2f}")

            st.markdown("**Clause Text:**")
            st.text_area(
                "Text",
                clause["text"],
                height=150,
                key=f"clause_{i}",
                label_visibility="collapsed",
            )


def show_chat_interface(contract_id):
    """Display chat interface tab."""
    st.header("💬 Chat with Your Contract")

    st.write("Ask questions about your contract in natural language.")

    # Sample questions
    with st.expander("💡 Sample Questions"):
        st.markdown(
            """
        - What are the termination conditions?
        - How much liability am I exposed to?
        - What are the payment terms?
        - Are there any non-compete clauses?
        - What happens if I breach this contract?
        """
        )

    # Chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    query = st.chat_input("Ask a question about your contract...")

    if query:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.write(query)

        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_with_contract(contract_id, query)

                if response:
                    st.write(response["answer"])

                    # Show relevant clauses
                    if response.get("relevant_clauses"):
                        with st.expander("📚 Relevant Clauses"):
                            for clause in response["relevant_clauses"]:
                                st.markdown(f"**{clause['type'].replace('_', ' ').title()}** [{clause['risk_level']}]")
                                st.write(clause["text"])
                                st.markdown("---")

                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": response["answer"]}
                    )
                else:
                    st.error("Failed to get response")


def show_report_section(contract_id):
    """Display report download section."""
    st.header("📄 Download Risk Report")

    st.write(
        "Generate a comprehensive PDF report with risk analysis, "
        "clause breakdown, and negotiation recommendations."
    )

    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("**Report includes:**")
        st.markdown("- Executive summary")
        st.markdown("- Risk overview with charts")
        st.markdown("- Detailed clause analysis")
        st.markdown("- Negotiation recommendations")
        st.markdown("- Professional formatting")

    with col2:
        report_url = download_report(contract_id)
        st.markdown("### ")
        st.markdown(f'<a href="{report_url}" target="_blank"><button style="background:#2c5aa0;color:white;padding:12px 24px;border:none;border-radius:6px;font-size:16px;font-weight:600;cursor:pointer;width:100%">📥 Download PDF Report</button></a>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()


