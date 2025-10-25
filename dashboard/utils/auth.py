"""
Authentication utilities for Streamlit dashboard.
"""
import streamlit as st
from .api_client import get_admin_token


def init_session_state():
    """Initialize session state variables."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None


def login(email: str, password: str) -> tuple[bool, str]:
    """
    Attempt to login with email/password.
    
    Args:
        email: User email
        password: User password
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    token = get_admin_token(email, password)
    
    if token:
        st.session_state.authenticated = True
        st.session_state.token = token
        st.session_state.user_email = email
        return True, "Connexion réussie !"
    else:
        st.session_state.authenticated = False
        st.session_state.token = None
        st.session_state.user_email = None
        return False, "Email ou mot de passe incorrect."


def logout():
    """Logout and clear session."""
    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.user_email = None


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.get('authenticated', False)


def get_current_token() -> str:
    """Get current user token."""
    return st.session_state.get('token', None)


def get_current_user_email() -> str:
    """Get current user email."""
    return st.session_state.get('user_email', None)


def require_authentication():
    """
    Decorator/function to require authentication.
    Redirects to login page if not authenticated.
    """
    if not is_authenticated():
        st.error("🔒 Vous devez être connecté pour accéder à cette page.")
        st.info("👉 Retournez à la page d'accueil pour vous connecter.")
        st.stop()

