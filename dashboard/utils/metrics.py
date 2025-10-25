"""
Metrics and formatting utilities for dashboard.
"""
import streamlit as st
from typing import Optional, Union


def display_metric_card(
    label: str,
    value: Union[str, float, int],
    delta: Optional[Union[str, float]] = None,
    delta_color: str = "normal"
):
    """
    Display a metric card with optional delta.
    
    Args:
        label: Metric name
        value: Metric value
        delta: Change value (optional)
        delta_color: "normal", "inverse", or "off"
    """
    st.metric(
        label=label,
        value=value,
        delta=delta,
        delta_color=delta_color
    )


def format_currency(value: float, currency: str = 'EUR') -> str:
    """
    Format number as currency.
    
    Args:
        value: Number to format
        currency: Currency code (default: EUR)
    
    Returns:
        Formatted string (e.g., "125 890,50 €")
    """
    if currency == 'EUR':
        return f"{value:,.2f} €".replace(',', ' ').replace('.', ',')
    elif currency == 'USD':
        return f"${value:,.2f}"
    else:
        return f"{value:,.2f} {currency}"


def format_percentage(value: float) -> str:
    """
    Format number as percentage with sign.
    
    Args:
        value: Number to format
    
    Returns:
        Formatted string (e.g., "+15.3%" or "-5.2%")
    """
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"


def format_number(value: Union[int, float]) -> str:
    """
    Format number with thousand separators.
    
    Args:
        value: Number to format
    
    Returns:
        Formatted string (e.g., "1 250")
    """
    if isinstance(value, float):
        return f"{value:,.0f}".replace(',', ' ')
    return f"{value:,}".replace(',', ' ')


def get_metric_icon(metric_type: str) -> str:
    """
    Get emoji icon for metric type.
    
    Args:
        metric_type: Type of metric
    
    Returns:
        Emoji string
    """
    icons = {
        'revenue': '💰',
        'money': '💰',
        'orders': '🛒',
        'cart': '🛒',
        'users': '👥',
        'customers': '👥',
        'products': '📦',
        'inventory': '📦',
        'growth': '📈',
        'up': '📈',
        'down': '📉',
        'trend': '📊',
        'aov': '💳',
        'card': '💳',
        'clv': '🎯',
        'target': '🎯',
        'repeat': '🔄',
        'refresh': '🔄',
        'retention': '🤝',
        'handshake': '🤝',
        'new': '🆕',
        'active': '✅',
        'check': '✅',
        'warning': '⚠️',
        'alert': '⚠️',
        'star': '⭐',
        'fire': '🔥',
        'rocket': '🚀',
    }
    return icons.get(metric_type.lower(), '📊')


def get_growth_indicator(value: float) -> str:
    """
    Get growth trend indicator.
    
    Args:
        value: Growth percentage
    
    Returns:
        Arrow emoji (↑, ↓, →)
    """
    if value > 0:
        return "↑"
    elif value < 0:
        return "↓"
    else:
        return "→"


def interpret_kpi(kpi_name: str, value: float) -> tuple[str, str]:
    """
    Interpret KPI value and return status + message.
    
    Args:
        kpi_name: Name of the KPI
        value: KPI value
    
    Returns:
        Tuple of (emoji, message)
    """
    if kpi_name == 'growth':
        if value > 15:
            return ("🚀", "Excellente croissance")
        elif value > 5:
            return ("✅", "Bonne croissance")
        elif value > 0:
            return ("⚠️", "Croissance faible")
        else:
            return ("❌", "Déclin")
    
    elif kpi_name == 'repeat_rate':
        if value > 40:
            return ("🚀", "Excellente fidélisation")
        elif value > 25:
            return ("✅", "Bonne fidélisation")
        elif value > 10:
            return ("⚠️", "Fidélisation moyenne")
        else:
            return ("❌", "Problème de fidélisation")
    
    elif kpi_name == 'retention':
        if value > 60:
            return ("🚀", "Excellente rétention")
        elif value > 40:
            return ("✅", "Bonne rétention")
        elif value > 20:
            return ("⚠️", "Rétention moyenne")
        else:
            return ("❌", "Rétention critique")
    
    else:
        return ("📊", "")

