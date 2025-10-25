"""
API Client for Django Analytics API.
"""
import requests
import streamlit as st
from typing import Optional, Dict, Any


# Configuration
API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30


def get_admin_token(email: str = "admin@shop.com", password: str = "TestPass123!") -> Optional[str]:
    """
    Login with admin credentials and return access token.
    
    Args:
        email: Admin email
        password: Admin password
    
    Returns:
        str: Access token or None if login fails
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/auth/login/",
            json={"email": email, "password": password},
            timeout=API_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("access")
        else:
            st.error(f"Login failed: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None


@st.cache_data(ttl=900)  # Cache for 15 minutes
def fetch_dashboard_kpis(token: str, period: str = '90d') -> Optional[Dict[str, Any]]:
    """
    Fetch all KPIs (business, products, users) from dashboard endpoint.
    
    Args:
        token: JWT access token
        period: Period shortcut (7d, 30d, 90d, 1y)
    
    Returns:
        dict: Dashboard data or None if error
    """
    try:
        headers = {"Authorization": f"Bearer {token}"}
        params = {"period": period}
        
        response = requests.get(
            f"{API_BASE_URL}/api/analytics/dashboard/",
            headers=headers,
            params=params,
            timeout=API_TIMEOUT
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.error("Authentication expired. Please refresh the page.")
            return None
        else:
            st.error(f"API error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None


@st.cache_data(ttl=900)
def fetch_business_kpis(
    token: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: str = '90d'
) -> Optional[Dict[str, Any]]:
    """
    Fetch business KPIs (revenue, orders, AOV, growth, CLV, repeat rate).
    
    Args:
        token: JWT access token
        start_date: Start date (YYYY-MM-DD) - optional
        end_date: End date (YYYY-MM-DD) - optional
        period: Period shortcut if no custom dates
    
    Returns:
        dict: Business KPIs data or None if error
    """
    try:
        headers = {"Authorization": f"Bearer {token}"}
        params = {}
        
        if start_date and end_date:
            params['start_date'] = start_date
            params['end_date'] = end_date
        else:
            params['period'] = period
        
        response = requests.get(
            f"{API_BASE_URL}/api/analytics/business/",
            headers=headers,
            params=params,
            timeout=API_TIMEOUT
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.error("Authentication expired. Please refresh the page.")
            return None
        else:
            st.error(f"API error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None


@st.cache_data(ttl=900)
def fetch_product_kpis(token: str) -> Optional[Dict[str, Any]]:
    """
    Fetch product KPIs (top products, stock alerts, categories).
    
    Args:
        token: JWT access token
    
    Returns:
        dict: Product KPIs data or None if error
    """
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(
            f"{API_BASE_URL}/api/analytics/products/",
            headers=headers,
            timeout=API_TIMEOUT
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.error("Authentication expired. Please refresh the page.")
            return None
        else:
            st.error(f"API error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None


@st.cache_data(ttl=900)
def fetch_user_kpis(token: str, period: str = '90d') -> Optional[Dict[str, Any]]:
    """
    Fetch user KPIs (total, active, retention, top customers, segments).
    
    Args:
        token: JWT access token
        period: Period shortcut (7d, 30d, 90d, 1y)
    
    Returns:
        dict: User KPIs data or None if error
    """
    try:
        headers = {"Authorization": f"Bearer {token}"}
        params = {"period": period}
        
        response = requests.get(
            f"{API_BASE_URL}/api/analytics/users/",
            headers=headers,
            params=params,
            timeout=API_TIMEOUT
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.error("Authentication expired. Please refresh the page.")
            return None
        else:
            st.error(f"API error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None


def clear_cache():
    """Clear all cached data."""
    st.cache_data.clear()

