"""
Club Analysis Page
Analyze club statistics, squad composition, and visualize best 11 in formation
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path
import numpy as np

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_fifa_data

st.set_page_config(page_title="Club Analysis", page_icon="🏟️", layout="wide")

# Custom CSS for football field and club styling
st.markdown("""
    <style>
    .club-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        text-align: center;
    }
    .team-rating {
        font-size: 4rem;
        font-weight: bold;
        color: #FFD700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .player-card-field {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        padding: 8px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        border: 2px solid #1e3c72;
    }
    .player-name {
        font-size: 0.9rem;
        font-weight: bold;
        color: #1e3c72;
        margin: 2px 0;
    }
    .player-rating {
        font-size: 1.2rem;
        font-weight: bold;
        color: #FFD700;
        background: #1e3c72;
        border-radius: 5px;
        padding: 2px 8px;
    }
    .position-label {
        font-size: 0.7rem;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

def get_best_11_formation(club_df, formation="4-3-3"):
    """
    Get the best 11 players for a club in specified formation
    
    Args:
        club_df: DataFrame with club players
        formation: Formation string (default "4-3-3")
    
    Returns:
        Dictionary with positions as keys and player data as values
    """
    # Define position mappings for 4-3-3
    position_requirements = {
        'GK': 1,
        'LB': 1,
        'CB': 2,
        'RB': 1,
        'CM': 3,
        'LW': 1,
        'ST': 1,
        'RW': 1
    }
    
    # Position categories for each requirement
    position_mappings = {
        'GK': ['GK'],
        'LB': ['LB', 'LWB'],
        'CB': ['CB'],
        'RB': ['RB', 'RWB'],
        'CM': ['CM', 'CDM', 'CAM'],
        'LW': ['LW', 'LM'],
        'ST': ['ST', 'CF'],
        'RW': ['RW', 'RM']
    }
    
    best_11 = {}
    used_player_ids = set()
    
    # For each position requirement
    for pos, count in position_requirements.items():
        players_in_position = []
        
        # Get all possible position codes for this role
        possible_positions = position_mappings[pos]
        
        # Filter players who can play this position
        for _, player in club_df.iterrows():
            if player['sofifa_id'] in used_player_ids:
                continue
                
            player_positions = str(player.get('player_positions', '')).upper()
            
            # Check if player can play in any of the possible positions
            if any(pos_code in player_positions for pos_code in possible_positions):
                players_in_position.append(player)
        
        # Sort by overall rating and get the best ones
        players_in_position_df = pd.DataFrame(players_in_position)
        if len(players_in_position_df) > 0:
            players_in_position_df = players_in_position_df.sort_values('overall', ascending=False)
            
            # Get required number of players for this position
            selected = players_in_position_df.head(count)
            
            # Store players for this position
            if count == 1:
                if len(selected) > 0:
                    best_11[pos] = selected.iloc[0].to_dict()
                    used_player_ids.add(selected.iloc[0]['sofifa_id'])
                else:
                    best_11[pos] = None
            else:
                # Multiple players needed (like CB or CM)
                best_11[pos] = []
                for idx, player in selected.iterrows():
                    best_11[pos].append(player.to_dict())
                    used_player_ids.add(player['sofifa_id'])
    
    return best_11

def calculate_team_rating(best_11):
    """
    Calculate overall team rating based on the best 11 players
    """
    ratings = []
    
    for pos, player_data in best_11.items():
        if player_data is None:
            continue
        
        if isinstance(player_data, list):
            for player in player_data:
                if player:
                    ratings.append(player['overall'])
        else:
            ratings.append(player_data['overall'])
    
    if ratings:
        return round(np.mean(ratings), 1)
    return 0

def create_football_field_formation(best_11):
    """
    Create a visual football field with players positioned in 4-3-3 formation
    """
    fig = go.Figure()
    
    # Draw field background
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=100, y1=100,
        fillcolor="#2d5016",
        line=dict(color="white", width=3)
    )
    
    # Draw center circle
    fig.add_shape(
        type="circle",
        x0=45, y0=45, x1=55, y1=55,
        line=dict(color="white", width=2),
        fillcolor="rgba(0,0,0,0)"
    )
    
    # Draw center line
    fig.add_shape(
        type="line",
        x0=0, y0=50, x1=100, y1=50,
        line=dict(color="white", width=2)
    )
    
    # Draw penalty boxes
    fig.add_shape(type="rect", x0=0, y0=30, x1=15, y1=70, 
                  line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)")
    fig.add_shape(type="rect", x0=85, y0=30, x1=100, y1=70,
                  line=dict(color="white", width=2), fillcolor="rgba(0,0,0,0)")
    
    # Position coordinates for 4-3-3 formation (x, y)
    positions = {
        'GK': (8, 50),
        'LB': (25, 15),
        'CB': [(25, 40), (25, 60)],  # Two center backs
        'RB': (25, 85),
        'CM': [(50, 30), (50, 50), (50, 70)],  # Three midfielders
        'LW': (75, 15),
        'ST': (75, 50),
        'RW': (75, 85)
    }
    
    # Add players to field
    for pos, coords in positions.items():
        player_data = best_11.get(pos)
        
        if isinstance(coords, list):
            # Multiple players (CB or CM)
            if isinstance(player_data, list):
                for i, coord in enumerate(coords):
                    if i < len(player_data) and player_data[i]:
                        player = player_data[i]
                        x, y = coord
                        
                        # Add player marker
                        fig.add_trace(go.Scatter(
                            x=[x], y=[y],
                            mode='markers+text',
                            marker=dict(size=40, color='#1e3c72', 
                                       line=dict(color='white', width=3)),
                            text=f"{player['short_name']}<br>{int(player['overall'])}",
                            textposition="middle center",
                            textfont=dict(color='white', size=10, family='Arial Black'),
                            hovertemplate=f"<b>{player['short_name']}</b><br>" +
                                        f"Position: {pos}<br>" +
                                        f"Overall: {int(player['overall'])}<br>" +
                                        f"Age: {int(player.get('age', 0))}<extra></extra>",
                            showlegend=False
                        ))
        else:
            # Single player
            if player_data:
                x, y = coords
                
                # Add player marker
                fig.add_trace(go.Scatter(
                    x=[x], y=[y],
                    mode='markers+text',
                    marker=dict(size=40, color='#1e3c72',
                               line=dict(color='white', width=3)),
                    text=f"{player_data['short_name']}<br>{int(player_data['overall'])}",
                    textposition="middle center",
                    textfont=dict(color='white', size=10, family='Arial Black'),
                    hovertemplate=f"<b>{player_data['short_name']}</b><br>" +
                                f"Position: {pos}<br>" +
                                f"Overall: {int(player_data['overall'])}<br>" +
                                f"Age: {int(player_data.get('age', 0))}<extra></extra>",
                    showlegend=False
                ))
    
    # Update layout
    fig.update_layout(
        title="Best 11 - 4-3-3 Formation",
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-5, 105]),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-5, 105]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=600,
        hovermode='closest',
        font=dict(color='white')
    )
    
    return fig

def create_squad_depth_chart(club_df):
    """
    Create a bar chart showing squad depth by position
    """
    # Count players by position category
    position_counts = club_df['position_category'].value_counts()
    
    fig = go.Figure(data=[
        go.Bar(
            x=position_counts.index,
            y=position_counts.values,
            marker=dict(
                color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'],
                line=dict(color='white', width=2)
            ),
            text=position_counts.values,
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Squad Depth by Position",
        xaxis_title="Position Category",
        yaxis_title="Number of Players",
        height=400,
        showlegend=False
    )
    
    return fig

def create_age_distribution(club_df):
    """
    Create age distribution histogram
    """
    fig = px.histogram(
        club_df,
        x='age',
        nbins=20,
        title="Squad Age Distribution",
        labels={'age': 'Age', 'count': 'Number of Players'},
        color_discrete_sequence=['#1e3c72']
    )
    
    # Add average age line
    avg_age = club_df['age'].mean()
    fig.add_vline(
        x=avg_age,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Avg: {avg_age:.1f}",
        annotation_position="top"
    )
    
    fig.update_layout(height=400, showlegend=False)
    
    return fig

def create_value_vs_rating_scatter(club_df):
    """
    Create scatter plot of player value vs overall rating
    """
    # Filter out players with zero value
    club_df_filtered = club_df[club_df['value_eur'] > 0].copy()
    
    fig = px.scatter(
        club_df_filtered,
        x='overall',
        y='value_eur',
        size='age',
        color='position_category',
        hover_name='short_name',
        title="Player Value vs Overall Rating",
        labels={'overall': 'Overall Rating', 'value_eur': 'Market Value (€)'},
        color_discrete_map={
            'Goalkeeper': '#FF6B6B',
            'Defender': '#4ECDC4',
            'Midfielder': '#45B7D1',
            'Forward': '#FFA07A'
        }
    )
    
    fig.update_layout(height=500)
    
    return fig

def create_top_players_table(club_df, top_n=15):
    """
    Create a formatted table of top players
    """
    # Select top players by overall rating
    top_players = club_df.nlargest(top_n, 'overall')[
        ['short_name', 'overall', 'potential', 'age', 'player_positions', 'value_eur', 'wage_eur']
    ].copy()
    
    # Format currency columns
    top_players['value_eur'] = top_players['value_eur'].apply(lambda x: f"€{x:,.0f}" if pd.notna(x) else "N/A")
    top_players['wage_eur'] = top_players['wage_eur'].apply(lambda x: f"€{x:,.0f}" if pd.notna(x) else "N/A")
    
    # Rename columns
    top_players.columns = ['Player', 'Overall', 'Potential', 'Age', 'Positions', 'Value', 'Wage']
    
    return top_players

def create_potential_vs_actual(club_df):
    """
    Create chart showing players with most growth potential
    """
    # Calculate potential gap
    club_df = club_df.copy()
    club_df['potential_gap'] = club_df['potential'] - club_df['overall']
    
    # Get top 10 players with most potential
    top_potential = club_df.nlargest(10, 'potential_gap')[
        ['short_name', 'overall', 'potential', 'potential_gap', 'age']
    ].sort_values('potential_gap', ascending=True)
    
    fig = go.Figure()
    
    # Add actual overall bars
    fig.add_trace(go.Bar(
        y=top_potential['short_name'],
        x=top_potential['overall'],
        name='Current Overall',
        orientation='h',
        marker=dict(color='#4ECDC4')
    ))
    
    # Add potential gap bars
    fig.add_trace(go.Bar(
        y=top_potential['short_name'],
        x=top_potential['potential_gap'],
        name='Growth Potential',
        orientation='h',
        marker=dict(color='#FFA07A')
    ))
    
    fig.update_layout(
        title="Players with Highest Growth Potential",
        xaxis_title="Rating",
        yaxis_title="Player",
        barmode='stack',
        height=450
    )
    
    return fig

def main():
    st.title("🏟️ Club Analysis - Squad Overview")
    
    # Load data
    with st.spinner("Loading FIFA data..."):
        df = load_fifa_data()
    
    if df is None:
        st.error("Failed to load data. Please check the data file.")
        return
    
    st.markdown("""
    Analyze club squads, visualize the best 11 in formation, and explore team statistics.
    """)
    
    # Year and club selection
    col1, col2 = st.columns([1, 2])
    
    with col1:
        available_years = sorted(df['year'].unique(), reverse=True)
        selected_year = st.selectbox("Select Year", available_years, index=0)
    
    # Filter by year
    df_year = df[df['year'] == selected_year].copy()
    
    with col2:
        # Get clubs with player counts
        club_counts = df_year['club_name'].value_counts()
        clubs_with_counts = [f"{club} ({count} players)" for club, count in club_counts.items()]
        
        selected_club_display = st.selectbox(
            "Select Club",
            clubs_with_counts,
            help="Choose a club to analyze"
        )
        
        # Extract club name
        selected_club = selected_club_display.split(" (")[0]
    
    # Filter club data
    club_df = df_year[df_year['club_name'] == selected_club].copy()
    
    if len(club_df) == 0:
        st.warning(f"No data found for {selected_club} in {selected_year}")
        return
    
    # Get best 11 in 4-3-3 formation
    best_11 = get_best_11_formation(club_df)
    team_rating = calculate_team_rating(best_11)
    
    # Club header with team rating
    st.markdown(f"""
        <div class="club-header">
            <h1>🏆 {selected_club}</h1>
            <p style="font-size: 1.2rem; margin: 10px 0;">Season {selected_year}</p>
            <div class="team-rating">{team_rating}</div>
            <p style="font-size: 0.9rem; margin-top: 5px;">Team Rating (Best 11)</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Squad Size", len(club_df))
    
    with col2:
        avg_overall = club_df['overall'].mean()
        st.metric("Avg Overall", f"{avg_overall:.1f}")
    
    with col3:
        avg_age = club_df['age'].mean()
        st.metric("Avg Age", f"{avg_age:.1f}")
    
    with col4:
        total_value = club_df['value_eur'].sum()
        st.metric("Total Value", f"€{total_value/1_000_000:.1f}M")
    
    with col5:
        top_player = club_df.nlargest(1, 'overall').iloc[0]
        st.metric("Top Player", f"{top_player['short_name']} ({int(top_player['overall'])})")
    
    # Football field with formation
    st.markdown("---")
    st.subheader("⚽ Best 11 in 4-3-3 Formation")
    
    field_fig = create_football_field_formation(best_11)
    st.plotly_chart(field_fig, use_container_width=True)
    
    # Formation breakdown
    with st.expander("📋 Starting XI Details"):
        cols = st.columns(3)
        col_idx = 0
        
        for pos, player_data in best_11.items():
            if isinstance(player_data, list):
                for i, player in enumerate(player_data):
                    if player:
                        with cols[col_idx % 3]:
                            st.markdown(f"""
                            **{pos} - {player['short_name']}**  
                            Overall: {int(player['overall'])} | Age: {int(player.get('age', 0))}  
                            Value: €{player.get('value_eur', 0):,.0f}
                            """)
                        col_idx += 1
            elif player_data:
                with cols[col_idx % 3]:
                    st.markdown(f"""
                    **{pos} - {player_data['short_name']}**  
                    Overall: {int(player_data['overall'])} | Age: {int(player_data.get('age', 0))}  
                    Value: €{player_data.get('value_eur', 0):,.0f}
                    """)
                col_idx += 1
    
    # Squad analysis visualizations
    st.markdown("---")
    st.subheader("📊 Squad Analysis")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Squad Depth", "Age & Value", "Top Players", "Potential"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            depth_fig = create_squad_depth_chart(club_df)
            st.plotly_chart(depth_fig, use_container_width=True)
        
        with col2:
            age_fig = create_age_distribution(club_df)
            st.plotly_chart(age_fig, use_container_width=True)
    
    with tab2:
        value_fig = create_value_vs_rating_scatter(club_df)
        st.plotly_chart(value_fig, use_container_width=True)
        
        st.info("""
        **Bubble size** represents player age. Larger bubbles = older players.  
        This helps identify value-for-money signings and overvalued players.
        """)
    
    with tab3:
        st.markdown("### Top 15 Players by Overall Rating")
        top_players_table = create_top_players_table(club_df, top_n=15)
        st.dataframe(top_players_table, use_container_width=True, hide_index=True)
    
    with tab4:
        potential_fig = create_potential_vs_actual(club_df)
        st.plotly_chart(potential_fig, use_container_width=True)
        
        st.info("""
        **Growth Potential** shows the gap between current overall and potential rating.  
        These players have the most room for improvement and could be future stars!
        """)
    
    # Squad statistics summary
    st.markdown("---")
    st.subheader("📈 Squad Statistics Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Position Distribution")
        position_dist = club_df['position_category'].value_counts()
        for pos, count in position_dist.items():
            percentage = (count / len(club_df)) * 100
            st.write(f"**{pos}**: {count} players ({percentage:.1f}%)")
    
    with col2:
        st.markdown("### Age Groups")
        young = len(club_df[club_df['age'] < 23])
        prime = len(club_df[(club_df['age'] >= 23) & (club_df['age'] <= 29)])
        veteran = len(club_df[club_df['age'] > 29])
        
        st.write(f"**Young (< 23)**: {young} players ({young/len(club_df)*100:.1f}%)")
        st.write(f"**Prime (23-29)**: {prime} players ({prime/len(club_df)*100:.1f}%)")
        st.write(f"**Veteran (> 29)**: {veteran} players ({veteran/len(club_df)*100:.1f}%)")

if __name__ == "__main__":
    main()
