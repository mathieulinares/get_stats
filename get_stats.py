#!/usr/bin/env python3
"""
GitHub Repository Statistics Collector

This script collects and stores statistics for the scanberg/viamd repository:
- Daily number of clones
- Daily unique clones
- Daily page views  
- Daily unique visitors

Data is stored in a SQLite database and plots are generated for visualization.
"""

import os
import requests
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GitHubStatsCollector:
    def __init__(self, owner="scanberg", repo="viamd", db_path="stats.db"):
        self.owner = owner
        self.repo = repo
        self.db_path = db_path
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        
        # Initialize database
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table for storing daily statistics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_stats (
                date TEXT PRIMARY KEY,
                clones INTEGER,
                unique_clones INTEGER,
                views INTEGER,
                unique_visitors INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized: {self.db_path}")
    
    def get_headers(self):
        """Get headers for GitHub API requests."""
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'get-stats-collector'
        }
        if self.github_token:
            headers['Authorization'] = f'token {self.github_token}'
        return headers
    
    def get_clone_stats(self):
        """Get clone statistics from GitHub API."""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/traffic/clones"
        
        try:
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching clone stats: {e}")
            return None
    
    def get_view_stats(self):
        """Get view statistics from GitHub API."""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/traffic/views"
        
        try:
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching view stats: {e}")
            return None
    
    def store_stats(self, date, clones=0, unique_clones=0, views=0, unique_visitors=0):
        """Store statistics in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO daily_stats 
                (date, clones, unique_clones, views, unique_visitors)
                VALUES (?, ?, ?, ?, ?)
            ''', (date, clones, unique_clones, views, unique_visitors))
            
            conn.commit()
            logger.info(f"Stored stats for {date}: clones={clones}, unique_clones={unique_clones}, views={views}, unique_visitors={unique_visitors}")
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
        finally:
            conn.close()
    
    def collect_and_store_stats(self):
        """Collect statistics from GitHub API and store in database."""
        logger.info(f"Collecting stats for {self.owner}/{self.repo}")
        
        # Get clone statistics
        clone_data = self.get_clone_stats()
        clone_stats = {}
        if clone_data and 'clones' in clone_data:
            for entry in clone_data['clones']:
                date = entry['timestamp'][:10]  # Extract date part
                clone_stats[date] = {
                    'clones': entry['count'],
                    'unique_clones': entry['uniques']
                }
        
        # Get view statistics
        view_data = self.get_view_stats()
        view_stats = {}
        if view_data and 'views' in view_data:
            for entry in view_data['views']:
                date = entry['timestamp'][:10]  # Extract date part
                view_stats[date] = {
                    'views': entry['count'],
                    'unique_visitors': entry['uniques']
                }
        
        # Combine and store data
        all_dates = set(clone_stats.keys()) | set(view_stats.keys())
        
        for date in all_dates:
            clones = clone_stats.get(date, {}).get('clones', 0)
            unique_clones = clone_stats.get(date, {}).get('unique_clones', 0)
            views = view_stats.get(date, {}).get('views', 0)
            unique_visitors = view_stats.get(date, {}).get('unique_visitors', 0)
            
            self.store_stats(date, clones, unique_clones, views, unique_visitors)
        
        logger.info("Statistics collection completed")
    
    def get_stored_stats(self, days=30):
        """Retrieve stored statistics from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get data from the last N days
        cursor.execute('''
            SELECT date, clones, unique_clones, views, unique_visitors
            FROM daily_stats
            ORDER BY date DESC
            LIMIT ?
        ''', (days,))
        
        results = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries and reverse to chronological order
        stats = []
        for row in reversed(results):
            stats.append({
                'date': row[0],
                'clones': row[1],
                'unique_clones': row[2],
                'views': row[3],
                'unique_visitors': row[4]
            })
        
        return stats
    
    def generate_plot(self, output_path="stats_plot.png", days=30):
        """Generate plot of statistics and save to file."""
        stats = self.get_stored_stats(days)
        
        if not stats:
            logger.warning("No data available for plotting")
            return False
        
        # Prepare data for plotting
        dates = [datetime.strptime(stat['date'], '%Y-%m-%d') for stat in stats]
        clones = [stat['clones'] for stat in stats]
        unique_clones = [stat['unique_clones'] for stat in stats]
        views = [stat['views'] for stat in stats]
        unique_visitors = [stat['unique_visitors'] for stat in stats]
        
        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        fig.suptitle(f'GitHub Repository Statistics - {self.owner}/{self.repo}', fontsize=16)
        
        # Plot clones
        ax1.plot(dates, clones, 'b-', label='Total Clones', linewidth=2)
        ax1.plot(dates, unique_clones, 'b--', label='Unique Clones', linewidth=2)
        ax1.set_ylabel('Clone Count')
        ax1.set_title('Repository Clones')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot views
        ax2.plot(dates, views, 'r-', label='Total Views', linewidth=2)
        ax2.plot(dates, unique_visitors, 'r--', label='Unique Visitors', linewidth=2)
        ax2.set_ylabel('View Count')
        ax2.set_xlabel('Date')
        ax2.set_title('Repository Views')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Format x-axis
        for ax in [ax1, ax2]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//10)))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Plot saved to {output_path}")
        return True

def main():
    """Main function to collect stats and generate plot."""
    collector = GitHubStatsCollector()
    
    # Collect and store current statistics
    collector.collect_and_store_stats()
    
    # Generate plot
    collector.generate_plot()
    
    # Display some recent stats
    recent_stats = collector.get_stored_stats(7)
    if recent_stats:
        logger.info("Recent statistics (last 7 days):")
        for stat in recent_stats:
            logger.info(f"  {stat['date']}: {stat['clones']} clones ({stat['unique_clones']} unique), {stat['views']} views ({stat['unique_visitors']} unique)")

if __name__ == "__main__":
    main()