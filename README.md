# get_stats
This repo is a python script to collect and store the statistics (traffic) of this repo: scanberg/viamd/
Collected information are: Daily number of clones, daily unique clones, daily page viewed and daily unique visitors.
Data are scraped everyday and the one for the day before is added to the database. Finally, the plot is showed in the readme.

## Setup and Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Run the complete workflow: `python run_stats.py`
3. For testing with sample data: `python generate_sample_data.py`

## Files
- `get_stats.py` - Main statistics collection script
- `run_stats.py` - Complete workflow (collect stats → generate plot → update README)
- `update_readme.py` - README update utility
- `generate_sample_data.py` - Sample data generator for testing
- `.github/workflows/update-stats.yml` - GitHub Actions workflow for daily automation


## Latest Statistics

![Repository Statistics](stats_plot.png)

*Last updated: 2025-09-10 16:21:23 UTC*

The plot above shows the daily traffic statistics for the scanberg/viamd repository, including:
- Total and unique clone counts
- Total page views and unique visitors

Data is collected daily using the GitHub API and stored in a local SQLite database.
