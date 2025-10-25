"""
Custom CSS styles for Streamlit dashboard.
"""
import streamlit as st


def inject_custom_css():
    """Inject custom CSS to improve dashboard styling."""
    
    custom_css = """
    <style>
    /* Main container */
    .main {
        padding: 2rem;
    }
    
    /* Metric cards styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #666;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    [data-testid="stSidebar"] .element-container {
        padding: 0.5rem 0;
    }
    
    /* Headers */
    h1 {
        color: #1f77b4;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e0e0e0;
    }
    
    h2 {
        color: #333;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #666;
        margin-top: 1.5rem;
    }
    
    /* Cards/containers */
    .stContainer {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: background-color 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #155a8a;
    }
    
    /* Selectbox */
    .stSelectbox {
        border-radius: 4px;
    }
    
    /* Dataframe tables */
    .dataframe {
        border: none !important;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .dataframe thead tr th {
        background-color: #1f77b4 !important;
        color: white !important;
        padding: 12px !important;
        text-align: left !important;
        font-weight: 600 !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: #f5f5f5 !important;
    }
    
    .dataframe tbody tr td {
        padding: 10px !important;
    }
    
    /* Charts container */
    .js-plotly-plot {
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Success/Error/Warning boxes */
    .stAlert {
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 4px;
        font-weight: 500;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        background-color: #f8f9fa;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid #e0e0e0;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #1f77b4 !important;
    }
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)


def create_sidebar_header(title: str, subtitle: str = ""):
    """
    Create a styled sidebar header.
    
    Args:
        title: Main title
        subtitle: Subtitle (optional)
    """
    st.sidebar.markdown(
        f"""
        <div style="
            padding: 1rem 0;
            text-align: center;
            border-bottom: 2px solid #e0e0e0;
            margin-bottom: 2rem;
        ">
            <h1 style="
                color: #1f77b4;
                font-size: 1.8rem;
                margin-bottom: 0.5rem;
                border: none;
                padding: 0;
            ">{title}</h1>
            {f'<p style="color: #666; font-size: 0.9rem; margin: 0;">{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True
    )


def create_page_header(icon: str, title: str, description: str = ""):
    """
    Create a styled page header.
    
    Args:
        icon: Emoji icon
        title: Page title
        description: Page description (optional)
    """
    st.markdown(
        f"""
        <div style="margin-bottom: 2rem;">
            <h1 style="
                color: #1f77b4;
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
                border: none;
                padding: 0;
            ">{icon} {title}</h1>
            {f'<p style="color: #666; font-size: 1.1rem; margin: 0;">{description}</p>' if description else ''}
        </div>
        """,
        unsafe_allow_html=True
    )


def create_metric_row(metrics: list):
    """
    Create a row of metrics with equal column widths.
    
    Args:
        metrics: List of tuples (label, value, delta, delta_color)
    """
    from .metrics import display_metric_card
    
    cols = st.columns(len(metrics))
    for col, (label, value, delta, delta_color) in zip(cols, metrics):
        with col:
            display_metric_card(label, value, delta, delta_color)

