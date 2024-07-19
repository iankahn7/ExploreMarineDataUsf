import pandas as pd

# File paths
file_path1 = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\ExploreMarineDataUsf\posterScripts\monthly_average_water_levels.csv'
file_path2 = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\ExploreMarineDataUsf\posterScripts\longterm_monthly_averages_1975_2022.csv'

# Read the CSV files
dfAverages = pd.read_csv(file_path1)
dfLongTermAverages = pd.read_csv(file_path2)

finalData = []

# Initialize a DataFrame to store anomalies
dfAnomalies = pd.DataFrame(index=dfAverages.index, columns=dfAverages.columns)
for i, stationRow in dfAverages.iterrows():
    stationName = stationRow[0]
    print(f"=== {stationName} ===")
    anomalyRow = [stationName]
    
    for date in stationRow.index[1:]:
        splitMonth = int(date.split("-")[1])
        monthVal = stationRow[date]
        climatologyVal = dfLongTermAverages.loc[dfLongTermAverages['month'] == splitMonth, stationName].values     
        finalVal = monthVal - climatologyVal
        anomalyRow.append(finalVal[0])
        
    print(anomalyRow)
    finalData.append(anomalyRow)

# Create DataFrame from finalData
df = pd.DataFrame(finalData)

# Add header
headers = ['Station'] + [date for date in dfAverages.columns[1:]]
df.columns = headers

# Save to CSV
output_file_path = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\ExploreMarineDataUsf\posterScripts\anomalies.csv'
df.to_csv(output_file_path, index=False)
