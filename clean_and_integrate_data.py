import pandas as pd
from pathlib import Path
from functools import reduce

# Define the path to your data directory
data_dir = Path('S:/JobGrowthForecaster/data')

# Create an empty list to hold dataframes
dataframes = []

# Mapping of series IDs to human-readable names
series_names = {
    'CES0000000001': 'Total Nonfarm Employment',
    'CES2000000001': 'Construction Employment',
    'CES3000000001': 'Manufacturing Employment',
    'CES4000000001': 'Trade, Transportation, and Utilities Employment',
    'CES5000000001': 'Information Employment',
    'CES6000000001': 'Financial Activities Employment',
    'CES7000000001': 'Professional and Business Services Employment',
    'CES8000000001': 'Education and Health Services Employment',
    'CES9000000001': 'Leisure and Hospitality Employment',
    'LNS14000000': 'Unemployment Rate',
    'CES0500000002': 'Average Weekly Hours - All Employees',
    'CES0500000003': 'Average Hourly Earnings - All Employees',
    'JTS00000000JOL': 'Job Openings Level - All Industries',
    'JTS00000000TSR': 'Total Separations Rate - All Industries'
}

# Loop through each CSV file in the data directory
integrated_data_filename = 'integrated_job_growth_data.csv'
for file in data_dir.glob('*.csv'):
    # Skip the integrated data file
    if file.name == integrated_data_filename:
        continue
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file)
    
    # Check if the series_id is in the series_names mapping and rename accordingly
    series_id = file.stem.split('_')[0]
    if series_id in series_names:
        df.rename(columns={'Value': series_names[series_id]}, inplace=True)
    else:
        print(f"Series ID {series_id} not found in series_names mapping.")
    
    # Ensure 'Year' and 'Period' columns exist before attempting to convert and drop
    if 'Year' in df.columns and 'Period' in df.columns:
        # Convert 'Year' and 'Period' to a datetime object, assuming 'Period' is a month
        df['Date'] = pd.to_datetime(df['Year'].astype(str) + df['Period'].str.replace('M', ''), format='%Y%m')
        
        # Drop the old 'Year' and 'Period' columns
        df.drop(['Year', 'Period'], axis=1, inplace=True)
    else:
        print(f"'Year' or 'Period' column not found in {file.name}")

    # Convert 'Date' to string for uniform merge and to avoid data type issues
    df['Date'] = df['Date'].astype(str)
    
    # Append the cleaned dataframe to the list
    dataframes.append(df)

# Merge all dataframes on the 'Date' column
cleaned_data = reduce(lambda left, right: pd.merge(left, right, on='Date', how='outer'), dataframes)

# After merging, convert 'Date' back to datetime
cleaned_data['Date'] = pd.to_datetime(cleaned_data['Date'])

# Save the cleaned and integrated data to a new CSV file
cleaned_data.to_csv(data_dir / 'integrated_job_growth_data.csv', index=False)

print("Data cleaning complete. The integrated dataset is saved.")

