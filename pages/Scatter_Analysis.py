"""
Scatter Analysis Page
Interactive scatter plot to explore relationships between different player attributes
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
import numpy as np

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_fifa_data

st.set_page_config(page_title="Scatter Analysis", page_icon="📊", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    h1 {
        color: #ffffff !important;
        font-weight: 700 !important;
        padding: 25px !important;
        margin: 25px 0 !important;
        border-radius: 16px !important;
        background: linear-gradient(135deg, #2c5282 0%, #2b6cb0 50%, #3182ce 100%) !important;
        box-shadow: 0 8px 16px rgba(44, 82, 130, 0.3) !important;
        text-align: center !important;
    }
    h2 {
        color: #4299e1 !important;
        font-weight: 700 !important;
        margin: 30px 0 20px 0 !important;
        padding-bottom: 10px !important;
        border-bottom: 2px solid #2d3748 !important;
    }
    h3 {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        margin: 20px 0 15px 0 !important;
    }
    .stSelectbox > div > div {
        background-color: #1a202c;
    }
    </style>
""", unsafe_allow_html=True)

def get_numeric_columns():
    """Get list of numeric columns for plotting"""
    return [
        'overall', 'potential', 'value_eur', 'wage_eur', 'age',
        'height_cm', 'weight_kg', 'pace', 'shooting', 'passing',
        'dribbling', 'defending', 'physic', 'attacking_crossing',
        'attacking_finishing', 'attacking_heading_accuracy',
        'attacking_short_passing', 'attacking_volleys', 'skill_dribbling',
        'skill_curve', 'skill_fk_accuracy', 'skill_long_passing',
        'skill_ball_control', 'movement_acceleration', 'movement_sprint_speed',
        'movement_agility', 'movement_reactions', 'movement_balance',
        'power_shot_power', 'power_jumping', 'power_stamina',
        'power_strength', 'power_long_shots', 'mentality_aggression',
        'mentality_interceptions', 'mentality_positioning', 'mentality_vision',
        'mentality_penalties', 'mentality_composure', 'defending_marking_awareness',
        'defending_standing_tackle', 'defending_sliding_tackle',
        'goalkeeping_diving', 'goalkeeping_handling', 'goalkeeping_kicking',
        'goalkeeping_positioning', 'goalkeeping_reflexes', 'weak_foot',
        'skill_moves', 'international_reputation'
    ]

def get_categorical_columns():
    """Get list of categorical columns for color coding"""
    return [
        'position_category', 'league_name', 'preferred_foot', 
        'work_rate', 'body_type', 'nationality_name'
    ]

def format_column_name(col_name):
    """Format column name for display"""
    return col_name.replace('_', ' ').title()

def main():
    st.title("Scatter Analysis - Explore Player Attributes")
    
    st.markdown("""
        Explore relationships between different player attributes using interactive scatter plots.
        Select any two numeric attributes and color-code by categorical variables to uncover patterns.
    """)
    
    # Load data
    with st.spinner("Loading FIFA data..."):
        df = load_fifa_data()
    
    if df is None:
        st.error("Failed to load data. Please check the data file.")
        return
    
    # Sidebar filters
    with st.sidebar:
        st.header("Filters")
        
        # Year filter
        available_years = sorted(df['year'].unique(), reverse=True)
        selected_years = st.multiselect(
            "Select Year(s)",
            available_years,
            default=[available_years[0]],
            help="Filter data by specific years"
        )
        
        st.markdown("---")
        
        # Position filter
        positions = ['All'] + sorted(df['position_category'].unique().tolist())
        selected_position = st.selectbox(
            "Position Category",
            positions,
            help="Filter by position category"
        )
        
        # Overall rating filter
        min_overall = st.slider(
            "Minimum Overall Rating",
            int(df['overall'].min()),
            int(df['overall'].max()),
            80,
            help="Filter players by minimum overall rating"
        )
        
        st.markdown("---")
        
        # Sample size limiter for performance
        max_points = st.slider(
            "Maximum Data Points",
            100,
            5000,
            1000,
            step=100,
            help="Limit number of points for better performance"
        )
    
    # Filter data
    df_filtered = df[df['year'].isin(selected_years)].copy()
    
    if selected_position != 'All':
        df_filtered = df_filtered[df_filtered['position_category'] == selected_position]
    
    df_filtered = df_filtered[df_filtered['overall'] >= min_overall]
    
    # Sample if too many points
    if len(df_filtered) > max_points:
        df_filtered = df_filtered.sample(n=max_points, random_state=42)
    
    st.markdown("---")
    
    # Main configuration
    col1, col2, col3 = st.columns(3)
    
    numeric_cols = get_numeric_columns()
    categorical_cols = get_categorical_columns()
    
    # Format options for display
    numeric_options = {format_column_name(col): col for col in numeric_cols if col in df_filtered.columns}
    categorical_options = {format_column_name(col): col for col in categorical_cols if col in df_filtered.columns}
    
    with col1:
        x_axis_display = st.selectbox(
            "x-Axis Attribute",
            options=list(numeric_options.keys()),
            index=list(numeric_options.values()).index('overall') if 'overall' in numeric_options.values() else 0
        )
        x_axis = numeric_options[x_axis_display]
    
    with col2:
        y_axis_display = st.selectbox(
            "y-Axis Attribute",
            options=list(numeric_options.keys()),
            index=list(numeric_options.values()).index('value_eur') if 'value_eur' in numeric_options.values() else 1
        )
        y_axis = numeric_options[y_axis_display]
    
    with col3:
        hue_display = st.selectbox(
            "Color By (Hue)",
            options=['None'] + list(categorical_options.keys()),
            index=list(categorical_options.keys()).index(format_column_name('position_category')) + 1 if 'position_category' in categorical_options.values() else 0
        )
        hue = categorical_options.get(hue_display, None) if hue_display != 'None' else None
    
    st.markdown("---")
    
    # Create scatter plot
    if len(df_filtered) == 0:
        st.warning("No data available with current filters. Please adjust your selections.")
        return
    
    # Prepare data - remove NaN values for selected columns
    plot_columns = [x_axis, y_axis, 'short_name']
    if hue:
        plot_columns.append(hue)
    
    df_plot = df_filtered[plot_columns].dropna().copy()
    
    if len(df_plot) == 0:
        st.warning("No valid data points after removing missing values.")
        return
    
    # Calculate data ranges for jitter
    x_range = df_plot[x_axis].max() - df_plot[x_axis].min()
    y_range = df_plot[y_axis].max() - df_plot[y_axis].min()
    
    # Jitter control
    st.markdown("---")
    col_option1, col_option2 = st.columns([1, 3])
    
    with col_option1:
        show_trendline = st.checkbox("Show Trendline", value=True)
    
    # Hardcoded jitter amount
    jitter_amount = 2.0
    
    # Apply jitter to reduce overlapping points
    x_jitter = x_range * 0.005 * jitter_amount
    y_jitter = y_range * 0.005 * jitter_amount
    
    # Apply jitter
    np.random.seed(42)  # For reproducibility
    df_plot[f'{x_axis}_jittered'] = df_plot[x_axis] + np.random.uniform(-x_jitter, x_jitter, len(df_plot))
    df_plot[f'{y_axis}_jittered'] = df_plot[y_axis] + np.random.uniform(-y_jitter, y_jitter, len(df_plot))
    
    # Create the scatter plot
    if hue:
        # Use distinct colors for categories
        fig = px.scatter(
            df_plot,
            x=f'{x_axis}_jittered',
            y=f'{y_axis}_jittered',
            color=hue,
            hover_data={
                'short_name': True, 
                x_axis: ':.2f',  # Show original values in hover
                y_axis: ':.2f',
                f'{x_axis}_jittered': False,  # Hide jittered values
                f'{y_axis}_jittered': False
            },
            labels={
                f'{x_axis}_jittered': x_axis_display,
                f'{y_axis}_jittered': y_axis_display,
                hue: hue_display,
                x_axis: x_axis_display,
                y_axis: y_axis_display
            },
            title=f"{y_axis_display} vs {x_axis_display}",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
    else:
        fig = px.scatter(
            df_plot,
            x=f'{x_axis}_jittered',
            y=f'{y_axis}_jittered',
            hover_data={
                'short_name': True, 
                x_axis: ':.2f',
                y_axis: ':.2f',
                f'{x_axis}_jittered': False,
                f'{y_axis}_jittered': False
            },
            labels={
                f'{x_axis}_jittered': x_axis_display,
                f'{y_axis}_jittered': y_axis_display,
                x_axis: x_axis_display,
                y_axis: y_axis_display
            },
            title=f"{y_axis_display} vs {x_axis_display}",
            color_discrete_sequence=['#4299e1']
        )
    
    if show_trendline:
        # Calculate trendline using original (non-jittered) values
        z = np.polyfit(df_plot[x_axis], df_plot[y_axis], 1)
        p = np.poly1d(z)
        
        x_trend = np.linspace(df_plot[x_axis].min(), df_plot[x_axis].max(), 100)
        y_trend = p(x_trend)
        
        fig.add_trace(go.Scatter(
            x=x_trend,
            y=y_trend,
            mode='lines',
            name='Trendline',
            line=dict(color='rgba(255, 255, 255, 0.5)', width=2, dash='dash'),
            showlegend=True
        ))
        
        # Calculate correlation using original values
        correlation = df_plot[x_axis].corr(df_plot[y_axis])
        
        with col_option2:
            st.metric("Correlation Coefficient", f"{correlation:.3f}")
    
    # Update layout
    fig.update_layout(
        height=700,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(30, 37, 48, 0.5)',
        font=dict(color='white'),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            showgrid=True
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            showgrid=True
        ),
        legend=dict(
            bgcolor='rgba(30, 37, 48, 0.8)',
            bordercolor='rgba(255, 255, 255, 0.2)',
            borderwidth=1
        ),
        hovermode='closest'
    )
    
    fig.update_traces(marker=dict(size=8, line=dict(width=0.5, color='rgba(255, 255, 255, 0.3)')))
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Statistics section
    st.subheader("Statistical Summary")
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.metric("Data Points", f"{len(df_plot):,}")
    
    with col_stat2:
        st.metric(f"Mean {x_axis_display}", f"{df_plot[x_axis].mean():.2f}")
    
    with col_stat3:
        st.metric(f"Mean {y_axis_display}", f"{df_plot[y_axis].mean():.2f}")
    
    with col_stat4:
        st.metric("Filtered from Total", f"{len(df_filtered):,}")
    
    # Show top/bottom performers
    st.markdown("---")
    
    col_top1, col_top2 = st.columns(2)
    
    with col_top1:
        st.subheader(f"Top 10 by {y_axis_display}")
        top_players = df_plot.nlargest(10, y_axis)[['short_name', x_axis, y_axis]]
        top_players.columns = ['Player', x_axis_display, y_axis_display]
        st.dataframe(top_players, use_container_width=True, hide_index=True)
    
    with col_top2:
        st.subheader(f"Top 10 by {x_axis_display}")
        top_players_x = df_plot.nlargest(10, x_axis)[['short_name', x_axis, y_axis]]
        top_players_x.columns = ['Player', x_axis_display, y_axis_display]
        st.dataframe(top_players_x, use_container_width=True, hide_index=True)
    
    # Download filtered data option
    st.markdown("---")
    
    csv = df_plot.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name=f"fifa_scatter_{x_axis}_vs_{y_axis}.csv",
        mime="text/csv",
    )

if __name__ == "__main__":
    main()
