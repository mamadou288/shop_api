"""
Products & Inventory Analytics
"""
import streamlit as st
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.auth import init_session_state, require_authentication, get_current_token, get_current_user_email, logout
from utils.api_client import fetch_product_kpis, clear_cache
from utils.charts import create_top_products_bar_chart, create_category_distribution_pie
from utils.metrics import format_currency, format_number
from utils.styles import inject_custom_css, create_page_header

st.set_page_config(
    page_title="Products - Analytics Dashboard",
    page_icon="📦",
    layout="wide"
)

init_session_state()
require_authentication()

inject_custom_css()

create_page_header(
    icon="📦",
    title="Products & Inventory",
    description="Analyse des produits, stock et catégories"
)

# Sidebar
st.sidebar.title("⚙️ Configuration")

st.sidebar.success(f"👤 **{get_current_user_email()}**")
if st.sidebar.button("🚪 Déconnexion"):
    logout()
    st.rerun()

st.sidebar.markdown("---")

if st.sidebar.button("🔄 Actualiser"):
    clear_cache()
    st.rerun()

# Fetch data
with st.spinner('Chargement des données produits...'):
    token = get_current_token()
    
    data = fetch_product_kpis(token)
    
    if not data:
        st.error("❌ Impossible de récupérer les données")
        st.stop()

# Inventory metrics
st.markdown("### 📊 Vue d'ensemble Inventory")

col1, col2, col3, col4 = st.columns(4)

with col1:
    # Total products (approximate from categories)
    total_products = sum(cat['product_count'] for cat in data.get('categories', {}).get('distribution', []))
    st.metric(
        label="📦 Total Produits",
        value=format_number(total_products)
    )

with col2:
    inventory = data.get('inventory', {})
    st.metric(
        label="💰 Valeur Inventory",
        value=format_currency(inventory.get('total_value', 0))
    )

with col3:
    low_stock = data.get('stock_alerts', {}).get('low_stock', [])
    st.metric(
        label="⚠️ Stock Faible",
        value=format_number(len(low_stock))
    )

with col4:
    out_of_stock_count = data.get('stock_alerts', {}).get('out_of_stock_count', 0)
    st.metric(
        label="❌ Rupture Stock",
        value=format_number(out_of_stock_count)
    )

st.markdown("---")

# Top products by revenue
st.markdown("### 🏆 Top 10 Produits par Revenue")

top_revenue = data.get('top_products', {}).get('by_revenue', [])

if top_revenue:
    fig = create_top_products_bar_chart(top_revenue, by='revenue')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Pas de données disponibles")

st.markdown("---")

# Two columns
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📊 Top 10 Produits par Quantité")
    
    top_quantity = data.get('top_products', {}).get('by_quantity', [])
    
    if top_quantity:
        fig = create_top_products_bar_chart(top_quantity, by='quantity')
        st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown("### 🥧 Ventes par Catégorie")
    
    top_categories = data.get('categories', {}).get('top_by_revenue', [])
    
    if top_categories:
        fig = create_category_distribution_pie(top_categories)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Low stock alerts
st.markdown("### ⚠️ Alertes Stock Faible")

if low_stock:
    # Convert to DataFrame
    df_low_stock = pd.DataFrame(low_stock)
    
    # Format columns
    df_display = df_low_stock[['name', 'stock', 'price']].copy()
    df_display['price'] = df_display['price'].apply(lambda x: format_currency(x))
    df_display.columns = ['Produit', 'Stock', 'Prix']
    
    # Color code
    def color_stock(val):
        if isinstance(val, int):
            if val <= 2:
                return 'background-color: #ffebee'  # Red
            elif val <= 5:
                return 'background-color: #fff3e0'  # Orange
            else:
                return 'background-color: #fff9c4'  # Yellow
        return ''
    
    styled_df = df_display.style.applymap(color_stock, subset=['Stock'])
    
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    st.warning(f"⚠️ {len(low_stock)} produits avec stock < 10. Action recommandée : Réapprovisionner")
else:
    st.success("✅ Aucun produit en stock faible !")

st.markdown("---")

# Categories performance
st.markdown("### 📁 Performance par Catégorie")

if top_categories:
    df_categories = pd.DataFrame(top_categories)
    
    df_display = df_categories[['name', 'revenue', 'units_sold', 'products_count']].copy()
    df_display['revenue'] = df_display['revenue'].apply(lambda x: format_currency(x))
    df_display.columns = ['Catégorie', 'Revenue', 'Unités vendues', 'Nb produits']
    
    st.dataframe(df_display, use_container_width=True)

st.caption(f"Dernière mise à jour : {data.get('generated_at', 'N/A')}")

