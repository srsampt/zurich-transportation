###################################################
############      Setup Section     ###############
###################################################


# Load packages
import os
import pandas as pd


# Set working directory
wd = os.chdir("data")

###################################################
############      Main Section     ################
###################################################


#### Load the data ####
# https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd_2022

#### Matching tables
stop_positions = pd.read_csv("stop_positions.csv")      # GPS position of each stop point
stop_names = pd.read_csv("stop_names.csv")              # full stop names

### travel time data
travel_times = pd.read_csv("travel_times.csv")


#### Matching ###
# In order to get the full stops information, you need to match travel_times with stop_positions and stop_names

### MERGE 1 ###
    ### match travel_times with the stop points from stop_positions, according to the DEPARTURE stop point
travel_time_departure_point = pd.merge(travel_times, stop_positions, how="left", # using the keys from the left frame (travel_times)
                            left_on=["halt_punkt_id_von", "halt_punkt_diva_von", "halt_id_von"],
                            right_on=["halt_punkt_id","halt_punkt_diva","halt_id"])


# adjust variable names to specifiy that these are the DEPARTURE stop point coordinates
travel_time_departure_point.rename(columns={'GPS_Latitude': 'GPS_Latitude_departure', 'GPS_Longitude': 'GPS_Longitude_departure',
                               'GPS_Bearing': 'GPS_Bearing_departure', 'halt_punkt_ist_aktiv': 'halt_punkt_ist_aktiv_departure'})


### MERGE 2 ####
    ### match travel_times with the stop points from stop_positions according to the DESTINATION stop point
travel_time_points = pd.merge(travel_time_departure_point, stop_positions, how="left",
                          left_on=["halt_punkt_id_nach","halt_punkt_diva_nach","halt_id_nach"],
                          right_on=["halt_punkt_id", "halt_punkt_diva", "halt_id"])

# adjust variable names to specify that these are the DESTINATION stop point coordinates
travel_time_points.rename(columns={'GPS_Latitude': 'GPS_Latitude_destination', 'GPS_Longitude': 'GPS_Longitude_destination',
                               'GPS_Bearing': 'GPS_Bearing_destination', 'halt_punkt_ist_aktiv': 'halt_punkt_ist_aktiv_destination'},
                                inplace=True)

### MERGE 3 ###
    ## match travel_time_points with the stop names from stop_names according to the DEPARTURE stop point
travel_time_departure_point_and_name = pd.merge(travel_time_departure_point, stop_names, how="left",                         
                                            left_on=["halt_id_von","halt_diva_von","halt_kurz_von1"],
                                            right_on=["halt_id","halt_diva","halt_kurz"])

## adjust variable names to specify that the columns are about the DEPARTURE stop
travel_time_departure_point_and_name.rename(columns={'halt_lang': 'halt_lang_departure', 'halt_ist_aktiv': 'halt_ist_aktiv_departure'},
                                            inplace=True)


### MERGE 4 ###
    ### match travel_time_departure_point with the stop names from stop_names according to the DESTINATION stop point
travel_time_points_and_names = pd.merge(travel_time_departure_point_and_name, stop_names, how="left",
                                        left_on=["halt_id_nach","halt_diva_nach","halt_kurz_nach1"],
                                        right_on=["halt_id","halt_diva","halt_kurz"])


## adjust variable names to specify that the columns are about the DESTINATION stop
travel_time_points_and_names.rename(columns={'halt_lang': 'halt_lang_destination', 'halt_ist_aktiv': 'halt_ist_aktiv_destination'},
                      inplace=True)




#### Calculate the punctuality per line ####
# According to the punctuality definition of VBZ, a ride is considered on time (punctual) when the actual arrival time at the stop
# does not exceed the scheduled arrival time by more than 2 minutes (otherwise defined as "delayed") or the actual
# departure at a stop does not happen more than 1 minute earlier than the scheduled departure (otherwise defined as
# "too early")


# first calculate the difference between actual ("ist") and scheduled ("soll") arrival ("an") / departure ("ab")
# and then assign the punctuality categories accordingly
travel_time_points_and_names['punct_categories'] = travel_time_points_and_names.apply(lambda x:
                                                     'delay' if x["ist_an_nach1"] - x["soll_an_nach"] >= 120 else 'too early'
                                                    if x["ist_ab_nach"] - x["soll_ab_nach"]<= -60 else "punctual", axis=1)

# count the occurrences per line of each category
count_punct_cat = travel_time_points_and_names.groupby(['linie', 'punct_categories']).size().rename('count')

# calculate the proportions
percent_punct = 100 * (count_punct_cat / count_punct_cat.groupby(level=0).sum())

# transform to data frame and name percentage column
punctuality = percent_punct.to_frame(name='percent')

# add count column to punctuality
punctuality = pd.merge(count_punct_cat,punctuality,how="left",
                         left_on=["linie","punct_categories"],
                         right_on=["linie","punct_categories"])



punctuality.to_csv('extracted/punctuality.csv')