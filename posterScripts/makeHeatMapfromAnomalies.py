import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

"""


"""


# File path for the anomalies CSV file
anomalies_file_path = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\ExploreMarineDataUsf\posterScripts\anomalies.csv'

# Read the anomalies CSV file
dfAnomalies = pd.read_csv(anomalies_file_path, index_col=0)

# Ensure the columns are strings in 'YYYY-MM' format and filter for the years 1975-2022
filtered_columns = [col for col in dfAnomalies.columns if col.split('-')[0].isdigit() and 1975 <= int(col.split('-')[0]) <= 2022]
dfAnomalies_filtered = dfAnomalies[filtered_columns]

# Check if we have 48 stations (48 rows)
assert dfAnomalies_filtered.shape[0] == 48, "The data does not have 48 stations."

# Compute the correlation matrix
correlation_matrix = dfAnomalies_filtered.T.corr()

# Set any correlation less than 0 to NaN
correlation_matrix[correlation_matrix < 0] = float('nan')

# Check if the correlation matrix is 48 by 48
assert correlation_matrix.shape == (48, 48), "The correlation matrix is not 48 by 48."

# Print the correlation matrix to the console for inspection
print(correlation_matrix)

# Generate the heatmap without annotations and ensure the figure is centered
plt.figure(figsize=(15, 12))
ax = sns.heatmap(correlation_matrix, annot=False, cmap='hot_r', linewidths=0, cbar_kws={"shrink": .75})

# Add vertical and horizontal lines for specific stations
station_names = dfAnomalies.index.tolist()  # Assuming index contains station names
highlight_stations = ['Pensacola', 'Key West', 'Fernandina Beach']

for i, station_name in enumerate(station_names):
    if station_name in highlight_stations:
        plt.axvline(x=i, color='white', linewidth=1.5)
        plt.axhline(y=i, color='white', linewidth=1.5)

plt.title('Correlation Heatmap of Station Anomalies (1975-2022)', pad=20)
plt.tight_layout()

# Save the plot to a file
output_image_path = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\ExploreMarineDataUsf\posterScripts\correlation_heatmap_1975_2022.png'
plt.savefig(output_image_path)

print(f"Heatmap saved to {output_image_path}. Please open the image file to view it.")


"""
de trend the stations 
""" 