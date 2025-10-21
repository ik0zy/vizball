"""
Data loading utilities for FIFA player dataset
Handles loading, caching, and preprocessing of FIFA player data
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

@st.cache_data
def load_fifa_data():
    """
    Load the main FIFA dataset with caching for performance
    Returns: pandas DataFrame with all player data
    """
    try:
        # Try to load the main cleaned dataset
        data_path = Path(__file__).parent.parent / "fifa_players_15_22_clean.csv"
        df = pd.read_csv(data_path, low_memory=False)
        
        # Clean and preprocess
        df = preprocess_data(df)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def preprocess_data(df):
    """
    Preprocess and clean the FIFA dataset
    """
    # Create a copy to avoid modifying the original
    df = df.copy()
    
    # Convert year to integer if it's not
    if 'year' in df.columns:
        df['year'] = df['year'].astype(int)
    
    # Handle missing values for key columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].fillna(0)
    
    # Fill missing categorical values
    categorical_columns = df.select_dtypes(include=['object']).columns
    df[categorical_columns] = df[categorical_columns].fillna('Unknown')
    
    # Create simplified position categories
    if 'player_positions' in df.columns:
        df['position_category'] = df['player_positions'].apply(categorize_position)
    
    # Calculate age from dob if available
    if 'dob' in df.columns and 'year' in df.columns:
        df['dob'] = pd.to_datetime(df['dob'], errors='coerce')
        df['calculated_age'] = df['year'] - df['dob'].dt.year
    
    return df

def categorize_position(position_str):
    """
    Categorize player positions into broader categories
    """
    if pd.isna(position_str) or position_str == 'Unknown':
        return 'Unknown'
    
    position_str = str(position_str).upper()
    
    # Goalkeepers
    if 'GK' in position_str:
        return 'Goalkeeper'
    
    # Defenders
    elif any(pos in position_str for pos in ['CB', 'LB', 'RB', 'RWB', 'LWB']):
        return 'Defender'
    
    # Midfielders
    elif any(pos in position_str for pos in ['CM', 'CDM', 'CAM', 'LM', 'RM']):
        return 'Midfielder'
    
    # Forwards
    elif any(pos in position_str for pos in ['ST', 'CF', 'LW', 'RW', 'LF', 'RF']):
        return 'Forward'
    
    else:
        return 'Other'

@st.cache_data
def get_player_evolution(df, player_id):
    """
    Get a player's stats across all years
    """
    return df[df['sofifa_id'] == player_id].sort_values('year')
