### MERGING A FEW CSV FILES TO TEST OUT RESULTS


import pandas as pd
import os

wd = os.chdir("data")


############################
# MERGE STOP POSITIONS AND STOP NAMES
# AND FILTER OUT INACTIVE STOPS
############################

# Read the CSV files into pandas DataFrames
stop_names_df = pd.read_csv("punctuality-data/stop_names1.csv") 
stop_positions_df = pd.read_csv("punctuality-data/stop_positions.csv")   

# Merge the DataFrames on the 'halt_id' column
merged_df = pd.merge(stop_names_df, stop_positions_df, on='halt_id')

mask = (merged_df['halt_ist_aktiv'] == merged_df['halt_punkt_ist_aktiv'])

# Apply the mask to filter out rows where the condition is not met
filtered_df = merged_df[mask]

# Write the filtered DataFrame to a new CSV file
filtered_df.to_csv('stop_names_positions_filtered.csv', index=False)



############################
# MERGE YEARLY LINE RIDERSHIP AND LINE INFO
############################

transit_lines_df = pd.read_csv("passenger-data/transit_lines_shp.csv")
pax_line_year_df = pd.read_csv("extracted/csv/pax_line_year.csv")

merged_df = pd.merge(transit_lines_df, pax_line_year_df, how='inner', left_on='LINIENNUMM', right_on='Linienname_Fahrgastauskunft')

# Drop the redundant column created by the merge operation
merged_df.drop('Linienname_Fahrgastauskunft', axis=1, inplace=True)


merged_df.to_csv("yearly_pax_lines_combined.csv", index=False)


punctuality_df = pd.read_csv("extracted/csv/punctuality.csv")
line_df = pd.read_csv("passenger-data/line.csv", delimiter=";")



merged_df = pd.merge(punctuality_df, line_df, how="left", left_on='linie', right_on="Linienname")

merged_df.drop(columns=["Linienname"], inplace=True)

merged_df.to_csv('punctuality_more_line_info.csv', index=False)