# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:06:58 2024

@author: Ian Kahn

This script contains a helper function that plots the correlation between the monthly anomalies
of two specified stations. This will help visualize the relationship between the water levels
recorded at different stations.

Positive Correlation: If the points tend to lie along a line that slopes upward from left to right, 
it indicates a positive correlation. This means that when the average water level at the first station 
increases, the average water level at the second station also tends to increase.

Negative Correlation: If the points tend to lie along a line that slopes downward from left to right, 
it indicates a negative correlation. This means that when the average water level at the first station 
increases, the average water level at the second station tends to decrease.

No Correlation: If the points are widely scattered with no discernible pattern, it indicates little to no 
correlation between the water levels at the two stations.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load the anomalies CSV file
anomaly_file_path = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\ExploreMarineDataUsf\monthly_anomalies.csv'
anomaly_df = pd.read_csv(anomaly_file_path)

# Extract year and month from column names and reshape the DataFrame
anomaly_df = anomaly_df.melt(id_vars=['Unnamed: 0'], var_name='Date', value_name='Anomaly')
anomaly_df['Date'] = pd.to_datetime(anomaly_df['Date'], format='%Y-%m')

# Rename columns for clarity
anomaly_df.rename(columns={'Unnamed: 0': 'Station'}, inplace=True)

# Pivot the DataFrame to have stations as columns
anomaly_df = anomaly_df.pivot(index='Date', columns='Station', values='Anomaly').reset_index()

# Extract station names from the columns
station_names = anomaly_df.columns[1:]  # Skip 'Date' column

# Directory to save the figures
save_dir = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\screenshots'
os.makedirs(save_dir, exist_ok=True)

# Helper function to clean station names for filenames
def clean_name(name):
    return name.replace(',', '').replace(' ', '_')

# Helper function to plot correlation between two stations
def plot_correlation(station_index1, station_index2):
    station_name1 = station_names[station_index1]
    station_name2 = station_names[station_index2]

    # Filter data for the specified stations
    station_anomalies1 = anomaly_df[['Date', station_name1]].dropna()
    station_anomalies2 = anomaly_df[['Date', station_name2]].dropna()

    # Merge the dataframes on 'Date' to find common dates
    merged_data = pd.merge(station_anomalies1, station_anomalies2, on='Date')

    # Prepare data for plotting
    data1_january = merged_data[merged_data['Date'].dt.month == 1][station_name1]
    data2_january = merged_data[merged_data['Date'].dt.month == 1][station_name2]
    data1_july = merged_data[merged_data['Date'].dt.month == 7][station_name1]
    data2_july = merged_data[merged_data['Date'].dt.month == 7][station_name2]

    plt.figure(figsize=(10, 6))
    plt.scatter(data1_january, data2_january, color='blue', label='January')
    plt.scatter(data1_july, data2_july, color='red', label='July')
    plt.title(f'Correlation between {station_name1} and {station_name2} Monthly Anomalies')
    plt.xlabel(f'{station_name1} Anomaly')
    plt.ylabel(f'{station_name2} Anomaly')
    plt.legend()
    plt.grid(True)
    cleaned_name1 = clean_name(station_name1)
    cleaned_name2 = clean_name(station_name2)
    plt.savefig(os.path.join(save_dir, f'correlation_{cleaned_name1}_{cleaned_name2}.png'))
    plt.show()


#change indices below if needed:
# Specify station indices
station_index1 = 2  # Change this to the first station index
station_index2 = 4  # Change this to the second station index

# Plot correlation between two stations
plot_correlation(station_index1, station_index2)
