"""
Player Analysis Page
Track player statistics evolution over the years
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path
import numpy as np
import base64

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_fifa_data, get_player_evolution
from components.player_selector import player_search_selector, player_dropdown_selector

def get_image_base64(image_path):
    """Convert image to base64 for HTML embedding"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

st.set_page_config(page_title="Player Analysis", page_icon="📊", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .player-card {
        background: linear-gradient(135deg, #2c5282 0%, #2b6cb0 100%);
        padding: 25px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 16px rgba(44, 82, 130, 0.3);
    }
    .stat-bar {
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        height: 24px;
        margin: 8px 0;
        overflow: hidden;
    }
    .stat-fill {
        height: 100%;
        border-radius: 8px;
        transition: width 0.5s ease;
        background: linear-gradient(90deg, #4299e1 0%, #3182ce 100%);
    }
    .attribute-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 15px;
        margin-top: 15px;
    }
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
    </style>
""", unsafe_allow_html=True)

def create_evolution_chart(player_data, attributes):
    """
    Create a line chart showing player attribute evolution over years
    """
    fig = go.Figure()
    
    for attr in attributes:
        if attr in player_data.columns:
            fig.add_trace(go.Scatter(
                x=player_data['year'],
                y=player_data[attr],
                mode='lines+markers',
                name=attr.replace('_', ' ').title(),
                line=dict(width=3),
                marker=dict(size=8)
            ))
    
    fig.update_layout(
        title="Player Attribute Evolution Over Time",
        xaxis_title="Year",
        yaxis_title="Rating",
        hovermode='x unified',
        height=500,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.05
        ),
        yaxis=dict(range=[0, 100])
    )
    
    return fig

def create_potential_vs_actual_chart(player_data):
    """
    Create a chart comparing potential vs actual overall rating
    """
    fig = go.Figure()
    
    # Actual overall
    fig.add_trace(go.Scatter(
        x=player_data['year'],
        y=player_data['overall'],
        mode='lines+markers',
        name='Overall Rating',
        line=dict(width=3, color='blue'),
        marker=dict(size=10)
    ))
    
    # Potential
    fig.add_trace(go.Scatter(
        x=player_data['year'],
        y=player_data['potential'],
        mode='lines+markers',
        name='Potential',
        line=dict(width=3, color='orange', dash='dash'),
        marker=dict(size=10)
    ))
    
    # Gap area
    fig.add_trace(go.Scatter(
        x=player_data['year'].tolist() + player_data['year'].tolist()[::-1],
        y=player_data['potential'].tolist() + player_data['overall'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(255, 165, 0, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Potential Gap',
        showlegend=True
    ))
    
    fig.update_layout(
        title="Overall Rating vs Potential Over Time",
        xaxis_title="Year",
        yaxis_title="Rating",
        hovermode='x unified',
        height=400,
        yaxis=dict(range=[0, 100])
    )
    
    return fig

def create_mini_sparkline(values, color='#4CAF50'):
    """
    Create a mini sparkline chart for attribute history
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=values,
        mode='lines',
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.3)',
        hovertemplate='Value: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=50,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='closest'
    )
    
    return fig

def get_stat_color(category):
    """
    Get color for stat category
    """
    colors = {
        'attacking': '#7CFC00',
        'movement': '#FFFF00', 
        'mentality': '#FFA500',
        'skills': '#00FF00',
        'power': '#FFD700',
        'defending': '#FF8C00',
        'goalkeeping': '#FF0000'
    }
    return colors.get(category, '#808080')

def create_attribute_history_chart(player_data, attribute, current_year):
    """
    Create FIFA-style attribute history chart with years on X-axis
    """
    fig = go.Figure()
    
    years = player_data['year'].tolist()
    values = player_data[attribute].tolist()
    
    # Calculate dynamic range with some padding
    min_val = min(values)
    max_val = max(values)
    range_padding = (max_val - min_val) * 0.1  # 10% padding
    if range_padding < 5:  # Minimum padding of 5 units
        range_padding = 5
    y_min = max(0, min_val - range_padding)
    y_max = min(100, max_val + range_padding)
    
    # Create area chart with gradient
    fig.add_trace(go.Scatter(
        x=years,
        y=values,
        mode='lines',
        line=dict(color='white', width=2),
        fill='tozeroy',
        fillcolor='rgba(100, 150, 180, 0.5)',
        showlegend=False,
        hovertemplate='<b>Year %{x}</b><br>Value: %{y}<extra></extra>'
    ))
    
    # Highlight current year point
    current_idx = years.index(current_year) if current_year in years else -1
    if current_idx >= 0:
        fig.add_trace(go.Scatter(
            x=[years[current_idx]],
            y=[values[current_idx]],
            mode='markers',
            marker=dict(size=10, color='#FF4B4B', line=dict(color='white', width=2)),
            showlegend=False,
            hovertemplate='<b>Current</b><br>%{y}<extra></extra>'
        ))
    
    fig.update_layout(
        height=120,
        margin=dict(l=35, r=10, t=25, b=20),
        xaxis=dict(
            showgrid=False,
            showticklabels=True,
            tickfont=dict(size=9, color='white'),
            title=None,
            fixedrange=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            showticklabels=True,
            tickfont=dict(size=9, color='white'),
            range=[y_min, y_max],
            fixedrange=True
        ),
        plot_bgcolor='rgba(30, 50, 70, 0.9)',
        paper_bgcolor='rgba(0,0,0,0)',
        title=dict(
            text="Attribute History over Years",
            font=dict(size=11, color='white'),
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        hovermode='closest'
    )
    
    return fig

def create_percentile_chart(df, player_row, attribute, current_year):
    """
    Create percentile comparison chart showing player rank vs similar positions
    """
    position_category = player_row['position_category']
    
    # Filter for current year and same position
    year_data = df[(df['year'] == current_year) & 
                   (df['position_category'] == position_category) &
                   (df[attribute].notna())]
    
    if len(year_data) < 10:
        return None
    
    player_value = player_row[attribute]
    percentile = (year_data[attribute] < player_value).sum() / len(year_data) * 100
    
    fig = go.Figure()
    
    # Create histogram
    fig.add_trace(go.Histogram(
        x=year_data[attribute],
        nbinsx=25,
        marker=dict(
            color='rgba(100, 150, 180, 0.6)',
            line=dict(color='rgba(255, 255, 255, 0.3)', width=0.5)
        ),
        showlegend=False,
        hovertemplate='Range: %{x}<br>Players: %{y}<extra></extra>'
    ))
    
    # Add player marker line
    fig.add_vline(
        x=player_value,
        line=dict(color='#FF4B4B', width=3),
        annotation_text=f"This Player",
        annotation_position="top",
        annotation=dict(
            font=dict(size=9, color='white'),
            bgcolor='rgba(255, 75, 75, 0.9)',
            bordercolor='white',
            borderwidth=1,
            borderpad=3
        )
    )
    
    fig.update_layout(
        height=160,
        margin=dict(l=10, r=10, t=55, b=25),
        xaxis=dict(
            showgrid=False,
            showticklabels=True,
            tickfont=dict(size=9, color='white'),
            range=[0, 100],
            title=None,
            fixedrange=True
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            fixedrange=True
        ),
        plot_bgcolor='rgba(30, 50, 70, 0.9)',
        paper_bgcolor='rgba(0,0,0,0)',
        title=dict(
            text=f"Comparison to {position_category}s<br><sub>Percentile: {percentile:.0f}% (Top {100-percentile:.0f}%)</sub>",
            font=dict(size=11, color='white'),
            x=0.5,
            xanchor='center',
            y=0.96,
            yanchor='top',
            pad=dict(t=10)
        ),
        bargap=0.05,
        hovermode='closest'
    )
    
    return fig

def get_position_specific_stats(player_data):
    """
    Get position-specific radar chart attributes and key stats based on player position
    """
    position_category = player_data.get('position_category', 'Unknown')
    player_positions = str(player_data.get('player_positions', '')).upper()
    
    # Determine position-specific attributes
    if position_category == 'Goalkeepers' or 'GK' in player_positions:
        radar_attrs = ['goalkeeping_diving', 'goalkeeping_handling', 'goalkeeping_kicking', 
                      'goalkeeping_positioning', 'goalkeeping_reflexes', 'goalkeeping_speed']
        radar_labels = ['Diving', 'Handling', 'Kicking', 'Positioning', 'Reflexes', 'Speed']
        key_stats = [
            ('Diving', 'goalkeeping_diving'),
            ('Handling', 'goalkeeping_handling'),
            ('Kicking', 'goalkeeping_kicking'),
            ('Positioning', 'goalkeeping_positioning'),
            ('Reflexes', 'goalkeeping_reflexes')
        ]
    elif position_category == 'Defenders':
        radar_attrs = ['defending', 'physic', 'pace', 'passing', 'mentality_interceptions', 'power_strength']
        radar_labels = ['Defending', 'Physical', 'Pace', 'Passing', 'Interceptions', 'Strength']
        key_stats = [
            ('Defending', 'defending'),
            ('Physical', 'physic'),
            ('Pace', 'pace'),
            ('Passing', 'passing'),
            ('Strength', 'power_strength')
        ]
    elif position_category == 'Midfielders':
        radar_attrs = ['passing', 'dribbling', 'pace', 'shooting', 'defending', 'physic']
        radar_labels = ['Passing', 'Dribbling', 'Pace', 'Shooting', 'Defending', 'Physical']
        key_stats = [
            ('Passing', 'passing'),
            ('Dribbling', 'dribbling'),
            ('Vision', 'mentality_vision'),
            ('Stamina', 'power_stamina'),
            ('Ball Control', 'skill_ball_control')
        ]
    elif position_category == 'Forwards':
        radar_attrs = ['shooting', 'pace', 'dribbling', 'passing', 'physic', 'mentality_positioning']
        radar_labels = ['Shooting', 'Pace', 'Dribbling', 'Passing', 'Physical', 'Positioning']
        key_stats = [
            ('Shooting', 'shooting'),
            ('Pace', 'pace'),
            ('Dribbling', 'dribbling'),
            ('Finishing', 'attacking_finishing'),
            ('Positioning', 'mentality_positioning')
        ]
    else:
        # Default to general stats
        radar_attrs = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
        radar_labels = ['Pace', 'Shooting', 'Passing', 'Dribbling', 'Defending', 'Physical']
        key_stats = [
            ('Pace', 'pace'),
            ('Shooting', 'shooting'),
            ('Passing', 'passing'),
            ('Dribbling', 'dribbling'),
            ('Defending', 'defending')
        ]
    
    return radar_attrs, radar_labels, key_stats

def display_detailed_player_card(player_row, player_evolution):
    """
    Display a detailed player card similar to the reference image
    """
    latest_data = player_evolution.iloc[-1]
    
    # Get player image path
    player_image_html = ""
    if 'player_face_url' in latest_data.index:
        player_face_url = latest_data['player_face_url']
        if pd.notna(player_face_url) and str(player_face_url).startswith('http'):
            try:
                url_parts = player_face_url.split('/')
                local_filename = f"{url_parts[-3]}_{url_parts[-2]}_{url_parts[-1]}"
                local_path = Path("player_images") / local_filename
                
                if local_path.exists():
                    # Use local image in card
                    player_image_html = f'<img src="data:image/png;base64,{get_image_base64(str(local_path))}" style="width: 150px; height: 150px; border-radius: 10px; object-fit: cover; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">'
            except:
                pass
    
    # Main card container with centered image
    st.markdown(f"""
        <div class="player-card">
            <div style="display: flex; justify-content: space-between; align-items: center; gap: 30px;">
                <div style="flex: 1;">
                    <h1 style="margin: 0; font-size: 48px; font-weight: bold;">{latest_data['short_name']}</h1>
                    <h3 style="margin: 5px 0; opacity: 0.8;">{latest_data.get('club_name', 'Unknown Club')}</h3>
                </div>
                <div style="display: flex; justify-content: center; align-items: center;">
                    {player_image_html}
                </div>
                <div style="flex: 1; text-align: right;">
                    <h2 style="margin: 0; font-size: 36px; opacity: 0.8;">{latest_data.get('player_positions', 'N/A').split(',')[0].strip()}</h2>
                    <h3 style="margin: 5px 0; opacity: 0.8;">{latest_data.get('nationality_name', 'Unknown')}</h3>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        # Basic info
        st.markdown("### Basic Info")
        st.metric("Age", int(latest_data.get('age', 0)))
        st.metric("Height", f"{latest_data.get('height_cm', 0):.0f} cm" if pd.notna(latest_data.get('height_cm')) else "N/A")
        st.metric("Weight", f"{latest_data.get('weight_kg', 0):.0f} kg" if pd.notna(latest_data.get('weight_kg')) else "N/A")
        st.markdown(f"**Value:** €{latest_data.get('value_eur', 0):,.0f}")
        st.markdown(f"**Wage:** €{latest_data.get('wage_eur', 0):,.0f}")
        st.markdown(f"**Preferred Foot:** {latest_data.get('preferred_foot', 'N/A')}")
    
    with col2:
        # Get position-specific stats
        radar_attrs, radar_labels, key_stats_config = get_position_specific_stats(latest_data)
        
        # Main overall rating
        st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: rgba(0,0,0,0.2); border-radius: 10px; margin-bottom: 20px;">
                <div style="font-size: 72px; font-weight: bold; color: white;">{int(latest_data['overall'])}</div>
                <div style="font-size: 18px; opacity: 0.7;">Overall</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Mini radar chart for position-specific stats
        values = [latest_data.get(attr, 0) for attr in radar_attrs]
        values.append(values[0])
        labels_closed = radar_labels + [radar_labels[0]]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=labels_closed,
            fill='toself',
            fillcolor='rgba(76, 175, 80, 0.3)',
            line=dict(color='rgba(76, 175, 80, 1)', width=2)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], showticklabels=False),
                bgcolor='rgba(0,0,0,0.1)'
            ),
            showlegend=False,
            height=300,
            margin=dict(l=60, r=60, t=40, b=40),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True, key="radar_chart", config={'displayModeBar': False})
    
    with col3:
        # Position-specific key stats
        st.markdown("### Key Stats")
        st.metric("Potential", int(latest_data.get('potential', 0)))
        
        for stat_label, stat_attr in key_stats_config:
            value = latest_data.get(stat_attr, 0)
            if pd.notna(value):
                st.metric(stat_label, int(value))
            else:
                st.metric(stat_label, "N/A")

def main():
    st.title("Player Analysis - Career Progression")
    
    # Load data
    with st.spinner("Loading FIFA data..."):
        df = load_fifa_data()
    
    if df is None:
        st.error("Failed to load data. Please check the data file.")
        return
    
    # Filter to only 2022 data for player search
    df_2022 = df[df['year'] == 2022].copy()
    
    st.markdown("""
    Track how player statistics evolved over the years (2015-2022).
    See career progression, potential vs actual performance.
    """)
    
    st.subheader("Single Player Career Analysis")
    
    # Player selection (using 2022 data only)
    filtered_df = player_search_selector(df_2022, key_suffix="evolution", year_filter=False)
    
    if len(filtered_df) > 0:
        selected_player = player_dropdown_selector(
            filtered_df,
            label="Select Player",
            key_suffix="evolution"
        )
        
        if selected_player is not None:
            player_id = selected_player['sofifa_id']
            
            # Get all years data for this player
            player_evolution = get_player_evolution(df, player_id)
            
            if len(player_evolution) > 1:
                # Display detailed player card
                st.markdown("---")
                display_detailed_player_card(selected_player, player_evolution)
                
                # Career summary
                st.markdown("---")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Years Tracked", len(player_evolution))
                
                with col2:
                    current_overall = player_evolution.iloc[-1]['overall']
                    first_overall = player_evolution.iloc[0]['overall']
                    change = current_overall - first_overall
                    st.metric(
                        "Career Change",
                        f"{change:+.0f}",
                        f"From {int(first_overall)} to {int(current_overall)}"
                    )
                
                with col3:
                    peak_overall = player_evolution['overall'].max()
                    peak_year = player_evolution[player_evolution['overall'] == peak_overall]['year'].iloc[0]
                    st.metric("Peak Overall", int(peak_overall), f"Year {int(peak_year)}")
                
                with col4:
                    avg_overall = player_evolution['overall'].mean()
                    st.metric("Average Overall", f"{avg_overall:.1f}")
                
                # Detailed Attributes with Sparklines
                st.markdown("---")
                st.subheader("Detailed Attributes (Hover to see history)")
                
                latest_data = player_evolution.iloc[-1]
                
                # Attribute categories
                attribute_categories = {
                        'Attacking': {
                            'attrs': ['attacking_crossing', 'attacking_finishing', 'attacking_heading_accuracy', 
                                     'attacking_short_passing', 'attacking_volleys'],
                            'labels': ['Crossing', 'Finishing', 'Heading Accuracy', 'Short Passing', 'Volleys'],
                            'color': '#7CFC00'
                        },
                        'Movement': {
                            'attrs': ['movement_acceleration', 'movement_sprint_speed', 'movement_agility', 
                                     'movement_reactions', 'movement_balance'],
                            'labels': ['Acceleration', 'Sprint Speed', 'Agility', 'Reactions', 'Balance'],
                            'color': '#FFFF00'
                        },
                        'Mentality': {
                            'attrs': ['mentality_aggression', 'mentality_interceptions', 'mentality_positioning', 
                                     'mentality_vision', 'mentality_penalties', 'mentality_composure'],
                            'labels': ['Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure'],
                            'color': '#FFA500'
                        },
                        'Skills': {
                            'attrs': ['skill_dribbling', 'skill_curve', 'skill_fk_accuracy', 
                                     'skill_long_passing', 'skill_ball_control'],
                            'labels': ['Dribbling', 'Curve', 'FK Accuracy', 'Long Passing', 'Ball Control'],
                            'color': '#00FF00'
                        },
                        'Power': {
                            'attrs': ['power_shot_power', 'power_jumping', 'power_stamina', 
                                     'power_strength', 'power_long_shots'],
                            'labels': ['Shot Power', 'Jumping', 'Stamina', 'Strength', 'Long Shots'],
                            'color': '#FFD700'
                        },
                        'Defending': {
                            'attrs': ['defending_marking_awareness', 'defending_standing_tackle', 
                                     'defending_sliding_tackle'],
                            'labels': ['Marking', 'Standing Tackle', 'Sliding Tackle'],
                            'color': '#FF8C00'
                        },
                        'Goalkeeping': {
                            'attrs': ['goalkeeping_diving', 'goalkeeping_handling', 'goalkeeping_kicking', 
                                     'goalkeeping_positioning', 'goalkeeping_reflexes', 'goalkeeping_speed'],
                            'labels': ['Diving', 'Handling', 'Kicking', 'Positioning', 'Reflexes', 'Speed'],
                            'color': '#FF0000'
                        }
                }
                
                # Display attributes in tabs
                tabs = st.tabs(list(attribute_categories.keys()))
                
                for tab, (category, data) in zip(tabs, attribute_categories.items()):
                    with tab:
                        # Create columns for attributes
                        num_cols = 2
                        rows = (len(data['attrs']) + num_cols - 1) // num_cols
                        
                        for row in range(rows):
                            cols = st.columns(num_cols)
                            for col_idx in range(num_cols):
                                attr_idx = row * num_cols + col_idx
                                if attr_idx < len(data['attrs']):
                                    with cols[col_idx]:
                                        attr = data['attrs'][attr_idx]
                                        label = data['labels'][attr_idx]
                                        
                                        if attr in latest_data:
                                            value = int(latest_data[attr])
                                            
                                            # Get historical values for sparkline
                                            historical_values = player_evolution[attr].tolist()
                                            
                                            # Create expander for detailed view
                                            with st.expander(f"**{label}**: {value}", expanded=False):
                                                # Historical chart
                                                history_fig = create_attribute_history_chart(
                                                    player_evolution, 
                                                    attr, 
                                                    latest_data['year']
                                                )
                                                st.plotly_chart(history_fig, use_container_width=True, 
                                                              key=f"history_{attr}")
                                                
                                                # Percentile comparison
                                                percentile_fig = create_percentile_chart(
                                                    df, 
                                                    latest_data, 
                                                    attr, 
                                                    latest_data['year']
                                                )
                                                if percentile_fig:
                                                    st.plotly_chart(percentile_fig, use_container_width=True, 
                                                                  key=f"percentile_{attr}")
                                            
                                            # Progress bar
                                            st.progress(value / 100)
                
                # Potential vs Actual
                st.markdown("---")
                st.subheader("Overall vs Potential")
                
                potential_fig = create_potential_vs_actual_chart(player_evolution)
                st.plotly_chart(potential_fig, use_container_width=True)
                
                # Main attributes evolution
                st.markdown("---")
                st.subheader("Main Attributes Evolution")
                
                # Get position-specific attributes for the evolution chart
                radar_attrs, radar_labels, _ = get_position_specific_stats(selected_player)
                main_fig = create_evolution_chart(player_evolution, radar_attrs)
                st.plotly_chart(main_fig, use_container_width=True)
                
                # Evolution table
                st.markdown("---")
                st.subheader("Year-by-Year Breakdown")
                
                display_cols = ['year', 'overall', 'potential', 'age', 'club_name', 
                               'value_eur', 'wage_eur', 'pace', 'shooting', 'passing', 
                               'dribbling', 'defending', 'physic']
                
                available_display_cols = [col for col in display_cols if col in player_evolution.columns]
                evolution_table = player_evolution[available_display_cols].copy()
                
                # Format currency columns
                if 'value_eur' in evolution_table.columns:
                    evolution_table['value_eur'] = evolution_table['value_eur'].apply(lambda x: f"€{x:,.0f}")
                if 'wage_eur' in evolution_table.columns:
                    evolution_table['wage_eur'] = evolution_table['wage_eur'].apply(lambda x: f"€{x:,.0f}")
                
                st.dataframe(evolution_table, use_container_width=True, hide_index=True)
            
            else:
                st.warning(f"Only one year of data available for {selected_player['short_name']}")
    else:
        st.info("No players found. Try adjusting your search filters.")

if __name__ == "__main__":
    main()
