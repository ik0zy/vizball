"""
FIFA Player Stats Dashboard
A comprehensive Streamlit dashboard for analyzing FIFA player statistics from 2015-2022
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from utils.data_loader import load_fifa_data

# Page configuration
st.set_page_config(
    page_title="FIFA Player Stats Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Optimized CSS - consolidated and minified
st.markdown("""
<style>
.main{background-color:#0e1117;padding-top:2rem}
.stMetric{background-color:#1e2530!important;padding:15px!important;border-radius:8px!important;border:2px solid #ff9800!important}
.stMetric label{color:#fff!important;font-size:14px!important;font-weight:600!important}
.stMetric [data-testid="stMetricValue"]{color:#ff9800!important;font-size:28px!important;font-weight:bold!important}
.stMetric [data-testid="stMetricDelta"]{color:#4caf50!important}
h1{color:#fff!important;text-align:center;font-weight:bold;padding:20px;margin-top:20px!important;border:3px solid #ff9800;border-radius:10px;background:linear-gradient(135deg,#1e3c72 0%,#2a5298 100%)!important}
h2{color:#ff9800!important}
h3{color:#fff!important}
[data-testid="stSidebar"]{background-color:#0e1117}
[data-testid="stSidebar"] .stMarkdown{color:#fff}
.football-field{background-color:#2d5016;border:2px solid white}
.dataframe{color:#fff!important}
</style>
""", unsafe_allow_html=True)

def main():
    # Load data
    with st.spinner("Loading FIFA data..."):
        df = load_fifa_data()
    
    if df is None:
        st.error("Failed to load data. Please check the data file.")
        return
    
    # Sidebar with year selection
    with st.sidebar:
        st.markdown("---")
        
        # Year selector for landing page data
        available_years = sorted(df['year'].unique(), reverse=True)
        selected_year = st.selectbox(
            "Select Year for Overview",
            available_years,
            index=0,
            help="Choose a year to see statistics on the landing page"
        )
        
        st.markdown("---")
        st.markdown("""
        ### About
        This interactive dashboard analyzes FIFA player statistics from 2015 to 2022.
        
        ### Features
        - **Home**: Overview and top players
        - **Player Analysis**: Track stats over time and analyze career progression
        - **Club Analysis**: Visualize best 11, squad depth, and team statistics
        
        ### Data
        Data from FIFA video game series (2015-2022)
        """)
        
        # Filters Section
        st.markdown("---")
        st.header("🔍 Filters")
        st.markdown("---")
        
        # Filter data by selected year first
        df_year = df[df['year'] == selected_year].copy()
        
        # Position filter - optimized to avoid repeated split/explode
        @st.cache_data(ttl=3600)
        def get_unique_positions(_df):
            return sorted([p for p in _df['player_positions'].str.split(',').explode().str.strip().unique() if pd.notna(p)])
        
        positions = get_unique_positions(df_year)
        selected_position = st.multiselect(
            "Select Position(s)",
            options=positions,
            default=[]
        )
        
        # Overall rating filter
        min_overall, max_overall = st.slider(
            "Overall Rating Range",
            int(df_year['overall'].min()),
            int(df_year['overall'].max()),
            (int(df_year['overall'].min()), int(df_year['overall'].max()))
        )
        
        # Age filter
        min_age, max_age = st.slider(
            "Age Range",
            int(df_year['age'].min()),
            int(df_year['age'].max()),
            (int(df_year['age'].min()), int(df_year['age'].max()))
        )
        
        # Apply filters button
        apply_filters = st.button("Apply Filters")
    
    # Use filtered or unfiltered data with optimized operations
    if apply_filters:
        # Build filter mask efficiently
        mask = (df_year['overall'] >= min_overall) & (df_year['overall'] <= max_overall) & \
               (df_year['age'] >= min_age) & (df_year['age'] <= max_age)
        
        if selected_position:
            pos_pattern = '|'.join(selected_position)
            mask &= df_year['player_positions'].str.contains(pos_pattern, na=False, regex=True)
        
        df_year = df_year[mask]
        st.sidebar.success(f"✓ Filtered: {len(df_year):,} players")
    else:
        # Filter data by selected year
        df_year = df[df['year'] == selected_year].copy()
    
    # Main content - Title
    st.markdown(f"<h1>⚽ FIFA {selected_year} Players Analysis</h1>", unsafe_allow_html=True)
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_value = df_year['value_eur'].mean() / 1_000_000
        st.metric("Average Value", f"€{avg_value:.2f}M")
    
    with col2:
        avg_wage = df_year['wage_eur'].mean() / 1_000
        st.metric("Average Wage", f"€{avg_wage:.2f}K")
    
    with col3:
        top_player_value = df_year.nlargest(1, 'value_eur').iloc[0]
        st.metric("Top Player By Value", top_player_value['short_name'])
        st.caption(f"Value: €{top_player_value['value_eur']/1_000_000:.0f}M")
    
    with col4:
        top_player_wage = df_year.nlargest(1, 'wage_eur').iloc[0]
        st.metric("Top Player By Wage", top_player_wage['short_name'])
        st.caption(f"Wage: €{top_player_wage['wage_eur']/1_000:.0f}K")
    
    st.markdown("---")
    
    # Second metrics row
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        max_value = df_year['value_eur'].max() / 1_000_000
        st.metric("Max Value", f"€{max_value:.0f}M")
    
    with col6:
        max_wage = df_year['wage_eur'].max() / 1_000
        st.metric("Max Wage", f"€{max_wage:.0f}K")
    
    with col7:
        right_foot = len(df_year[df_year['preferred_foot'] == 'Right'])
        st.metric("Right Footed", f"{right_foot:,}")
    
    with col8:
        left_foot = len(df_year[df_year['preferred_foot'] == 'Left'])
        st.metric("Left Footed", f"{left_foot:,}")
    
    st.markdown("---")
    
    # Main content area
    row1_col1, row1_col2 = st.columns([1, 2])
    
    # Top Clubs by Value - optimized aggregation
    with row1_col1:
        st.subheader("Top 20 Clubs by Value")
        club_value = df_year.groupby('club_name', observed=True)['value_eur'].sum().nlargest(20).sort_values(ascending=True)
        club_value_df = pd.DataFrame({
            'Club': club_value.index,
            'Value': club_value.values / 1_000_000  # Convert to millions
        })
        
        fig_clubs = px.bar(
            club_value_df,
            y='Club',
            x='Value',
            orientation='h',
            title=f'Top 20 Clubs by Total Value ({selected_year})',
            labels={'Value': 'Value (Millions €)', 'Club': ''},
            color='Value',
            color_continuous_scale='Viridis'
        )
        fig_clubs.update_layout(
            height=600,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig_clubs, use_container_width=True, config={'displayModeBar': False})
    
    # Distribution charts
    with row1_col2:
        col_hist1, col_hist2 = st.columns(2)
        
        with col_hist1:
            st.subheader("Overall Rating Distribution")
            fig_overall = px.histogram(
                df_year,
                x='overall',
                nbins=30,
                title='Overall Rating Distribution',
                labels={'overall': 'Overall Rating', 'count': 'Players'},
                color_discrete_sequence=['#1f77b4']
            )
            fig_overall.update_layout(
                height=300,
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            # Use config to disable unnecessary features for better performance
            st.plotly_chart(fig_overall, use_container_width=True, config={'displayModeBar': False})
        
        with col_hist2:
            st.subheader("Potential Distribution")
            fig_potential = px.histogram(
                df_year,
                x='potential',
                nbins=30,
                title='Potential Rating Distribution',
                labels={'potential': 'Potential', 'count': 'Players'},
                color_discrete_sequence=['#1f77b4']
            )
            fig_potential.update_layout(
                height=300,
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_potential, use_container_width=True, config={'displayModeBar': False})
        
        # Preferred Foot
        st.subheader("Players by Preferred Foot")
        foot_counts = df_year['preferred_foot'].value_counts()
        fig_foot = px.bar(
            x=foot_counts.index,
            y=foot_counts.values,
            title='Distribution by Preferred Foot',
            labels={'x': 'Preferred Foot', 'y': 'Number of Players'},
            color=foot_counts.index,
            color_discrete_map={'Right': '#1f77b4', 'Left': '#ff9800'}
        )
        fig_foot.update_layout(
            height=300,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig_foot, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    
    # Row 2: Age Distribution and Position Categories
    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        st.subheader("Players Distribution by Age")
        df_year['age_group'] = pd.cut(df_year['age'], bins=[16, 20, 25, 30, 35, 50], 
                                  labels=['16-20', '21-25', '26-30', '31-35', '36+'])
        age_counts = df_year.groupby('age_group').size().reset_index(name='count')
        
        fig_age = px.treemap(
            age_counts,
            path=['age_group'],
            values='count',
            title='Players by Age Groups',
            color='count',
            color_continuous_scale='RdYlGn'
        )
        fig_age.update_layout(
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        fig_age.update_traces(textinfo="label+value+percent parent")
        st.plotly_chart(fig_age, use_container_width=True, config={'displayModeBar': False})
    
    with row2_col2:
        st.subheader("Players Distribution by Nationality")
        nationality_counts = df_year['nationality_name'].value_counts().reset_index()
        nationality_counts.columns = ['country', 'count']
        
        # Map country names to ISO codes for plotly
        fig_map = px.choropleth(
            nationality_counts.head(50),
            locations='country',
            locationmode='country names',
            color='count',
            hover_name='country',
            hover_data={'count': True},
            title='Top 50 Countries by Player Count',
            color_continuous_scale='Blues',
            labels={'count': 'Number of Players'}
        )
        fig_map.update_layout(
            height=500,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='natural earth',
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    
    # Additional Statistics Section
    st.header("📊 Additional Statistics")
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.subheader("Top 10 Leagues by Players")
        league_counts = df_year['league_name'].value_counts().sort_values(ascending=True).tail(10)
        fig_leagues = px.bar(
            x=league_counts.values,
            y=league_counts.index,
            orientation='h',
            labels={'x': 'Number of Players', 'y': 'League'},
            color=league_counts.values,
            color_continuous_scale='Bluered'
        )
        fig_leagues.update_layout(
            height=500,
            showlegend=False,
            coloraxis_showscale=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=20, r=20, t=40, b=40)
        )
        st.plotly_chart(fig_leagues, use_container_width=True, config={'displayModeBar': False})
    
    with col_stat2:
        st.subheader("Work Rate Distribution")
        if 'work_rate' in df_year.columns:
            work_rate_counts = df_year['work_rate'].value_counts().head(10)
            fig_workrate = px.pie(
                values=work_rate_counts.values,
                names=work_rate_counts.index,
                title='Top 10 Work Rate Patterns',
                hole=0.4
            )
            fig_workrate.update_layout(
                height=600,
                showlegend=True,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                margin=dict(l=60, r=20, t=60, b=40)
            )
            st.plotly_chart(fig_workrate, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Work rate data not available for this year")
    
    with col_stat3:
        st.subheader("Body Type Distribution")
        if 'body_type' in df_year.columns:
            body_type_counts = df_year['body_type'].value_counts().head(10)
            fig_body = px.bar(
                x=body_type_counts.index,
                y=body_type_counts.values,
                labels={'x': 'Body Type', 'y': 'Number of Players'},
                color=body_type_counts.values,
                color_continuous_scale='Sunset'
            )
            fig_body.update_layout(
                height=500,
                showlegend=False,
                coloraxis_showscale=False,
                xaxis_tickangle=-45,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                margin=dict(l=20, r=20, t=40, b=80)
            )
            st.plotly_chart(fig_body, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Body type data not available for this year")
    
    st.markdown("---")
    
    # Top Players Table
    st.subheader(f"🌟 Top 20 Players by Overall Rating ({selected_year})")
    top_players = df_year.nlargest(20, 'overall')[
        ['short_name', 'overall', 'potential', 'age', 'club_name', 'nationality_name', 'value_eur', 'player_positions']
    ].copy()
    top_players['value_eur'] = top_players['value_eur'].apply(lambda x: f"€{x/1_000_000:.1f}M" if pd.notna(x) else "N/A")
    top_players.columns = ['Player', 'Overall', 'Potential', 'Age', 'Club', 'Nationality', 'Value', 'Positions']
    st.dataframe(top_players, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Filtered Player Data (shown if filters applied)
    if apply_filters:
        st.subheader("📋 Filtered Player Data")
        st.info(f"Showing top 50 players from {len(df_year):,} filtered results")
        
        filtered_display = df_year.nlargest(50, 'overall')[
            ['short_name', 'overall', 'potential', 'age', 'club_name', 'nationality_name', 'value_eur', 'wage_eur', 'player_positions']
        ].copy()
        
        # Format currency columns
        filtered_display['value_eur'] = filtered_display['value_eur'].apply(
            lambda x: f"€{x/1_000_000:.1f}M" if pd.notna(x) and x > 0 else "N/A"
        )
        filtered_display['wage_eur'] = filtered_display['wage_eur'].apply(
            lambda x: f"€{x/1_000:.1f}K" if pd.notna(x) and x > 0 else "N/A"
        )
        
        filtered_display.columns = ['Player', 'Overall', 'Potential', 'Age', 'Club', 'Nationality', 'Value', 'Wage', 'Positions']
        st.dataframe(filtered_display, use_container_width=True, hide_index=True)
        
        st.markdown("---")
    
    # Footer
    st.markdown("---")
    st.markdown(
        f"""
        <div style='text-align: center; color: gray; padding: 20px;'>
            <p>⚽ FIFA Player Stats Dashboard | Data from FIFA {selected_year}</p>
            <p>Navigate using the sidebar to explore Player Analysis and Club Analysis pages</p>
            <p>Total Players in {selected_year}: {len(df_year):,} | All Years (2015-2022): {len(df):,}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
