"""
Author: Ian Kahn

Description: 
This script analyzes NOAA tide gauge monthly anomalies. It performs a quadratic fit on the monthly anomalies,
detrends them, calculates the correlation and significance of the correlations between different stations, 
and generates heatmaps to visualize the significant correlations. Pensacola, Key West, and Fernandina Beach 
stations are highlighted in the visualizations.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr

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

# Function to perform quadratic fit and remove trend
def detrend_anomalies(df, station_names):
    detrended_df = df.copy()
    for station in station_names:
        x = np.arange(len(df))
        y = df[station].values
        mask = ~np.isnan(y)
        if mask.sum() >= 3:  # Ensure there are enough points to fit a quadratic model
            coeffs = np.polyfit(x[mask], y[mask], 2)
            trend = np.polyval(coeffs, x)
            detrended_df[station] = y - trend
    return detrended_df

# Function to calculate p-values for the correlation matrix
def calculate_p_values(df):
    p_values = pd.DataFrame(index=df.columns, columns=df.columns)
    for col1 in df.columns:
        for col2 in df.columns:
            if col1 != col2:
                common_data = df[[col1, col2]].dropna()
                if len(common_data) > 2:  # Ensure there are enough points for correlation calculation
                    _, p_value = pearsonr(common_data[col1], common_data[col2])
                    p_values.loc[col1, col2] = p_value
                else:
                    p_values.loc[col1, col2] = np.nan
            else:
                p_values.loc[col1, col2] = np.nan
    return p_values

# Function to plot anomalies of Lake Worth Pier versus St. Augustine
def plot_anomalies(station1, station2, df):
    plt.figure(figsize=(14, 7))
    plt.plot(df['Date'], df[station1], label=station1)
    plt.plot(df['Date'], df[station2], label=station2)
    plt.xlabel('Date')
    plt.ylabel('Anomalies')
    plt.title(f'Anomalies of {station1} vs {station2}')
    plt.legend()
    plt.grid(True)
    cleaned_station1 = clean_name(station1)
    cleaned_station2 = clean_name(station2)
    plt.savefig(os.path.join(save_dir, f'{cleaned_station1}_vs_{cleaned_station2}.png'))
    plt.show()

# Detrend anomalies
detrended_anomaly_df = detrend_anomalies(anomaly_df, station_names)

# Extract anomaly data
anomaly_data = detrended_anomaly_df[station_names]

# Compute the correlation matrix
correlation_matrix = anomaly_data.corr()

# Compute the p-values for the correlations
p_values = calculate_p_values(anomaly_data)

# Compute the absolute value correlation matrix
abs_correlation_matrix = correlation_matrix.abs()

# Plot heatmap for correlation matrix with significant correlations only
plt.figure(figsize=(10, 7))
significance_level = 0.05
mask = p_values.astype(float) > significance_level
significant_corr_matrix = correlation_matrix.mask(mask)

plt.imshow(significant_corr_matrix, cmap='coolwarm', interpolation='nearest', vmin=-1, vmax=1)
plt.colorbar()
plt.title('Correlation Detrended NOAA monthly tide gauge anomalies (significant)')
plt.xticks(np.arange(len(station_names)), station_names, rotation=45, ha='right')
plt.yticks(np.arange(len(station_names)), station_names)

# Adding white lines for specific stations
for i, station_name in enumerate(station_names):
    if station_name in ['Pensacola', 'Key West', 'Fernandina Beach', 'Fernandina']:
        plt.axvline(x=i, color='white', linewidth=1.5)
        plt.axhline(y=i, color='white', linewidth=1.5)

plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'correlation_matrix_heatmap_significant.png'))
plt.show()

# Plot heatmap for absolute value correlation matrix with significant correlations only
plt.figure(figsize=(10, 7))
significant_abs_corr_matrix = abs_correlation_matrix.mask(mask)

plt.imshow(significant_abs_corr_matrix, cmap='hot_r', interpolation='nearest', vmin=-1, vmax=1)
plt.colorbar()
plt.title('Absolute Value Water Level Detrended Anomaly Correlation Matrix (significant)')
plt.xticks(np.arange(len(station_names)), station_names, rotation=45, ha='right')
plt.yticks(np.arange(len(station_names)), station_names)

# Adding white lines for specific stations
for i, station_name in enumerate(station_names):
    if (station_name in ['Pensacola', 'Key West', 'Fernandina Beach', 'Fernandina']):
        plt.axvline(x=i, color='white', linewidth=1.5)
        plt.axhline(y=i, color='white', linewidth=1.5)

plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'abs_correlation_matrix_heatmap_significant.png'))
plt.show()

print("Significant Correlation Matrix:")
print(significant_corr_matrix)
print("\nSignificant Absolute Value Anomaly Correlation Matrix:")
print(significant_abs_corr_matrix)

# Plot anomalies of Lake Worth Pier versus St. Augustine
plot_anomalies('Lake Worth Pier, Atlantic Ocean', 'St. Augustine Beach', anomaly_df)