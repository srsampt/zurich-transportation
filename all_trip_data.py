
###################################################
### CREATING A NEW CSV FILE OF ALL OF THE TRIPS FROM
### THE WEEK, ASSIGNING APPROPRIATE COORDINATES TO THE
### DEPARTURE AND DESTINATION STOPS TO CREATE STOP POINTS
### AND THEN TO CREATE LINES REPRESENTING EACH TRIP
###################################################

# reads the CSV files, merges them based on the stop numbers, 
# calculates punctuality, selects the relevant columns
# then exports the resulting DataFrame to new CSV file called "trip_data.csv" (test_trip_data.csv)

# Load packages
import os
import pandas as pd


# Set working directory
wd = os.chdir("data")

travel_times_df = pd.read_csv("punctuality-data/travel_times.csv")
stop_positions_df = pd.read_csv("punctuality-data/stop_positions.csv")
stop_names_df = pd.read_csv("punctuality-data/stop_names1.csv")



# merge travel_times and stop_positions using the DEPARTURE stop id number 
# aka assign the correct coordinates to the departure stop
merged_df = pd.merge(travel_times_df, stop_positions_df, left_on="halt_punkt_id_von", right_on="halt_punkt_id", how="left")

merged_df.rename(columns={'halt_punkt_id_von' : 'depart_stop_id'}, inplace=True)


# merge travel_times and stop_positions using the DESTINATION stop id number 
# aka assign the correct coordinates to the destination stop
# and assign suffixes to differentiate between coordinates for departure stop vs. destination stop
merged_df = pd.merge(merged_df, stop_positions_df, left_on="halt_punkt_id_nach", right_on="halt_punkt_id", suffixes=("_departure", "_destination"), how="left")


merged_df.rename(columns={'halt_punkt_id_nach' : 'destin_stop_id'}, inplace=True)


merged_df.rename(columns={'soll_an_nach' : 'target_arrival_at_dest', 'ist_an_nach1' : 'actual_arrival_at_dest', 'soll_ab_nach' : 'target_depart_from_dest', 'ist_ab_nach' : 'actual_depart_from_dest'}, inplace=True)



# soll_an_nach = target arrival at the destination
# ist_an_nach1 = actual arrival at the destination

# soll_ab_nach = target departure 
# ist_ab_nach = actual departure 

merged_df['punct_cat'] = merged_df.apply(lambda x:
                                            'delay' if x["actual_arrival_at_dest"] - x["target_arrival_at_dest"] >= 120 else 'too early'
                                            if x["actual_depart_from_dest"] - x["target_depart_from_dest"]<= -60 else "punctual", axis=1)


final_df = merged_df[['linie', 'richtung', 'betriebsdatum', 'depart_stop_id', 'destin_stop_id', 'punct_cat', 'GPS_Latitude_departure', 'GPS_Longitude_departure', 'GPS_Latitude_destination', 'GPS_Longitude_destination']]

final_df.to_csv('test_trip_data.csv', index=False)

# merged_df.to_csv('trip_data.csv')


# # calculate punctuality
# merged_df['actual arrival time'] = pd.to_datetime(merged_df['actual arrival time'], unit='s')  # Convert seconds to datetime
# merged_df['target arrival time'] = pd.to_datetime(merged_df['target arrival time'], unit='s')  # Convert seconds to datetime
# merged_df['actual departure time'] = pd.to_datetime(merged_df['actual departure time'], unit='s')  # Convert seconds to datetime
# merged_df['target departure time'] = pd.to_datetime(merged_df['target departure time'], unit='s')  # Convert seconds to datetime