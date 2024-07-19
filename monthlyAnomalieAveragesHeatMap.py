# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:06:58 2024

@author: Ian Kahn

This script reads monthly anomalies data and creates a heatmap of the correlation matrix for all stations.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the monthly anomalies CSV file
anomaly_file_path = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\ExploreMarineDataUsf\monthly_anomalies.csv'
anomaly_df = pd.read_csv(anomaly_file_path)

# Transpose the DataFrame to have dates as rows and stations as columns
anomaly_df = anomaly_df.transpose()

# Set the first row as the header
anomaly_df.columns = anomaly_df.iloc[0]
anomaly_df = anomaly_df.drop(anomaly_df.index[0])

# Reset the index to get dates as a column
anomaly_df = anomaly_df.reset_index().rename(columns={'index': 'Date'})

# Convert the 'Date' column to datetime
anomaly_df['Date'] = pd.to_datetime(anomaly_df['Date'], format='%Y-%m')

# Melt the DataFrame to long format
anomaly_df = anomaly_df.melt(id_vars=['Date'], var_name='Station', value_name='Anomaly')

# Pivot the DataFrame to have stations as columns
anomaly_df = anomaly_df.pivot(index='Date', columns='Station', values='Anomaly')

# Extract station names from the columns
station_names = anomaly_df.columns

# Print the anomaly_df to check if the data is correctly processed
print(anomaly_df.head())

# Create correlation matrices and plot heatmaps
def create_correlation_matrices():
    # Compute the correlation matrix
    correlation_matrix = anomaly_df.corr()

    # Compute the absolute value correlation matrix
    abs_correlation_matrix = correlation_matrix.abs()

    # Directory to save the figures
    save_dir = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\screenshots'
    os.makedirs(save_dir, exist_ok=True)

    # Plot heatmap for correlation matrix
    plt.figure(figsize=(10, 7))
    plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='nearest')
    plt.colorbar()
    plt.title('Correlation NOAA Monthly Tide Gauge Anomalies')
    plt.xticks(np.arange(len(station_names)), station_names, rotation=45, ha='right')
    plt.yticks(np.arange(len(station_names)), station_names)
    
    # Adding white lines for specific stations
    for i, station_name in enumerate(station_names):
        if station_name in ['Pensacola', 'Key West', 'Fernandina Beach']:
            plt.axvline(x=i, color='white', linewidth=1.5)
            plt.axhline(y=i, color='white', linewidth=1.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'correlation_matrix_heatmap.png'))
    plt.show()

    # Plot heatmap for absolute value correlation matrix
    plt.figure(figsize=(10, 7))
    plt.imshow(abs_correlation_matrix, cmap='hot_r', interpolation='nearest')
    plt.colorbar()
    plt.title('Absolute Value Water Level Anomaly Correlation Matrix')
    plt.xticks(np.arange(len(station_names)), station_names, rotation=45, ha='right')
    plt.yticks(np.arange(len(station_names)), station_names)
    
    # Adding white lines for specific stations
    for i, station_name in enumerate(station_names):
        if station_name in ['Pensacola', 'Key West', 'Fernandina Beach']:
            plt.axvline(x=i, color='white', linewidth=1.5)
            plt.axhline(y=i, color='white', linewidth=1.5)
    
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'abs_correlation_matrix_heatmap.png'))
    plt.show()

    print("Correlation Matrix:")
    print(correlation_matrix)
    print("\nAbsolute Value Anomaly Correlation Matrix:")
    print(abs_correlation_matrix)

    return correlation_matrix, abs_correlation_matrix

# Create and display the correlation matrices with heatmaps
correlation_matrix, abs_correlation_matrix = create_correlation_matrices()
