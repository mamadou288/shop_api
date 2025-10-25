"""
Overview Dashboard - Vue d'ensemble des KPIs principaux
"""
import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.auth import init_session_state, require_authentication, get_current_token, get_current_user_email, logout
from utils.api_client import fetch_dashboard_kpis, clear_cache
from utils.charts import (
    create_revenue_line_chart,
    create_orders_pie_chart,
    create_top_products_bar_chart
)
from utils.metrics import (
    format_currency,
    format_percentage,
    format_number,
    get_growth_indicator
)
from utils.styles import inject_custom_css, create_page_header

# Page config
st.set_page_config(
    page_title="Overview - Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Initialize and check authentication
init_session_state()
require_authentication()

# Inject custom CSS
inject_custom_css()

# Page header
create_page_header(
    icon="📊",
    title="Overview Dashboard",
    description="Vue d'ensemble des indicateurs clés de performance"
)

# Sidebar
st.sidebar.title("⚙️ Configuration")

# User info
st.sidebar.success(f"👤 **{get_current_user_email()}**")
if st.sidebar.button("🚪 Déconnexion"):
    logout()
    st.rerun()

st.sidebar.markdown("---")

# Period selector
period = st.sidebar.selectbox(
    "Période",
    options=['7d', '30d', '90d', '1y'],
    index=2,  # Default: 90d
    help="Période pour l'analyse des données"
)

period_labels = {
    '7d': '7 derniers jours',
    '30d': '30 derniers jours',
    '90d': '90 derniers jours',
    '1y': '1 an'
}

# Refresh button
if st.sidebar.button("🔄 Actualiser les données"):
    clear_cache()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(f"**Période active :** {period_labels[period]}")

# Fetch data
with st.spinner('Chargement des données...'):
    # Get token from session
    token = get_current_token()
    
    # Fetch dashboard data
    data = fetch_dashboard_kpis(token, period=period)
    
    if not data:
        st.error("❌ Impossible de récupérer les données. Vérifiez l'API.")
        st.stop()

# Extract data
business = data.get('business', {})
products = data.get('products', {})
users = data.get('users', {})

# Metrics row
st.markdown("### 📈 Indicateurs clés")

col1, col2, col3, col4 = st.columns(4)

with col1:
    revenue = business.get('revenue', {})
    total_revenue = revenue.get('total', 0)
    revenue_growth = revenue.get('growth', 0)
    
    st.metric(
        label="💰 Revenue Total",
        value=format_currency(total_revenue),
        delta=format_percentage(revenue_growth),
        delta_color="normal"
    )

with col2:
    orders = business.get('orders', {})
    total_orders = orders.get('total', 0)
    orders_growth = orders.get('growth', 0)
    
    st.metric(
        label="🛒 Commandes",
        value=format_number(total_orders),
        delta=format_percentage(orders_growth),
        delta_color="normal"
    )

with col3:
    aov = business.get('aov', {})
    aov_value = aov.get('value', 0)
    
    st.metric(
        label="💳 Panier Moyen (AOV)",
        value=format_currency(aov_value),
        delta=None
    )

with col4:
    clv = business.get('clv', {})
    clv_value = clv.get('value', 0)
    
    st.metric(
        label="🎯 Valeur Client (CLV)",
        value=format_currency(clv_value),
        delta=None
    )

st.markdown("---")

# Revenue trend chart
st.markdown("### 📈 Évolution du Revenue")

revenue_chart_data = business.get('charts', {}).get('revenue_by_month', [])

if revenue_chart_data:
    fig_revenue = create_revenue_line_chart(revenue_chart_data)
    st.plotly_chart(fig_revenue, use_container_width=True)
else:
    st.info("Pas de données de revenue disponibles")

st.markdown("---")

# Two columns for pie and bar charts
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🥧 Commandes par Statut")
    
    orders_status_chart = orders.get('status_chart', [])
    
    if orders_status_chart:
        fig_orders = create_orders_pie_chart(orders_status_chart)
        st.plotly_chart(fig_orders, use_container_width=True)
    else:
        st.info("Pas de données de commandes disponibles")

with col_right:
    st.markdown("### 🏆 Top 5 Produits")
    
    top_products = products.get('top_products', {}).get('by_revenue', [])[:5]
    
    if top_products:
        fig_products = create_top_products_bar_chart(top_products, by='revenue')
        st.plotly_chart(fig_products, use_container_width=True)
    else:
        st.info("Pas de données de produits disponibles")

st.markdown("---")

# Quick stats
st.markdown("### 📊 Statistiques Rapides")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_users = users.get('total_users', 0)
    st.metric(
        label="👥 Total Utilisateurs",
        value=format_number(total_users)
    )

with col2:
    active_users = users.get('active_users', 0)
    activation_rate = (active_users / total_users * 100) if total_users > 0 else 0
    st.metric(
        label="✅ Utilisateurs Actifs",
        value=format_number(active_users),
        delta=f"{activation_rate:.1f}%"
    )

with col3:
    low_stock = products.get('stock_alerts', {}).get('low_stock', [])
    low_stock_count = len(low_stock)
    st.metric(
        label="⚠️ Stock Faible",
        value=format_number(low_stock_count)
    )

with col4:
    repeat_rate = business.get('repeat_purchase_rate', {}).get('percentage', 0)
    st.metric(
        label="🔄 Taux de Rachat",
        value=f"{repeat_rate:.1f}%"
    )

# Footer
st.markdown("---")
st.caption(f"Dernière mise à jour : {data.get('generated_at', 'N/A')}")

