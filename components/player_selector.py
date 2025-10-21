"""
Player selector component
Reusable component for searching and selecting players
"""

import streamlit as st
import pandas as pd

def player_search_selector(df, key_suffix="", year_filter=True, position_filter=True):
    """
    Create a player search and filter widget
    
    Args:
        df: DataFrame with player data
        key_suffix: Unique suffix for widget keys
        year_filter: Whether to show year filter
        position_filter: Whether to show position filter
    
    Returns:
        Filtered DataFrame based on user selections
    """
    filtered_df = df.copy()
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Search by player name
        search_term = st.text_input(
            "Search Player",
            placeholder="Enter player name...",
            key=f"player_search_{key_suffix}"
        )
        
        if search_term:
            filtered_df = filtered_df[
                filtered_df['short_name'].str.contains(search_term, case=False, na=False) |
                filtered_df['long_name'].str.contains(search_term, case=False, na=False)
            ]
    
    with col2:
        if year_filter:
            years = ['All'] + sorted(df['year'].unique().tolist(), reverse=True)
            selected_year = st.selectbox(
                "Year",
                years,
                key=f"year_filter_{key_suffix}"
            )
            
            if selected_year != 'All':
                filtered_df = filtered_df[filtered_df['year'] == selected_year]
    
    with col3:
        if position_filter:
            positions = ['All', 'Goalkeeper', 'Defender', 'Midfielder', 'Forward']
            selected_position = st.selectbox(
                "Position",
                positions,
                key=f"position_filter_{key_suffix}"
            )
            
            if selected_position != 'All':
                filtered_df = filtered_df[filtered_df['position_category'] == selected_position]
    
    return filtered_df

def player_dropdown_selector(df, label="Select Player", key_suffix="", default_index=0):
    """
    Create a dropdown to select a specific player
    
    Args:
        df: DataFrame with player data
        label: Label for the dropdown
        key_suffix: Unique suffix for widget key
        default_index: Default selected index
    
    Returns:
        Selected player row as Series or None
    """
    if len(df) == 0:
        st.warning("No players found with current filters")
        return None
    
    # Create display names (name - team - year)
    display_options = df.apply(
        lambda row: f"{row['short_name']} - {row.get('club_name', 'Unknown')} ({int(row['year'])})",
        axis=1
    ).tolist()
    
    # Add overall rating to display
    display_options_with_rating = [
        f"{opt} - OVR: {int(df.iloc[i]['overall'])}"
        for i, opt in enumerate(display_options)
    ]
    
    selected_index = st.selectbox(
        label,
        range(len(display_options_with_rating)),
        format_func=lambda x: display_options_with_rating[x],
        index=default_index if default_index < len(df) else 0,
        key=f"player_dropdown_{key_suffix}"
    )
    
    return df.iloc[selected_index]
