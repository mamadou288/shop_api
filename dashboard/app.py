"""
Shop E-commerce Analytics Dashboard
Login Page - Authentication required
"""
import streamlit as st
from utils.auth import init_session_state, login, logout, is_authenticated, get_current_user_email

# Page configuration
st.set_page_config(
    page_title="Login - Analytics Dashboard",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize session
init_session_state()

# Custom CSS for login page
st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton > button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: 600;
        padding: 0.75rem;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Check if already authenticated
if is_authenticated():
    st.success(f"✅ Vous êtes connecté en tant que **{get_current_user_email()}**")
    
    st.markdown("""
    # 📊 Shop E-commerce Analytics Dashboard
    
    **Naviguez vers une page via le menu latéral :**
    
    - 📊 **Overview** - Vue d'ensemble des KPIs principaux
    - 💰 **Business** - Analyse revenue & croissance  
    - 📦 **Products** - Inventory & top produits
    - 👥 **Users** - Clients & rétention
    
    ---
    """)
    
    st.info("💡 Sélectionnez une page dans le menu latéral pour commencer l'analyse !", icon="📊")
    
    # Logout button
    if st.button("🚪 Se déconnecter"):
        logout()
        st.rerun()

else:
    # Login form
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1>🔐 Connexion</h1>
            <p style="color: #666;">Analytics Dashboard - Admin uniquement</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown("### 📧 Identifiants")
        
        email = st.text_input(
            "Email",
            placeholder="admin@shop.com",
            help="Utilisez un compte admin pour accéder au dashboard"
        )
        
        password = st.text_input(
            "Mot de passe",
            type="password",
            placeholder="••••••••",
            help="Mot de passe de votre compte admin"
        )
        
        submitted = st.form_submit_button("🔓 Se connecter")
        
        if submitted:
            if not email or not password:
                st.error("❌ Veuillez remplir tous les champs.")
            else:
                with st.spinner("Authentification en cours..."):
                    success, message = login(email, password)
                    
                    if success:
                        st.success(message)
                        st.info("✨ Redirection en cours...")
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
    
    # Info box
    st.markdown("---")
    
    with st.expander("ℹ️ Informations"):
        st.markdown("""
        **Prérequis :**
        - L'API Django doit être lancée sur `http://localhost:8000`
        - Vous devez avoir un compte admin
        
        **Compte de test :**
        - Email : `admin@shop.com`
        - Mot de passe : `TestPass123!`
        
        **Note :** Seuls les administrateurs peuvent accéder au dashboard analytics.
        """)
    
    st.caption("Shop E-commerce API © 2025")

