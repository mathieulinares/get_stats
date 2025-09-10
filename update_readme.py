#!/usr/bin/env python3
"""
README updater script

Updates the README.md file with the latest statistics plot.
"""

import os
import base64
from datetime import datetime

def update_readme_with_plot(plot_path="stats_plot.png", readme_path="README.md"):
    """Update README.md with the generated plot."""
    
    if not os.path.exists(plot_path):
        print(f"Plot file {plot_path} not found. Please run get_stats.py first.")
        return False
    
    # Read the current README
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Create the updated content with plot
    plot_section = f"""

## Latest Statistics

![Repository Statistics](stats_plot.png)

*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*

The plot above shows the daily traffic statistics for the scanberg/viamd repository, including:
- Total and unique clone counts
- Total page views and unique visitors

Data is collected daily using the GitHub API and stored in a local SQLite database.
"""
    
    # Check if plot section already exists
    if "## Latest Statistics" in content:
        # Replace existing section
        lines = content.split('\n')
        start_idx = None
        for i, line in enumerate(lines):
            if line.startswith("## Latest Statistics"):
                start_idx = i
                break
        
        if start_idx is not None:
            # Keep content before the statistics section
            new_content = '\n'.join(lines[:start_idx]) + plot_section
        else:
            new_content = content + plot_section
    else:
        # Append to existing content
        new_content = content + plot_section
    
    # Write updated README
    with open(readme_path, 'w') as f:
        f.write(new_content)
    
    print(f"README.md updated with latest plot")
    return True

if __name__ == "__main__":
    update_readme_with_plot()