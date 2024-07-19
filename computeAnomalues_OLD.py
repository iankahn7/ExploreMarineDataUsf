"""
ianKahn 

computes anomales

anomaly = avg - climatological_avg



"""


import os
import scipy.io
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Load the .mat file containing time references
timeMat = scipy.io.loadmat('tchar.mat')
t_ref_char = timeMat['t_ref_char']

# Convert datetime strings to datetime objects
timeStamps = [datetime.strptime(t, '%m/%d/%Y %H:') for t in t_ref_char.flatten()]

# Load the water level data
mat = scipy.io.loadmat('noaa.mat')
noaa_raw = mat['noaa_raw']
station_names = [name[0][0] for name in mat['name']]

# Function to convert datetime object to its components
def datetime_to_vector(dt):
    return [dt.year, dt.month, dt.day, dt.hour]

# Apply the function to each datetime object in the timeStamps list
vectors = [datetime_to_vector(dt) for dt in timeStamps]

# Initialize dictionaries to store the monthly averages and count of good points
monthly_averages = {}
monthly_good_points = {}

# Loop over each station
for station_index in range(noaa_raw.shape[1]):
    # Loop over each datetime vector and corresponding water level
    for vector, water_level in zip(vectors, noaa_raw[:, station_index]):
        year, month, _, _ = vector
        key = (year, month, station_index)
        
        if key not in monthly_averages:
            monthly_averages[key] = []
        
        if not np.isnan(water_level):  # Check for NaN and ignore if NaN
            monthly_averages[key].append(water_level)

# Calculate the average and count for each month and station
average_matrix = {}
good_points_matrix = {}

for key, values in monthly_averages.items():
    year, month, station_index = key
    average_matrix[key] = np.mean(values)
    good_points_matrix[key] = len(values)

# Prepare data for CSV files
average_data = []
good_points_data = []

for (year, month, station_index), avg in average_matrix.items():
    station_name = station_names[station_index]
    average_data.append([year, month, station_name, avg])
    good_points = good_points_matrix[(year, month, station_index)]
    good_points_data.append([year, month, station_name, good_points])

# Convert to DataFrame
average_df = pd.DataFrame(average_data, columns=['Year', 'Month', 'StationName', 'AverageWaterLevel'])
good_points_df = pd.DataFrame(good_points_data, columns=['Year', 'Month', 'StationName', 'GoodPointsCount'])

# Save to CSV files
average_df.to_csv('monthly_average_water_levels.csv', index=False)
good_points_df.to_csv('monthly_good_points_count.csv', index=False)

# Calculate long-term monthly averages (climatological averages)
longterm_monthly_data = {station_index: {month: [] for month in range(1, 13)} for station_index in range(len(station_names))}

# Loop over each station
for station_index in range(noaa_raw.shape[1]):
    # Loop over each datetime vector and corresponding water level
    for vector, water_level in zip(vectors, noaa_raw[:, station_index]):
        _, month, _, _ = vector
        
        if not np.isnan(water_level):  # Check for NaN and ignore if NaN
            longterm_monthly_data[station_index][month].append(water_level)

# Calculate the long-term average for each month and station
longterm_average_matrix = {station_index: {month: -999 for month in range(1, 13)} for station_index in range(len(station_names))}

for station_index, months in longterm_monthly_data.items():
    for month, values in months.items():
        if values:  # Check if there are any values
            longterm_average_matrix[station_index][month] = np.mean(values)

# Calculate monthly anomalies
anomaly_matrix = {}

for (year, month, station_index), avg in average_matrix.items():
    climatological_avg = longterm_average_matrix[station_index][month]
    anomaly = avg - climatological_avg
    key = (year, month)
    if key not in anomaly_matrix:
        anomaly_matrix[key] = {}
    anomaly_matrix[key][station_index] = anomaly

# Prepare data for anomalies CSV file
anomaly_data = {'Year': [], 'Month': []}
for station_name in station_names:
    anomaly_data[station_name] = []

for (year, month), anomalies in anomaly_matrix.items():
    anomaly_data['Year'].append(year)
    anomaly_data['Month'].append(month)
    for station_index, station_name in enumerate(station_names):
        anomaly_data[station_name].append(anomalies.get(station_index, -999))

# Convert anomalies to DataFrame
anomaly_df = pd.DataFrame(anomaly_data)

# Save to CSV file
anomaly_df.to_csv('monthly_anomalies.csv', index=False)

# Helper function to plot anomalies for a given station index
def plot_anomalies(station_index):
    station_anomalies = anomaly_df[['Year', 'Month', station_names[station_index]]]
    
    if station_anomalies.empty:
        print(f"No anomalies found for station index {station_index}.")
        return
    
    plt.figure(figsize=(12, 6))
    plt.plot(station_anomalies['Year'], station_anomalies[station_names[station_index]], 'ro', label='Anomalies')
    plt.axhline(y=0, color='gray', linestyle='--')
    plt.xlabel('Year')
    plt.ylabel('Anomaly')
    plt.title(f'Monthly Anomalies in Water Levels for Station Index {station_index} ({station_names[station_index]})')
    plt.legend()
    plt.show()

# Example usage of plot_anomalies function
plot_anomalies(0)  # Replace 0 with the actual station index you want to plot

# Display some of the average data for verification if testingFlag is set to True
testingFlag = True
if testingFlag:
    print("Monthly Average Water Levels")
    print(average_df.head(10))
    print("Long-term Monthly Average Water Levels")
    print(pd.DataFrame(longterm_average_matrix).head(12))
    print("Monthly Anomalies")
    print(anomaly_df.head(10))



"""
take the old code for correlations, read in the anomalies and then run the 
correlations. Before we had hourly time series, now we have monthly time series
"""