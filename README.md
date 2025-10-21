# ⚽ FIFA Player Stats Dashboard

A comprehensive Streamlit dashboard for analyzing FIFA player statistics from 2015 to 2022, inspired by the [FIFA Dashboard](https://wimmerth.github.io/fifa-dashboard) project.

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

### 📉 Player Evolution
- Track player statistics across years (2015-2022)
- Compare potential vs actual overall rating
- Multi-player career comparison
- Year-by-year detailed breakdown

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

## 🎨 Using GitHub Copilot for Development

This project was developed with GitHub Copilot assistance. Here's how to leverage Copilot effectively:

### Best Practices with Copilot:

1. **Start with Clear Structure:**
   - Define your project structure first (pages, components, utils)
   - Use descriptive file and function names
   - Copilot will suggest better code with clear context

2. **Use Comments as Prompts:**
   ```python
   # Create a radar chart comparing two players across main attributes
   def create_radar_chart(player1, player2, attributes, labels):
       # Copilot will suggest the implementation
   ```

3. **Leverage Copilot Chat:**
   - Ask for specific visualizations: "Create a Plotly scatter plot with hover data"
   - Request code refactoring: "Optimize this data loading function with caching"
   - Get explanations: "Explain how this filtering works"

4. **Iterate and Refine:**
   - Accept Copilot's suggestions as starting points
   - Refine the code to match your specific needs
   - Use Copilot to add error handling and edge cases

5. **Component-Based Development:**
   - Build reusable components (like `player_selector.py`)
   - Copilot excels at suggesting variations once you have a base component

### Example Workflow:

```python
# 1. Start with a function signature and docstring
def load_fifa_data():
    """
    Load the main FIFA dataset with caching for performance
    Returns: pandas DataFrame with all player data
    """
    # 2. Copilot suggests implementation
    # 3. Refine as needed
```

## 📁 Project Structure

```
Vizball/
├── app.py                          # Main dashboard entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── fifa_players_15_22_clean.csv   # Main dataset
├── utils/
│   └── data_loader.py             # Data loading and preprocessing utilities
├── components/
│   └── player_selector.py         # Reusable player selection components
└── pages/
    ├── 1_⚽_Field_View.py         # Football field visualization
    ├── 2_⚖️_Player_Comparison.py  # Player comparison with radar charts
    ├── 3_📈_Scatter_Analysis.py   # Multi-attribute scatter plots
    └── 4_📉_Player_Evolution.py   # Career progression tracking
```

## 🛠️ Customization

### Adding New Visualizations

1. Create a new file in the `pages/` directory:
   ```python
   # pages/5_🎯_Your_New_Page.py
   import streamlit as st
   
   st.title("Your New Visualization")
   # Add your code here
   ```

2. Streamlit automatically detects new pages in the `pages/` folder

### Modifying Filters

Edit `components/player_selector.py` to add new filter options or modify existing ones.

### Adding New Attributes

1. Update `utils/data_loader.py` in the `get_attribute_columns()` function
2. New attributes will automatically appear in dropdown menus

## 🔧 Troubleshooting

### Data Loading Issues

If you get a "Failed to load data" error:
- Ensure `fifa_players_15_22_clean.csv` is in the root directory
- Check file permissions
- Verify the CSV file is not corrupted

### Performance Issues

For large datasets:
- The scatter plot automatically samples to 5000 points
- Use the year filter to reduce data volume
- Increase Streamlit's memory limit: `streamlit run app.py --server.maxUploadSize=200`

### Import Errors

If you encounter import errors:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 📝 Future Enhancements

Potential features to add:
- [ ] Team analysis and comparison
- [ ] League-wide statistics
- [ ] Player clustering and similarity search
- [ ] Export capabilities (PDF reports, data downloads)
- [ ] Advanced statistical models (regression, prediction)
- [ ] Interactive tutorials/guided tours

## 🤝 Contributing

Feel free to:
1. Fork the repository
2. Create a new branch for your feature
3. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Inspired by [FIFA Dashboard](https://wimmerth.github.io/fifa-dashboard) by Thomas Wimmer and Haileleul Z. Haile
- FIFA data from the EA Sports FIFA video game series
- Built with Streamlit, Plotly, and Pandas

## 📧 Contact

For questions or suggestions, please open an issue in the repository.

---

**Happy Analyzing! ⚽📊**
