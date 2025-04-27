import os
import pandas as pd
import matplotlib.pyplot as plt

# File path for the anomalies CSV file
anomalies_file_path = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\ExploreMarineDataUsf\posterScripts\anomalies.csv'

# Load the anomalies CSV file
anomaly_df = pd.read_csv(anomalies_file_path)

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
def plot_anomaly_correlation(station_index1, station_index2, start_year, end_year):
    station_name1 = station_names[station_index1]
    station_name2 = station_names[station_index2]

    # Filter data for the specified stations and date range
    station_anomalies1 = anomaly_df[['Date', station_name1]].dropna()
    station_anomalies2 = anomaly_df[['Date', station_name2]].dropna()
    filtered_df = anomaly_df[(anomaly_df['Date'].dt.year >= start_year) & (anomaly_df['Date'].dt.year <= end_year)]
    
    # Merge the dataframes on 'Date' to find common dates within the filtered range
    merged_data = pd.merge(
        station_anomalies1[station_anomalies1['Date'].isin(filtered_df['Date'])], 
        station_anomalies2[station_anomalies2['Date'].isin(filtered_df['Date'])], 
        on='Date'
    )

    plt.figure(figsize=(14, 10))
    plt.scatter(merged_data[station_name1], merged_data[station_name2], color='blue')
    plt.title(f'Correlation between {station_name1} and {station_name2} Anomalies ({start_year}-{end_year})')
    plt.xlabel(f'{station_name1} Anomaly')
    plt.ylabel(f'{station_name2} Anomaly')
    plt.grid(True)
    cleaned_name1 = clean_name(station_name1)
    cleaned_name2 = clean_name(station_name2)
    plt.savefig(os.path.join(save_dir, f'correlation_{cleaned_name1}_{cleaned_name2}_{start_year}_{end_year}.png'))
    plt.show()

# Specify station indices and year range
station_index1 = 2  # Change this to the first station index
station_index2 = 4  # Change this to the second station index
start_year = 1975   # Change this to the desired start year
end_year = 2022     # Change this to the desired end year

# Plot the correlation between anomalies of the specified stations
plot_anomaly_correlation(station_index1, station_index2, start_year, end_year)
