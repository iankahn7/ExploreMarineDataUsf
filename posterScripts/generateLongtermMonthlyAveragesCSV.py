# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 13:42:34 2024
@author: ikahn

Generate data from a specified year range and save this range in the file name.

Read in the monthly averages CSV and then compute the long-term monthly average
for the given years specified.
"""
import pandas as pd
import os

# Define the file path to the monthly average water levels CSV
file_path = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\ExploreMarineDataUsf\monthly_average_water_levels.csv'

# Read the data from the provided CSV file
anomaly_df = pd.read_csv(file_path, index_col=0)

# Define the year range
start_year = 1975
end_year = 2022

# Filter the columns based on the specified year range
filtered_columns = [col for col in anomaly_df.columns if int(col.split('-')[0]) in range(start_year, end_year + 1)]
anomaly_df_filtered = anomaly_df[filtered_columns]

# Compute the long-term monthly averages for the filtered data

# Group by month (last two characters of the column name) and compute the mean
longterm_monthly_avg = anomaly_df_filtered.groupby(lambda x: x.split('-')[1], axis=1).mean()



# Transpose the DataFrame to match the desired format
#longterm_monthly_avg_df = longterm_monthly_avg.T

# Directory to save the output file
output_dir = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\ExploreMarineDataUsf'

# Ensure the save directory exists
os.makedirs(output_dir, exist_ok=True)



# Save the results to a new CSV file
output_file_name = f'longterm_monthly_averages_{start_year}_{end_year}_test.csv'
output_file_path = os.path.join(output_dir, output_file_name)
longterm_monthly_avg.to_csv(output_file_path)


print(f'Long-term monthly averages saved to {output_file_path}')
