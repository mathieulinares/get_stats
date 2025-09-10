#!/usr/bin/env python3
"""
Sample data generator for testing the get_stats functionality.

This script generates sample data to demonstrate the functionality
when GitHub API access is not available.
"""

import sqlite3
import random
from datetime import datetime, timedelta
from get_stats import GitHubStatsCollector

def generate_sample_data(days=30):
    """Generate sample statistics data for testing."""
    collector = GitHubStatsCollector()
    
    # Generate data for the last N days
    end_date = datetime.now()
    
    for i in range(days):
        current_date = end_date - timedelta(days=i)
        date_str = current_date.strftime('%Y-%m-%d')
        
        # Generate realistic sample data with some variation
        base_clones = 5 + random.randint(0, 15)
        base_views = 20 + random.randint(0, 80)
        
        clones = base_clones + random.randint(-2, 8)
        unique_clones = min(clones, base_clones // 2 + random.randint(0, 5))
        views = base_views + random.randint(-10, 40)
        unique_visitors = min(views, views // 3 + random.randint(0, 15))
        
        # Ensure non-negative values
        clones = max(0, clones)
        unique_clones = max(0, unique_clones)
        views = max(0, views)
        unique_visitors = max(0, unique_visitors)
        
        collector.store_stats(date_str, clones, unique_clones, views, unique_visitors)
    
    print(f"Generated sample data for {days} days")
    
    # Generate plot with sample data
    collector.generate_plot()
    print("Sample plot generated: stats_plot.png")

if __name__ == "__main__":
    generate_sample_data()