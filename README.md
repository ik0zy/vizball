# Vizball

An interactive dashboard for analyzing FIFA player statistics from 2015 to 2022, built with Streamlit.

## Overview

Vizball provides a comprehensive platform for exploring and comparing FIFA player data across multiple seasons. The dashboard offers various visualization tools to help you understand player performance, team composition, and statistical trends over time.

## Features

### Field View

Visualize players positioned on an interactive football field. Filter by position, overall rating, and year to see top players in each position category. Player markers are sized according to their rating for quick visual comparison.

### Player Comparison

Compare two players side-by-side with detailed radar charts showing their attributes. The comparison breaks down stats into categories including attacking, defending, movement, skills, and physical attributes.

### Scatter Analysis

Explore relationships between different player attributes using customizable scatter plots. Choose from over 40 attributes for the X and Y axes, and apply color coding based on position, league, nationality, or any other attribute. The tool includes filtering options and trendline support.

### Player Analysis

Track individual player statistics across all available years. View potential versus actual overall rating, explore attribute evolution over time, and analyze position-specific performance through interactive heatmaps.

### Club Analysis

Examine team composition and strength by visualizing the best 11 players in a 4-3-3 formation. The analysis includes overall team rating calculations, squad depth by position, age distribution, player value analysis, and identification of high-potential players.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

Clone or navigate to the project directory:

```bash
cd /path/to/vizball
```

Create a virtual environment (recommended):

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

Ensure your virtual environment is activated, then run:

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`.

## Dataset

The application uses FIFA player data spanning 2015 to 2022. The dataset includes over 17,000 unique players with more than 40 attributes per player, covering basic statistics (overall rating, potential, age, value, wage), physical attributes (pace, strength, stamina), technical skills (passing, dribbling, shooting), mental attributes (vision, positioning, composure), defensive stats (marking, tackling, interceptions), and goalkeeper-specific metrics.

