# model_development.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from joblib import dump
from pathlib import Path
import math

# Load the cleaned and integrated dataset
data = pd.read_csv('S:/JobGrowthForecaster/data/integrated_job_growth_data.csv')

# Convert 'Date' to datetime and set it as the index for modeling (if not already done)
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Check for columns with all NaN values and drop them or fill with a constant
columns_with_all_nan = data.columns[data.isna().all()].tolist()
if columns_with_all_nan:
    print(f"Columns with all NaN values: {columns_with_all_nan}")
    # Option 1: Drop columns
    data.drop(columns=columns_with_all_nan, inplace=True)

# Predict values for specified category
target = 'Information Employment'

# Prepare the data for modeling
X = data.drop(target, axis=1)
y = data[target]

# Impute any remaining NaN values using SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')  
X_imputed = imputer.fit_transform(X)

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, 
    y, 
    test_size=0.2,  # 80% training and 20% testing
    random_state=42
)

# Initialize the model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# save predictions
predictions = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
predictions.to_csv('S:/JobGrowthForecaster/modeling/model_predictions.csv', index=False)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Calculate RMSE
rmse = math.sqrt(mse)
print(f'Root Mean Squared Error: {rmse}')

# Save the model and scaler for future use
model_dir = Path('S:/JobGrowthForecaster/modeling')
model_dir.mkdir(parents=True, exist_ok=True)
dump(model, model_dir / 'linear_regression_model.joblib')
dump(scaler, model_dir / 'scaler.joblib')
dump(imputer, model_dir / 'imputer.joblib')  # Also save the imputer

print("Model, scaler, and imputer have been saved.")
