# eda_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import itertools
import numpy as np
import math

# Create a figures directory if it doesn't exist
figures_dir = Path('S:/JobGrowthForecaster/analysis/figures')
figures_dir.mkdir(parents=True, exist_ok=True)

# Load the integrated dataset
data = pd.read_csv('S:/JobGrowthForecaster/data/integrated_job_growth_data.csv')

# Convert 'Date' to a datetime object and set it as the index
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Define a list of colors (you can add more colors to this list)
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

# Define a list of line styles
line_styles = ['-', '--', '-.', ':']

# Create a product of colors and line styles to get a list of combinations
line_combinations = list(itertools.product(colors, line_styles))

# Plot time series trends and save the figure
plt.figure(figsize=(15, 10))
for i, column in enumerate(data.columns):
    color, style = line_combinations[i % len(line_combinations)]
    plt.plot(data.index, data[column], label=column, color=color, linestyle=style)

plt.title('Time Series Trends')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(figures_dir / 'time_series_trends.png', bbox_inches='tight')
plt.close()

# Calculate the layout size for histograms: create enough subplots for all variables
n_cols = 4
n_rows = math.ceil(len(data.columns) / n_cols)

# Create subplots with the calculated layout size
fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(n_cols * 4, n_rows * 3))
axes = axes.flatten()  # Flatten the axes array for easy iteration

# Plot a histogram for each variable
for i, col in enumerate(data.columns):
    data[col].hist(ax=axes[i], bins=20)
    axes[i].set_title(col)

# Remove any empty subplots
for i in range(len(data.columns), len(axes)):
    fig.delaxes(axes[i])

fig.tight_layout()
plt.savefig(figures_dir / 'histograms.png')
plt.close()

# Scatter plot for potential correlations
# Due to memory and performance concerns, sample the data if it's too large
sampled_data = data.sample(n=1000, random_state=1) if len(data) > 1000 else data
sns.pairplot(sampled_data)
plt.savefig(figures_dir / 'pairplot.png')
plt.close()

# Statistical summary
stats_summary = data.describe()
print(stats_summary)
stats_summary.to_csv(figures_dir / 'statistical_summary.csv')

# Correlation matrix
plt.figure(figsize=(16, 12))
correlation_matrix = data.corr()
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Correlation Matrix')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=45)
plt.tight_layout()
plt.savefig(figures_dir / 'correlation_matrix.png')
plt.close()

print("EDA analysis is complete. Figures and summary are saved in the figures directory.")
