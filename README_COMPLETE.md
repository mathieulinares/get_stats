# get_stats

This repository contains a Python script to collect and store the statistics (traffic) of the GitHub repository: `scanberg/viamd/`

## Features

The script collects the following information:
- Daily number of clones
- Daily unique clones  
- Daily page views
- Daily unique visitors

Data is scraped daily and stored in a local SQLite database. A plot is generated and displayed in this README.

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/mathieulinares/get_stats.git
   cd get_stats
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Set up a GitHub token for higher API rate limits:
   ```bash
   export GITHUB_TOKEN=your_github_token_here
   ```

## Usage

### Manual execution
Run the complete workflow (collect stats, generate plot, update README):
```bash
python run_stats.py
```

### Individual components
- Collect stats only: `python get_stats.py`
- Generate sample data for testing: `python generate_sample_data.py`
- Update README with existing plot: `python update_readme.py`

### Automated execution
The repository includes a GitHub Actions workflow (`.github/workflows/update-stats.yml`) that:
- Runs daily at 06:00 UTC
- Collects fresh statistics
- Updates the plot and README
- Commits changes back to the repository

## Files

- `get_stats.py` - Main statistics collection script
- `update_readme.py` - README update utility
- `run_stats.py` - Complete workflow script
- `generate_sample_data.py` - Sample data generator for testing
- `requirements.txt` - Python dependencies
- `stats.db` - SQLite database storing historical data
- `stats_plot.png` - Generated statistics plot

## API Access

The script uses the GitHub API to collect repository traffic data. Note that:
- Traffic statistics require repository owner permissions or appropriate GitHub token
- Without a token, you'll get 403 errors when accessing private repository stats
- The sample data generator can be used for testing and demonstration

## Latest Statistics

![Repository Statistics](stats_plot.png)

*Last updated: 2025-09-10 16:20:21 UTC*

The plot above shows the daily traffic statistics for the scanberg/viamd repository, including:
- Total and unique clone counts
- Total page views and unique visitors

Data is collected daily using the GitHub API and stored in a local SQLite database.