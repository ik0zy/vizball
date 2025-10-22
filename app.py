"""
FIFA Player Stats Dashboard
A comprehensive Streamlit dashboard for analyzing FIFA player statistics from 2015-2022
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="FIFA Player Stats Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    h1 {
        color: #1f77b4;
    }
    .football-field {
        background-color: #2d5016;
        border: 2px solid white;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Sidebar
    with st.sidebar:
        st.title("FIFA Dashboard")
        st.markdown("---")
        st.markdown("""
        ### About
        This interactive dashboard analyzes FIFA player statistics from 2015 to 2022.
        
        ### Features
        - **Home**: Overview and top players
        - **Player Analysis**: Track stats over time and analyze career progression
        
        ### Data
        Data from FIFA video game series (2015-2022)
        """)
    
    # Main content
    st.title("FIFA Player Stats Dashboard")
    st.markdown("### Welcome to the FIFA Scouting Dashboard")
    
    st.info("""
    This dashboard provides comprehensive analysis of FIFA player statistics from 2015 to 2022.
    Navigate to the Player Analysis page to explore detailed player career progressions.
    """)
    
    # Quick stats
    st.markdown("## Quick Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Years of Data", "2015-2022", "8 years")
    with col2:
        st.metric("Players Tracked", "17,000+", "Across all years")
    with col3:
        st.metric("Attributes", "40+", "Per player")
    with col4:
        st.metric("Teams", "700+", "Worldwide")
    
    # Getting started guide
    st.markdown("## Getting Started")
    
    st.markdown("""
    ### How to use this dashboard:
    
    **Player Analysis**
    - Track how player stats changed over years (2015-2022)
    - See career progression with position-specific attributes
    - View detailed attribute history and percentile comparisons
    - Analyze overall vs potential ratings over time
    - Review year-by-year breakdowns
    - Explore interactive attribute heatmaps
    """)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Navigate using the sidebar to explore different visualizations</p>
        <p><em>Data source: FIFA video game series (2015-2022)</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
