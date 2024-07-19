# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 08:15:43 2024

@author: ikahn
"""

# extract the anomalies 
# generate heat map of correlation between sites of all the anomalies


"""
extract anomalies from monthly_average_water_levels.csv , generate heat
map of correlation between all anomalies
"""

import pandas as pd

# File paths
file_path1 = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\ExploreMarineDataUsf\posterScripts\monthly_average_water_levels.csv'
file_path2 = r'C:\Users\ikahn\Desktop\unm\IanKahn_RESUMES\ocean_sci\usf_making_waves\Research\ExploreMarineDataUsf\posterScripts\longterm_monthly_averages_1975_2022.csv'

# Read the CSV files
dfAverages = pd.read_csv(file_path1)
dfLongTermAverages = pd.read_csv(file_path2)
print(dfLongTermAverages)

# Assuming the DataFrames are structured with the same columns for stations and months

# Initialize a DataFrame to store anomalies
dfAnomalies = pd.DataFrame(index=dfAverages.index, columns=dfAverages.columns)
for i,stationRow in dfAverages.iterrows():

  stationName = stationRow[0]
  print(f"=== {stationName} ===")
  anomalyRow = [stationName]
  
  for date in stationRow.index[1:]:
      #print(date)
      splitMonth = int(date.split("-")[1])
      #print(splitMonth)
      climatologyVal = dfLongTermAverages.loc[dfLongTermAverages['month'] == splitMonth, stationName].values 
      print(climatologyVal)

      
      """
      dateVal = stationRow[date]
      print(dateVal)
      splitMonth = dateVal.split()[1]
      climatologyVal = dfLongTermAverages["month" == int(splitMonth)][stationName] 
      print(climatologyVal) 
      # split the string by the hyphen
      # (2nd part is the month, index with a 1)
      #filter for the month on the df longterm averages , get the coumn with station name 
      # then take month avg value - longterm avg value
      
      anomalyRow.append(newVal)
      """



