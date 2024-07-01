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

# Directory to save the figures
save_dir = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\screenshots'

# Ensure the save directory exists
os.makedirs(save_dir, exist_ok=True)

# Helper function to clean station names for filenames
def clean_name(name):
    return name.replace(',', '').replace(' ', '_')

# Helper function to plot correlation between anomalies of two stations
def plot_anomaly_correlation(station_index1, station_index2):
    station_name1 = station_names[station_index1]
    station_name2 = station_names[station_index2]

    # Filter data for the specified stations
    station_anomalies1 = anomaly_df[['Date', station_name1]].dropna()
    station_anomalies2 = anomaly_df[['Date', station_name2]].dropna()

    # Merge the dataframes on 'Date' to find common dates
    merged_data = pd.merge(station_anomalies1, station_anomalies2, on='Date')

    plt.figure(figsize=(14, 10))
    plt.scatter(merged_data[station_name1], merged_data[station_name2], color='blue')
    plt.title(f'Correlation between {station_name1} and {station_name2} Anomalies')
    plt.xlabel(f'{station_name1} Anomaly')
    plt.ylabel(f'{station_name2} Anomaly')
    plt.grid(True)
    cleaned_name1 = clean_name(station_name1)
    cleaned_name2 = clean_name(station_name2)
    plt.savefig(os.path.join(save_dir, f'correlation_{cleaned_name1}_{cleaned_name2}.png'))
    plt.show()

# Function to create correlation matrices and plot heatmaps
def create_correlation_matrices():
    # Extract anomaly data
    anomaly_data = anomaly_df[station_names]

    # Compute the correlation matrix
    correlation_matrix = anomaly_data.corr()

    # Compute the absolute value correlation matrix
    abs_correlation_matrix = correlation_matrix.abs()

    # Plot heatmap for correlation matrix
    plt.figure(figsize=(20, 15))
    plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='nearest')
    plt.colorbar()
    plt.title('Correlation Matrix Heatmap')
    plt.xticks(np.arange(len(station_names)), station_names, rotation=45, ha='right')
    plt.yticks(np.arange(len(station_names)), station_names)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'correlation_matrix_heatmap.png'))
    plt.show()

    # Plot heatmap for absolute value correlation matrix
    plt.figure(figsize=(20, 15))
    plt.imshow(abs_correlation_matrix, cmap='hot_r', interpolation='nearest')
    plt.colorbar()
    plt.title('Absolute Value Water Level Anomaly Correlation Matrix')
    plt.xticks(np.arange(len(station_names)), station_names, rotation=45, ha='right')
    plt.yticks(np.arange(len(station_names)), station_names)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'abs_correlation_matrix_heatmap.png'))
    plt.show()

    print("Correlation Matrix:")
    print(correlation_matrix)
    print("\nAbsolute Value Anomaly Correlation Matrix:")
    print(abs_correlation_matrix)

    return correlation_matrix, abs_correlation_matrix

# Specify station indices
station_index1 = 2  # Change this to the first station index
station_index2 = 4  # Change this to the second station index

# Plot the correlation between anomalies of the specified stations
plot_anomaly_correlation(station_index1, station_index2)

# Create and display the correlation matrices with heatmaps
correlation_matrix, abs_correlation_matrix = create_correlation_matrices()
