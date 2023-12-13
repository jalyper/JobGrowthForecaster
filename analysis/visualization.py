# visualization.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Define the directory where the predictions are saved and where figures should be saved
model_dir = Path('S:/JobGrowthForecaster/modeling')
figures_dir = Path('S:/JobGrowthForecaster/analysis/figures')
figures_dir.mkdir(parents=True, exist_ok=True)  # Create the figures directory if it doesn't exist

# Load the predictions
predictions = pd.read_csv(model_dir / 'model_predictions.csv')

# Actual vs Predicted plot
plt.figure(figsize=(10, 6))
plt.scatter(predictions['Actual'], predictions['Predicted'], alpha=0.5)
plt.title('Actual vs Predicted')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.plot([predictions['Actual'].min(), predictions['Actual'].max()],
         [predictions['Actual'].min(), predictions['Actual'].max()], 'k--', lw=2)
plt.savefig(figures_dir / 'actual_vs_predicted.png')
plt.close()

# Residuals Plot
residuals = predictions['Actual'] - predictions['Predicted']
plt.figure(figsize=(10, 6))
plt.scatter(predictions['Predicted'], residuals, alpha=0.5)
plt.title('Residuals vs Predicted')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.hlines(y=0, xmin=predictions['Predicted'].min(), xmax=predictions['Predicted'].max(), colors='red', linestyles='--')
plt.savefig(figures_dir / 'residuals_vs_predicted.png')
plt.close()

# Histogram of Prediction Errors
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True, bins=30, edgecolor='k')
plt.title('Histogram of Prediction Errors')
plt.xlabel('Prediction Error')
plt.ylabel('Frequency')
plt.savefig(figures_dir / 'prediction_error_histogram.png')
plt.close()

# Time Series Plot (if applicable)
# Note: Only include this if 'Date' is part of your predictions and it's a time series problem.
# You would need to modify the code to ensure 'Date' is available and in the correct format.

print("Visualization complete. Figures are saved in the figures directory.")
