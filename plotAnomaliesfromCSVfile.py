# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 08:50:00 2024

@author: ikahn


plots anomalies from anomalies.csv file


"""
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\ExploreMarineDataUsf\anomalies.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the data to understand its structure
print(data.head())

# Create a new column 'Date' combining Year, Month, and Day
data['Date'] = pd.to_datetime(data[['Year', 'Month', 'Day']])

# List all unique station indices
stations = data['StationIndex'].unique()
print("Available stations:")
for i, station in enumerate(stations):
    print(f"{i}: {station}")

# Function to plot data for a selected station
def plot_station(station_index):
    station_data = data[data['StationIndex'] == station_index]
    station_data = station_data.set_index('Date')
    anomalies = station_data['WaterLevel'] - station_data['Mean']
    
    plt.figure(figsize=(10, 6))
    plt.scatter(anomalies.index, anomalies, label=f'Station {station_index}', s=10)
    plt.xlabel('Date')
    plt.ylabel('Water Level Anomaly')
    plt.title(f'Water Level Anomalies for Station {station_index}')
    plt.legend()
    plt.grid(True)
    plt.show()

# User input to select a station
station_index = int(input("Enter the number corresponding to the station you want to plot: "))
selected_station = stations[station_index]

# Plot the data for the selected station
plot_station(selected_station)
