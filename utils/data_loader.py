"""
Data loading utilities for FIFA player dataset
Handles loading, caching, and preprocessing of FIFA player data
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

@st.cache_data(ttl=3600)
def load_fifa_data():
    """
    Load the main FIFA dataset with caching and optimized dtypes for performance
    Returns: pandas DataFrame with all player data
    """
    try:
        # Try to load the main cleaned dataset with optimized dtypes
        data_path = Path(__file__).parent.parent / "fifa_players_15_22_clean.csv"
        
        # Define optimal dtypes for faster loading and reduced memory
        dtype_dict = {
            'sofifa_id': 'int32',
            'short_name': 'string',
            'long_name': 'string',
            'player_positions': 'category',
            'overall': 'int8',
            'potential': 'int8',
            'value_eur': 'float32',
            'wage_eur': 'float32',
            'age': 'int8',
            'height_cm': 'float32',
            'weight_kg': 'float32',
            'club_name': 'category',
            'league_name': 'category',
            'nationality_name': 'category',
            'preferred_foot': 'category',
            'work_rate': 'category',
            'body_type': 'category',
            'year': 'int16',
            'pace': 'int8',
            'shooting': 'int8',
            'passing': 'int8',
            'dribbling': 'int8',
            'defending': 'int8',
            'physic': 'int8'
        }
        
        # Load with optimized dtypes
        df = pd.read_csv(data_path, dtype=dtype_dict, low_memory=False)
        
        # Clean and preprocess
        df = preprocess_data(df)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def preprocess_data(df):
    """
    Preprocess and clean the FIFA dataset with optimized operations
    """
    # Handle missing values efficiently
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 0:
        df[numeric_columns] = df[numeric_columns].fillna(0)
    
    # Fill missing categorical values - only for object/string types
    categorical_columns = df.select_dtypes(include=['object', 'string']).columns
    if len(categorical_columns) > 0:
        df[categorical_columns] = df[categorical_columns].fillna('Unknown')
    
    # Create simplified position categories with caching
    if 'player_positions' in df.columns:
        df['position_category'] = df['player_positions'].apply(categorize_position)
        # Convert to category for better memory usage
        df['position_category'] = df['position_category'].astype('category')
    
    # Calculate age from dob if available (only if needed)
    if 'dob' in df.columns and 'year' in df.columns and 'calculated_age' not in df.columns:
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
def get_player_evolution(_df, player_id):
    """
    Get a player's stats across all years with optimized filtering
    """
    return _df[_df['sofifa_id'] == player_id].sort_values('year')

@st.cache_data
def get_image_base64_cached(image_path):
    """Cache base64 encoding of images to avoid repeated conversions"""
    import base64
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""
