"""
@author: ikahn


 plots the correlation between two specified stations
 but also generates a correlation matrix and an absolute 
 value correlation matrix for all stations.
"""
import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime

# Load the anomalies CSV file
anomaly_df = pd.read_csv('monthly_anomalies.csv')

# Extract station names from the columns
station_names = anomaly_df.columns[2:]  # Skip 'Year' and 'Month' columns

# Convert 'Year' and 'Month' to datetime for easier plotting
anomaly_df['Date'] = pd.to_datetime(anomaly_df[['Year', 'Month']].assign(DAY=1))

# Helper function to plot correlation between anomalies of two stations
def plot_anomaly_correlation(station_index1, station_index2):
    station_name1 = station_names[station_index1]
    station_name2 = station_names[station_index2]

    # Filter data for the specified stations
    station_anomalies1 = anomaly_df[['Date', station_name1]].dropna()
    station_anomalies2 = anomaly_df[['Date', station_name2]].dropna()

    # Merge the dataframes on 'Date' to find common dates
    merged_data = pd.merge(station_anomalies1, station_anomalies2, on='Date')

    plt.figure(figsize=(10, 6))
    plt.scatter(merged_data[station_name1], merged_data[station_name2], color='blue')
    plt.title(f'Correlation between {station_name1} and {station_name2} Anomalies')
    plt.xlabel(f'{station_name1} Anomaly')
    plt.ylabel(f'{station_name2} Anomaly')
    plt.grid(True)
    plt.show()

# Function to create correlation matrices
def create_correlation_matrices():
    # Extract anomaly data
    anomaly_data = anomaly_df[station_names]

    # Compute the correlation matrix
    correlation_matrix = anomaly_data.corr()

    # Compute the absolute value correlation matrix
    abs_correlation_matrix = correlation_matrix.abs()

    # Save the correlation matrices to CSV files
    correlation_matrix.to_csv('correlation_matrix.csv')
    abs_correlation_matrix.to_csv('abs_correlation_matrix.csv')

    print("Correlation Matrix:")
    print(correlation_matrix)
    print("\nAbsolute Value Correlation Matrix:")
    print(abs_correlation_matrix)

    return correlation_matrix, abs_correlation_matrix

# Specify station indices
station_index1 = 2  # Change this to the first station index
station_index2 = 4  # Change this to the second station index

# Plot the correlation between anomalies of the specified stations
plot_anomaly_correlation(station_index1, station_index2)

# Create and display the correlation matrices
correlation_matrix, abs_correlation_matrix = create_correlation_matrices()
