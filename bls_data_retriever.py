import requests
import json
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import os

# Ensure that the data directory exists
data_dir = Path('S:/JobGrowthForecaster/data')
data_dir.mkdir(parents=True, exist_ok=True)

def retrieve_bls_data(series_ids, start_year, end_year, api_key):
    headers = {'Content-type': 'application/json'}
    data = json.dumps({
        "seriesid": series_ids,
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationkey": api_key
    })
    response = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    return response.json()

# Define the series IDs and other parameters
series_ids = [
    'CES0000000001', 'CES2000000001', 'CES3000000001',
    'CES4000000001', 'CES5000000001', 'CES6000000001',
    'CES7000000001', 'CES8000000001', 'CES9000000001',
    'LNS14000000', 'CES0500000002', 'CES0500000003',
    'JTS00000000JOL', 'JTS00000000TSR'
]
load_dotenv()
api_key = os.getenv('API_KEY')  
start_year = 2011
end_year = 2021

# Retrieve the data
bls_data = retrieve_bls_data(series_ids, start_year, end_year, api_key)

# Process and save the data
for series_id in series_ids:
    series_data = []
    for series in bls_data['Results']['series']:
        if series['seriesID'] == series_id:
            for item in series['data']:
                year = item['year']
                period = item['period']
                value = item['value']
                # Only include monthly data (exclude annual summaries)
                if 'M' in period:
                    series_data.append([year, period, value])
    df = pd.DataFrame(series_data, columns=['Year', 'Period', 'Value'])
    df.to_csv(data_dir / f'{series_id}_{start_year}_to_{end_year}.csv', index=False)

print("Data retrieval complete. Check the data folder for CSV files.")
