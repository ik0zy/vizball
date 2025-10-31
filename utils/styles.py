"""
Shared CSS styles for the application
"""

import streamlit as st

def apply_common_styles():
    """Apply common CSS styles across all pages"""
    st.markdown("""
        <style>
        /* Main layout */
        .main {
            background-color: #0e1117;
            padding-top: 2rem;
        }
        
        /* Metric cards */
        .stMetric {
            background-color: #1e2530 !important;
            padding: 20px !important;
            border-radius: 12px !important;
            border: 1px solid #2d3748 !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        .stMetric:hover {
            border-color: #4299e1 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 12px rgba(66, 153, 225, 0.2) !important;
        }
        .stMetric label {
            color: #a0aec0 !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        .stMetric [data-testid="stMetricValue"] {
            color: #4299e1 !important;
            font-size: 32px !important;
            font-weight: 700 !important;
        }
        .stMetric [data-testid="stMetricDelta"] {
            color: #48bb78 !important;
        }
        
        /* Headers */
        h1 {
            color: #ffffff !important;
            text-align: center;
            font-weight: 700 !important;
            padding: 30px 20px !important;
            margin: 30px 0 !important;
            border-radius: 16px !important;
            background: linear-gradient(135deg, #2c5282 0%, #2b6cb0 50%, #3182ce 100%) !important;
            box-shadow: 0 8px 16px rgba(44, 82, 130, 0.3) !important;
            font-size: 2.5rem !important;
            letter-spacing: -0.5px !important;
        }
        h2 {
            color: #4299e1 !important;
            font-weight: 700 !important;
            font-size: 1.75rem !important;
            margin: 30px 0 20px 0 !important;
            padding-bottom: 10px !important;
            border-bottom: 2px solid #2d3748 !important;
        }
        h3 {
            color: #e2e8f0 !important;
            font-weight: 600 !important;
            font-size: 1.25rem !important;
            margin: 20px 0 15px 0 !important;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #1a202c !important;
            border-right: 1px solid #2d3748 !important;
        }
        [data-testid="stSidebar"] .stMarkdown {
            color: #e2e8f0 !important;
        }
        [data-testid="stSidebar"] h3 {
            color: #4299e1 !important;
            border-bottom: 2px solid #2d3748 !important;
            padding-bottom: 10px !important;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #2c5282 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            border: none !important;
            transition: all 0.3s ease !important;
        }
        .stButton > button:hover {
            background-color: #2b6cb0 !important;
            box-shadow: 0 4px 12px rgba(44, 82, 130, 0.4) !important;
            transform: translateY(-1px) !important;
        }
        
        /* Separators */
        hr {
            margin: 40px 0 !important;
            border: none !important;
            border-top: 1px solid #2d3748 !important;
        }
        
        /* Dataframes */
        .dataframe {
            color: #e2e8f0 !important;
            background-color: #1a202c !important;
        }
        </style>
    """, unsafe_allow_html=True)


def apply_player_card_styles():
    """Apply player card specific styles"""
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
        </style>
    """, unsafe_allow_html=True)


def apply_club_styles():
    """Apply club analysis specific styles"""
    st.markdown("""
        <style>
        .club-header {
            background: linear-gradient(135deg, #2c5282 0%, #2b6cb0 100%);
            padding: 35px;
            border-radius: 20px;
            color: white;
            margin-bottom: 35px;
            text-align: center;
            box-shadow: 0 10px 20px rgba(44, 82, 130, 0.4);
        }
        .team-rating {
            font-size: 4.5rem;
            font-weight: 800;
            color: #fbbf24;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
            letter-spacing: -2px;
        }
        .player-card-field {
            background: rgba(255, 255, 255, 0.97);
            border-radius: 12px;
            padding: 10px;
            text-align: center;
            box-shadow: 0 6px 12px rgba(0,0,0,0.25);
            border: 2px solid #2c5282;
            transition: all 0.3s ease;
        }
        .player-card-field:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 16px rgba(44, 82, 130, 0.4);
        }
        .player-name {
            font-size: 0.95rem;
            font-weight: 700;
            color: #1a202c;
            margin: 4px 0;
        }
        .player-rating {
            font-size: 1.3rem;
            font-weight: 800;
            color: #ffffff;
            background: linear-gradient(135deg, #2c5282 0%, #3182ce 100%);
            border-radius: 8px;
            padding: 4px 10px;
            display: inline-block;
        }
        .position-label {
            font-size: 0.75rem;
            color: #718096;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        </style>
    """, unsafe_allow_html=True)
