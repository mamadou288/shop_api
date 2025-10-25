"""
Plotly charts functions for analytics dashboard.
"""
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any


def create_revenue_line_chart(data: List[Dict[str, Any]]) -> go.Figure:
    """
    Create line chart for revenue by month.
    
    Args:
        data: List of {month: str, revenue: float}
    
    Returns:
        Plotly figure
    """
    months = [item['month'] for item in data]
    revenues = [item['revenue'] for item in data]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months,
        y=revenues,
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(31, 119, 180, 0.2)',
        hovertemplate='<b>%{x}</b><br>Revenue: %{y:,.2f}€<extra></extra>'
    ))
    
    fig.update_layout(
        title='Revenue par mois',
        xaxis_title='Mois',
        yaxis_title='Revenue (€)',
        template='plotly_white',
        hovermode='x unified',
        height=400
    )
    
    return fig


def create_orders_pie_chart(data: List[Dict[str, Any]]) -> go.Figure:
    """
    Create pie/donut chart for orders by status.
    
    Args:
        data: List of {status: str, label: str, count: int}
    
    Returns:
        Plotly figure
    """
    labels = [item['label'] for item in data if item['count'] > 0]
    values = [item['count'] for item in data if item['count'] > 0]
    
    # Custom colors by status
    color_map = {
        'En attente': '#FFC107',     # Yellow
        'Confirmée': '#2196F3',      # Blue
        'Expédiée': '#9C27B0',       # Purple
        'Livrée': '#4CAF50',         # Green
        'Annulée': '#F44336'         # Red
    }
    
    colors = [color_map.get(label, '#757575') for label in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors),
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Commandes: %{value}<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Commandes par statut',
        template='plotly_white',
        height=400,
        showlegend=True
    )
    
    return fig


def create_top_products_bar_chart(data: List[Dict[str, Any]], by: str = 'revenue') -> go.Figure:
    """
    Create horizontal bar chart for top products.
    
    Args:
        data: List of product data
        by: 'revenue' or 'quantity'
    
    Returns:
        Plotly figure
    """
    # Limit to top 10
    data = data[:10]
    
    if by == 'revenue':
        names = [item['name'] for item in data]
        values = [item['revenue'] for item in data]
        title = 'Top 10 Produits par Revenue'
        x_label = 'Revenue (€)'
        hover_template = '<b>%{y}</b><br>Revenue: %{x:,.2f}€<extra></extra>'
    else:
        names = [item['name'] for item in data]
        values = [item['units_sold'] for item in data]
        title = 'Top 10 Produits par Quantité'
        x_label = 'Unités vendues'
        hover_template = '<b>%{y}</b><br>Quantité: %{x}<extra></extra>'
    
    # Reverse for better display (highest at top)
    names = names[::-1]
    values = values[::-1]
    
    fig = go.Figure(data=[go.Bar(
        x=values,
        y=names,
        orientation='h',
        marker=dict(
            color=values,
            colorscale='Blues',
            showscale=False
        ),
        hovertemplate=hover_template
    )])
    
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title='Produit',
        template='plotly_white',
        height=500,
        yaxis=dict(automargin=True)
    )
    
    return fig


def create_user_growth_line_chart(data: List[Dict[str, Any]]) -> go.Figure:
    """
    Create line chart for user growth by month.
    
    Args:
        data: List of {month: str, count: int}
    
    Returns:
        Plotly figure
    """
    months = [item['month'] for item in data]
    counts = [item['count'] for item in data]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months,
        y=counts,
        mode='lines+markers',
        name='Nouveaux utilisateurs',
        line=dict(color='#4CAF50', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(76, 175, 80, 0.2)',
        hovertemplate='<b>%{x}</b><br>Nouveaux: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Croissance utilisateurs par mois',
        xaxis_title='Mois',
        yaxis_title='Nouveaux utilisateurs',
        template='plotly_white',
        hovermode='x unified',
        height=400
    )
    
    return fig


def create_category_distribution_pie(data: List[Dict[str, Any]]) -> go.Figure:
    """
    Create pie chart for category distribution.
    
    Args:
        data: List of {name: str, revenue: float}
    
    Returns:
        Plotly figure
    """
    # Limit to top 10
    data = data[:10]
    
    labels = [item['name'] for item in data]
    values = [item['revenue'] for item in data]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=px.colors.qualitative.Set3),
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Revenue: %{value:,.2f}€<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Revenue par catégorie (Top 10)',
        template='plotly_white',
        height=400,
        showlegend=True
    )
    
    return fig


def create_user_segmentation_donut(data: Dict[str, int]) -> go.Figure:
    """
    Create donut chart for user segmentation.
    
    Args:
        data: Dict with segments (new, one_time, repeat, loyal)
    
    Returns:
        Plotly figure
    """
    labels = ['Nouveaux', 'Achat unique', 'Récurrents', 'Fidèles']
    values = [
        data.get('new', 0),
        data.get('one_time', 0),
        data.get('repeat', 0),
        data.get('loyal', 0)
    ]
    
    colors = ['#FFC107', '#2196F3', '#9C27B0', '#4CAF50']
    
    total = sum(values)
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(colors=colors),
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Utilisateurs: %{value}<br>%{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Segmentation utilisateurs',
        template='plotly_white',
        height=400,
        showlegend=True,
        annotations=[dict(
            text=f'Total<br>{total}',
            x=0.5, y=0.5,
            font_size=20,
            showarrow=False
        )]
    )
    
    return fig

