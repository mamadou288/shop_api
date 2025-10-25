"""
Users & Customers Analytics
"""
import streamlit as st
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.auth import init_session_state, require_authentication, get_current_token, get_current_user_email, logout
from utils.api_client import fetch_user_kpis, clear_cache
from utils.charts import create_user_growth_line_chart, create_user_segmentation_donut
from utils.metrics import format_currency, format_number, interpret_kpi
from utils.styles import inject_custom_css, create_page_header

st.set_page_config(
    page_title="Users - Analytics Dashboard",
    page_icon="👥",
    layout="wide"
)

init_session_state()
require_authentication()

inject_custom_css()

create_page_header(
    icon="👥",
    title="Users & Customers",
    description="Analyse des utilisateurs, clients et rétention"
)

# Sidebar
st.sidebar.title("⚙️ Configuration")

st.sidebar.success(f"👤 **{get_current_user_email()}**")
if st.sidebar.button("🚪 Déconnexion"):
    logout()
    st.rerun()

st.sidebar.markdown("---")

period = st.sidebar.selectbox(
    "Période",
    options=['7d', '30d', '90d', '1y'],
    index=2
)

if st.sidebar.button("🔄 Actualiser"):
    clear_cache()
    st.rerun()

# Fetch data
with st.spinner('Chargement des données utilisateurs...'):
    token = get_current_token()
    
    data = fetch_user_kpis(token, period)
    
    if not data:
        st.error("❌ Impossible de récupérer les données")
        st.stop()

# Main metrics
st.markdown("### 📊 Indicateurs Utilisateurs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_users = data.get('total_users', 0)
    st.metric(
        label="👥 Total Utilisateurs",
        value=format_number(total_users)
    )

with col2:
    active_users = data.get('active_users', 0)
    activation_rate = (active_users / total_users * 100) if total_users > 0 else 0
    st.metric(
        label="✅ Utilisateurs Actifs",
        value=format_number(active_users),
        delta=f"{activation_rate:.1f}%"
    )

with col3:
    new_users = data.get('new_users', 0)
    st.metric(
        label="🆕 Nouveaux (période)",
        value=format_number(new_users)
    )

with col4:
    retention = data.get('retention_rate', {}).get('percentage', 0)
    emoji, msg = interpret_kpi('retention', retention)
    st.metric(
        label="🔄 Rétention",
        value=f"{retention:.1f}%"
    )
    st.caption(f"{emoji} {msg}")

st.markdown("---")

# User growth
st.markdown("### 📈 Croissance Utilisateurs")

users_by_month = data.get('users_by_month', [])

if users_by_month:
    fig = create_user_growth_line_chart(users_by_month)
    st.plotly_chart(fig, use_container_width=True)
    
    total_new = sum(item['count'] for item in users_by_month)
    st.info(f"**Total nouveaux utilisateurs (période) :** {format_number(total_new)}")

st.markdown("---")

# Two columns
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 🥧 Segmentation Utilisateurs")
    
    segments = data.get('segments', {})
    
    if segments:
        fig = create_user_segmentation_donut(segments)
        st.plotly_chart(fig, use_container_width=True)
        
        # Segment details
        st.markdown("#### Détails")
        st.write(f"**Nouveaux** (0 commande) : {segments.get('new', 0)}")
        st.write(f"**Achat unique** (1 commande) : {segments.get('one_time', 0)}")
        st.write(f"**Récurrents** (2-4 commandes) : {segments.get('repeat', 0)}")
        st.write(f"**Fidèles** (5+ commandes) : {segments.get('loyal', 0)}")

with col_right:
    st.markdown("### 🏆 Top 10 Customers")
    
    top_customers = data.get('top_customers', [])
    
    if top_customers:
        df = pd.DataFrame(top_customers)
        
        df_display = df[['name', 'email', 'total_spent', 'order_count']].copy()
        df_display['total_spent'] = df_display['total_spent'].apply(lambda x: format_currency(x))
        df_display.columns = ['Nom', 'Email', 'Total dépensé', 'Commandes']
        
        st.dataframe(df_display, use_container_width=True, height=400)
        
        # Top customer highlight
        top_1 = top_customers[0]
        st.success(f"🏆 **Top customer :** {top_1['name']} avec {format_currency(top_1['total_spent'])} ({top_1['order_count']} commandes)")

st.markdown("---")

# Insights
st.markdown("### 💡 Insights")

# Activation rate
if activation_rate > 50:
    st.success(f"✅ **Bon taux d'activation** : {activation_rate:.1f}% des utilisateurs ont passé au moins 1 commande")
else:
    st.warning(f"⚠️ **Taux d'activation faible** : {activation_rate:.1f}%. Optimisez l'onboarding pour convertir plus d'inscrits en acheteurs.")

# Loyal customers
loyal_count = segments.get('loyal', 0)
loyal_pct = (loyal_count / total_users * 100) if total_users > 0 else 0
if loyal_pct > 10:
    st.success(f"🌟 **{loyal_pct:.1f}% de clients fidèles** (5+ commandes). Excellente fidélisation !")
elif loyal_pct > 5:
    st.info(f"👍 **{loyal_pct:.1f}% de clients fidèles**. Bon ratio, continuez les efforts de rétention.")
else:
    st.warning(f"⚠️ **Seulement {loyal_pct:.1f}% de clients fidèles**. Implémentez un programme de fidélité.")

# Retention
if retention > 60:
    st.success(f"🔥 **Excellente rétention** : {retention:.1f}% des clients reviennent !")
elif retention < 40:
    st.error(f"❌ **Rétention faible** ({retention:.1f}%). Actions urgentes : email marketing, remarketing, améliorer l'expérience.")

st.caption(f"Période : {data.get('period', {}).get('start_date', 'N/A')} → {data.get('period', {}).get('end_date', 'N/A')}")

