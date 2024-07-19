# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:06:58 2024

@author: ikahn
"""
import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Load the .mat file containing time references
timeMat = scipy.io.loadmat('tchar.mat')
t_ref_char = timeMat['t_ref_char']

# Convert datetime strings to datetime objects
timeStamps = [datetime.strptime(t, '%m/%d/%Y %H:') for t in t_ref_char]

# Load the water level data
mat = scipy.io.loadmat('noaa.mat')
noaa_raw = mat['noaa_raw']
station_names = mat['name']

# Function to convert datetime object to its components
def datetime_to_vector(dt):
    return [dt.year, dt.month, dt.day, dt.hour]

# Apply the function to each datetime object in the timeStamps list
vectors = [datetime_to_vector(dt) for dt in timeStamps]

# Initialize a dictionary to store the monthly averages
monthly_averages = {}

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

# Calculate the average for each month and station
average_matrix = {}

for key, values in monthly_averages.items():
    year, month, station_index = key
    average_matrix[key] = np.mean(values)

# Convert the dictionary to a structured array for saving
dtype = [('Year', 'i4'), ('Month', 'i4'), ('StationIndex', 'i4'), ('AverageWaterLevel', 'f4')]
average_data = np.array([(year, month, station_index, avg) for (year, month, station_index), avg in average_matrix.items()], dtype=dtype)

# Save the structured array to a .npz file
np.savez('monthly_average_water_levels.npz', average_data=average_data)

# Display some of the average data for verification if testingFlag is set to True
testingFlag = False
if testingFlag:
    print("Year  Month  StationIndex  AverageWaterLevel")
    for row in average_data[:10]:
        print(row)

# Helper function to plot the average data over the raw data
def plot_average_over_raw(station_index, start_year, end_year):
    # Filter the data for the specified station and years
    filtered_data = average_data[(average_data['StationIndex'] == station_index) &
                                 (average_data['Year'] >= start_year) &
                                 (average_data['Year'] <= end_year)]
    
    dates = [datetime(year=row['Year'], month=row['Month'], day=1) for row in filtered_data]
    avg_levels = filtered_data['AverageWaterLevel']
    
    # Find the indices for the specified years in the raw data
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    mask = [(start_date <= ts <= end_date) for ts in timeStamps]
    raw_data_indices = np.argwhere(mask).flatten()
    
    raw_dates = [timeStamps[i] for i in raw_data_indices]
    raw_levels = [noaa_raw[i, station_index] for i in raw_data_indices]
    
    # Remove NaN values from the raw data
    raw_dates = [date for date, level in zip(raw_dates, raw_levels) if not np.isnan(level)]
    raw_levels = [level for level in raw_levels if not np.isnan(level)]
    
    # Retrieve the station name
    station_name = station_names[station_index][0][0]
    
    plt.figure(figsize=(10, 6))
    plt.plot(raw_dates, raw_levels, label='Raw Data', alpha=0.5)
    plt.plot(dates, avg_levels, label='Monthly Average', marker='o', color='red')
    plt.title(f'Raw Data and Monthly Average Water Level for {station_name} (Years: {start_year}-{end_year})')
    plt.xlabel('Date')
    plt.ylabel('Water Level (CM)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Helper function to plot only January and July data points
def plot_january_july(station_index, start_year, end_year):
    # Filter the data for the specified station and years
    filtered_data = average_data[(average_data['StationIndex'] == station_index) &
                                 (average_data['Year'] >= start_year) &
                                 (average_data['Year'] <= end_year)]
    
    january_dates = [datetime(year=row['Year'], month=row['Month'], day=1) for row in filtered_data if row['Month'] == 1]
    july_dates = [datetime(year=row['Year'], month=row['Month'], day=1) for row in filtered_data if row['Month'] == 7]
    
    january_levels = [row['AverageWaterLevel'] for row in filtered_data if row['Month'] == 1]
    july_levels = [row['AverageWaterLevel'] for row in filtered_data if row['Month'] == 7]
    
    # Retrieve the station name
    station_name = station_names[station_index][0][0]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(january_dates, january_levels, color='blue', label='January')
    plt.scatter(july_dates, july_levels, color='red', label='July')
    plt.title(f'January and July Average Water Levels for {station_name} (Years: {start_year}-{end_year})')
    plt.xlabel('Date')
    plt.ylabel('Water Level (CM)')
    plt.legend()
    plt.grid(True)
    plt.show()



# Example usage of the helper functions

"**********************************************************"
station_to_plot = 14  # Change this to the index of the station you want to plot
start_year = 1975
end_year = 2022
"***********************************************************"
# Plot average data over raw data
plot_average_over_raw(station_to_plot, start_year, end_year)

# Plot only January and July data points
plot_january_july(station_to_plot, start_year, end_year)
