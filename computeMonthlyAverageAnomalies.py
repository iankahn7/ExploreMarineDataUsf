import pandas as pd

# Load monthly averages and long-term averages
monthly_avg_df = pd.read_csv('monthly_average_water_levels.csv')
longterm_avg_df = pd.read_csv('longterm_monthly_average_water_levels.csv')

# Verify the columns
print("Columns in longterm_avg_df:", longterm_avg_df.columns)
print("Columns in monthly_avg_df:", monthly_avg_df.columns)

# Check if 'Month' column exists
if 'Month' not in longterm_avg_df.columns:
    raise KeyError("The 'Month' column is missing in longterm_avg_df.")

# Define number of months
years = 125
num_months = (years * 12) - 7

# Expand long-term averages to match the number of months
expanded_longterm_averages = pd.DataFrame(index=range(num_months), columns=longterm_avg_df.columns)

for month in range(1, 13):
    month_indices = list(range(month - 1, num_months, 12))
    if month == 1:  # Print indices for the first month as an example
        print(f"Month {month} indices: {month_indices[:20]}")  # Print first 20 indices
    longterm_avg_row = longterm_avg_df.loc[longterm_avg_df['Month'] == month]
    if not longterm_avg_row.empty:
        expanded_longterm_averages.loc[month_indices, :] = longterm_avg_row.values[0]
    else:
        raise ValueError(f"Month {month} not found in longterm_avg_df.")

# Function to calculate anomalies
def calculate_anomalies(monthly_values, longterm_averages):
    return monthly_values - longterm_averages

# Calculate anomalies for each station
anomalies_df = monthly_avg_df.copy()
for station in longterm_avg_df.columns:
    if station != 'Month' and station in anomalies_df.columns:
        anomalies_df[station] = calculate_anomalies(anomalies_df[station], expanded_longterm_averages[station])

# Save anomalies to a new CSV file
anomalies_df.to_csv('monthly_anomalies_water_levels.csv', index=False)
