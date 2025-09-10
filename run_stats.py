#!/usr/bin/env python3
"""
Main script to run the complete stats collection and README update workflow.

This script:
1. Collects GitHub repository statistics
2. Generates a plot of the statistics
3. Updates the README with the plot
"""

import sys
import os
from get_stats import GitHubStatsCollector
from update_readme import update_readme_with_plot
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main workflow: collect stats, generate plot, update README."""
    try:
        # Initialize collector
        collector = GitHubStatsCollector()
        
        # Collect and store statistics
        logger.info("Starting stats collection...")
        collector.collect_and_store_stats()
        
        # Generate plot
        logger.info("Generating statistics plot...")
        plot_generated = collector.generate_plot()
        
        if plot_generated:
            # Update README with plot
            logger.info("Updating README with latest plot...")
            update_readme_with_plot()
            logger.info("Workflow completed successfully!")
        else:
            logger.warning("No plot generated - README not updated")
            return 1
            
    except Exception as e:
        logger.error(f"Error in workflow: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())