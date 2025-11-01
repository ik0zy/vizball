# Vizball

An interactive Streamlit toolkit for analyzing FIFA player statistics (2015–2022) with focused pages for yearwise overview, player evolution, club composition, and attribute relationships.

## Introduction

Vizball helps you explore FIFA player data across seasons with clear, interactive visualizations. It’s organized as a set of Streamlit pages you can run individually, each tackling a different question:

- Which clubs and leagues dominate a given year?
- How has a specific player evolved across seasons versus their potential?
- What’s the best XI for a club in a 4-3-3 and how strong is that lineup?
- How do two attributes (e.g., overall vs value) relate, by position or league?

The project ships with a cleaned dataset (`fifa_players_15_22_clean.csv`) and optional image downloader to display player faces offline.

## Project Structure

```
vizball/
├─ Yearwise_Analysis.py          # Year-level landing/overview page (single-entry run)
├─ download_player_images.py     # Optional: download 2022 player face images to use offline
├─ fifa_players_15_22_clean.csv  # Cleaned dataset (2015–2022)
├─ pages/                        # Streamlit pages (can be run individually)
│  ├─ Player_Analysis.py         # Player evolution, potential vs overall, position-aware insights
│  ├─ Club_Analysis.py           # Best XI (4-3-3), team rating, squad depth, value analysis
│  └─ Scatter_Analysis.py        # Customizable scatter plots with trendlines and filters
├─ components/
│  └─ player_selector.py         # Reusable player search/dropdown components
├─ utils/
│  ├─ data_loader.py             # Cached CSV loading, preprocessing, position categorization
│  └─ styles.py                  # Shared styling for a consistent dark theme
├─ player_images/                # Local cache of downloaded player face images (optional)
├─ requirements.txt              # Python dependencies
└─ README.md
```

## Methodology

### Data loading and preprocessing (`utils/data_loader.py`)
- Loads `fifa_players_15_22_clean.csv` with caching for fast page reloads.
- Cleans missing values (numeric to 0, categorical to "Unknown").
- Ensures `year` is integer; computes `calculated_age` if DOB is present.
- Derives a broad `position_category` from `player_positions` (Goalkeeper, Defender, Midfielder, Forward).

### Yearwise overview (`Yearwise_Analysis.py`)
- Sidebar-driven filters: year, positions, overall and age ranges.
- Metrics: average value/wage, top player by value/wage, max value/wage, footedness counts.
- Visuals: club value ranking, rating/potential histograms, preferred-foot distribution, age-group treemap, nationality choropleth, leagues/work-rate/body-type distributions, and a top-players table.

### Player analysis (`pages/Player_Analysis.py`)
- Search 2022 players with a reusable selector, pick one, then analyze all years for that player.
- Visuals:
	- Overall vs Potential across years (with the gap shaded).
	- Position-aware radar (different attribute sets for GKs/DEF/MID/FWD).
	- Attribute histories per stat with percentiles vs same-position peers in the selected year.
	- Evolution lines for key attributes and a year-by-year detail table.
- Optional player face rendering via locally cached images (see downloader below).

### Club analysis (`pages/Club_Analysis.py`)
- Choose a year and club, compute the best XI in a 4-3-3:
	- Role mapping (e.g., LB/LWB, CB×2, CM×3, LW/ST/RW) and selection by highest `overall` without duplicates.
	- Team rating = mean `overall` of the XI.
- Visuals:
	- A styled formation view and starting XI details.
	- Squad depth by position, age distribution, value vs overall scatter, top N players table, and potential gap (potential − overall) stacks.

### Scatter analysis (`pages/Scatter_Analysis.py`)
- Pick any numeric attributes for X/Y and color by a categorical attribute.
- Filtering by year(s), position category, minimum overall, and sample size cap.
- Adds jitter to reduce overplotting; optional linear trendline with correlation metric.
- Top-10 tables by X and Y; export the filtered data as CSV.

### Components and styling
- `components/player_selector.py`: shared search and dropdown for player selection.
- `utils/styles.py`: consistent dark theme, metric cards, headers, club/player card accents.
- Streamlit caching (`@st.cache_data`) improves responsiveness during repeated interactions.

## Results (what you can learn)

- Identify value clusters and outliers (e.g., high value at moderate overall) by league, position, or nationality.
- Track a player’s development arc, peak year, and potential gap over time.
- See a club’s strongest XI for a season, with an at-a-glance team rating and role coverage.
- Understand squad composition: depth by position, age balance, and where future potential lies.

## Conclusions

Vizball offers an extensible, page-based workflow for FIFA analytics: robust preprocessing, performant caching, and focused visualizations enable quick insights for players, clubs, and attributes. The structure encourages adding new pages or methods (e.g., new formations, clustering profiles, or transfer market simulators) without disrupting existing functionality.

Potential next steps:
- Add alternative formations and selection heuristics (chemistry, preferred foot, form).
- Extend the dataset to newer seasons and include league/team-level advanced metrics.
- Introduce model-driven insights (e.g., similarity search, role archetype clustering).
- Package a true multipage entrypoint (e.g., `Home.py`) that links all pages via Streamlit’s sidebar.

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Setup (Windows PowerShell)

```powershell
# From the project root
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
```

### Run the app (single-page entry)

You can run any page directly. Common entry points:

```powershell
# Yearwise overview (landing-style page)
streamlit run Yearwise_Analysis.py

# Player analysis
streamlit run .\pages\Player_Analysis.py

# Club analysis
streamlit run .\pages\Club_Analysis.py

# Scatter analysis
streamlit run .\pages\Scatter_Analysis.py
```

Note: This repository is organized as standalone pages. If you prefer Streamlit’s multi-page navigation, create a small `Home.py` at the project root and keep the `pages/` folder as-is.

### Optional: download player images (for richer visuals)

```powershell
python .\download_player_images.py
```

This downloads unique 2022 player face images to `player_images/` for offline use in the Player and Club pages. It uses concurrent downloads; runtime depends on your network.

## Troubleshooting

- File not found: Ensure `fifa_players_15_22_clean.csv` is in the project root.
- No player images: Run the image downloader above; missing images gracefully fall back to rating badges.
- Maps or external tiles not rendering: Some corporate/VPN networks block map assets; try a different network.
- PowerShell paths with spaces: Quote the path, e.g., `streamlit run "d:\\Git Repo\\vizball\\Yearwise_Analysis.py"`.
- Streamlit version issues: Update via `pip install --upgrade streamlit` to match `requirements.txt`.

## License and data

This repository includes a pre-cleaned CSV for educational/analytical purposes. Verify usage rights for any external data sources before redistribution. 
