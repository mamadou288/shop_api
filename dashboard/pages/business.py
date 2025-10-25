"""
Business Analytics - Revenue, Orders, Growth KPIs
"""
import streamlit as st
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.auth import init_session_state, require_authentication, get_current_token, get_current_user_email, logout
from utils.api_client import fetch_business_kpis, clear_cache
from utils.charts import create_revenue_line_chart, create_orders_pie_chart
from utils.metrics import (
    format_currency,
    format_percentage,
    format_number,
    interpret_kpi,
    get_growth_indicator
)
from utils.styles import inject_custom_css, create_page_header

# Page config
st.set_page_config(
    page_title="Business - Analytics Dashboard",
    page_icon="💰",
    layout="wide"
)

init_session_state()
require_authentication()

inject_custom_css()

create_page_header(
    icon="💰",
    title="Business & Revenue Analytics",
    description="Analyse approfondie du chiffre d'affaires et de la croissance"
)

# Sidebar
st.sidebar.title("⚙️ Configuration")

st.sidebar.success(f"👤 **{get_current_user_email()}**")
if st.sidebar.button("🚪 Déconnexion"):
    logout()
    st.rerun()

st.sidebar.markdown("---")

# Period selector
period = st.sidebar.selectbox(
    "Période",
    options=['7d', '30d', '90d', '1y'],
    index=2
)

# Date range (advanced)
with st.sidebar.expander("📅 Plage de dates personnalisée"):
    use_custom_dates = st.checkbox("Utiliser des dates personnalisées")
    
    if use_custom_dates:
        end_date = st.date_input("Date de fin", value=datetime.now())
        start_date = st.date_input("Date de début", value=datetime.now() - timedelta(days=90))
        
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
    else:
        start_date_str = None
        end_date_str = None

if st.sidebar.button("🔄 Actualiser"):
    clear_cache()
    st.rerun()

# Fetch data
with st.spinner('Chargement des données business...'):
    token = get_current_token()
    
    data = fetch_business_kpis(token, start_date_str, end_date_str, period)
    
    if not data:
        st.error("❌ Impossible de récupérer les données")
        st.stop()

# Main KPIs
st.markdown("### 📊 Indicateurs Business Clés")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    revenue = data.get('revenue', {})
    st.metric(
        label="💰 Revenue Total",
        value=format_currency(revenue.get('total', 0)),
        delta=format_percentage(revenue.get('growth', 0))
    )

with col2:
    growth = revenue.get('growth', 0)
    emoji, msg = interpret_kpi('growth', growth)
    st.metric(
        label="📈 Croissance MoM",
        value=f"{growth:+.1f}%",
        delta=msg,
        delta_color="off"
    )
    st.caption(f"{emoji} {msg}")

with col3:
    aov = data.get('aov', {})
    st.metric(
        label="💳 AOV",
        value=format_currency(aov.get('value', 0))
    )

with col4:
    clv = data.get('clv', {})
    st.metric(
        label="🎯 CLV",
        value=format_currency(clv.get('value', 0))
    )

with col5:
    repeat_rate = data.get('repeat_purchase_rate', {}).get('percentage', 0)
    emoji, msg = interpret_kpi('repeat_rate', repeat_rate)
    st.metric(
        label="🔄 Repeat Rate",
        value=f"{repeat_rate:.1f}%"
    )
    st.caption(f"{emoji} {msg}")

st.markdown("---")

# Revenue trend
st.markdown("### 📈 Évolution du Revenue")

revenue_data = data.get('charts', {}).get('revenue_by_month', [])

if revenue_data:
    fig = create_revenue_line_chart(revenue_data)
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate total and average
    total_rev = sum(item['revenue'] for item in revenue_data)
    avg_rev = total_rev / len(revenue_data) if revenue_data else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Revenue total période :** {format_currency(total_rev)}")
    with col2:
        st.info(f"**Revenue moyen/mois :** {format_currency(avg_rev)}")

st.markdown("---")

# Orders section
st.markdown("### 🛒 Analyse des Commandes")

col_left, col_right = st.columns(2)

with col_left:
    orders = data.get('orders', {})
    
    st.markdown("#### Métriques")
    st.metric("Total Commandes", format_number(orders.get('total', 0)))
    st.metric("Croissance", format_percentage(orders.get('growth', 0)))
    
    st.markdown("#### Par Statut")
    by_status = orders.get('by_status', {})
    for status, count in by_status.items():
        st.write(f"**{status.title()}** : {count}")

with col_right:
    status_chart = orders.get('status_chart', [])
    if status_chart:
        fig = create_orders_pie_chart(status_chart)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Insights
st.markdown("### 💡 Insights")

# Growth insight
growth_val = revenue.get('growth', 0)
if growth_val > 15:
    st.success(f"🚀 **Excellente performance !** Croissance de {growth_val:+.1f}% par rapport au mois précédent.")
elif growth_val > 5:
    st.info(f"✅ **Bonne croissance** de {growth_val:+.1f}%. Continuez sur cette lancée !")
elif growth_val > 0:
    st.warning(f"⚠️ **Croissance faible** ({growth_val:+.1f}%). Envisagez des actions marketing.")
else:
    st.error(f"❌ **Déclin** de {growth_val:.1f}%. Analyse urgente nécessaire !")

# CLV insight
clv_val = clv.get('value', 0)
aov_val = aov.get('value', 0)
if clv_val > aov_val * 2:
    st.success(f"🎯 **Bonne fidélisation !** CLV ({format_currency(clv_val)}) > 2× AOV ({format_currency(aov_val)})")

st.caption(f"Période : {data.get('period', {}).get('start_date', 'N/A')} → {data.get('period', {}).get('end_date', 'N/A')}")

