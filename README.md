# ⚽ FIFA Player Stats Dashboard

A comprehensive Streamlit dashboard for analyzing FIFA player statistics from 2015 to 2022.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Features

### 📍 Field View
- Visualize players positioned on an interactive football field
- Filter by position, overall rating, and year
- See top players in each position category
- Interactive markers sized by player rating

### ⚖️ Player Comparison
- Compare two players side-by-side
- Detailed radar charts for attribute visualization
- Category-specific breakdowns (Attacking, Defending, Movement, Skills, Physical)
- Complete statistical comparison

### 📈 Scatter Analysis
- Explore relationships between different attributes
- Customizable X/Y axes with 40+ attributes
- Color coding by position, league, nationality, or any attribute
- Interactive filtering and statistical insights
- Trendline support

### 📊 Player Analysis
- Track player statistics across years (2015-2022)
- Compare potential vs actual overall rating
- Interactive attribute heatmaps with filtering
- Position-specific attribute evolution
- Year-by-year detailed breakdown

### 🏟️ Club Analysis
- Visualize best 11 players in 4-3-3 formation on a football field
- Calculate overall team rating from starting lineup
- Analyze squad depth by position category
- View age distribution and player value analysis
- Identify players with highest growth potential
- Compare top performers within the squad

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /path/to/Vizball
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # On Linux/Mac:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Ensure your FIFA dataset is in place:**
   - The dashboard expects `fifa_players_15_22_clean.csv` in the root directory
   - You can also use the individual yearly datasets in the `fifa-22-complete-player-dataset/` folder

### Running the Dashboard

```bash
# Activate venv first
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run Streamlit
streamlit run app.py
```

The dashboard will automatically open at `http://localhost:8501`

## 📊 Dataset

The dashboard uses FIFA player data from 2015 to 2022, containing:
- **17,000+** unique players
- **40+** attributes per player including:
  - Basic stats (Overall, Potential, Age, Value, Wage)
  - Physical attributes (Pace, Strength, Stamina)
  - Technical skills (Passing, Dribbling, Shooting)
  - Mental attributes (Vision, Positioning, Composure)
  - Defensive stats (Marking, Tackling, Interceptions)
  - Goalkeeper-specific attributes
