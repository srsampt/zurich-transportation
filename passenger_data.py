###################################################
############      Setup Section     ###############
###################################################

# Load packages
import os
import pandas as pd

# suppress scientific notation from pandas results
pd.options.display.float_format = '{:.4f}'.format

# Set working directory
wd = os.chdir("data")


###################################################
############      Main Section     ################
###################################################

### Load the data
# from https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd


### Matching tables
STOP_NAMES = pd.read_csv('passenger-data/stop_names.csv', delimiter=";")
DAY_TYPE = pd.read_csv('passenger-data/day_type.csv', delimiter=";")
LINE = pd.read_csv('passenger-data/line.csv', delimiter=";")
VEHICLE_CAPACITY = pd.read_csv('passenger-data/vehicle_capacity.csv', delimiter=";")

# Main table w/ passenger count data
PASSENGERS = pd.read_csv('passenger-data/passengers.csv', delimiter=";")

# match passengers w/ stop_names, day_type, and line

PASSENGERS = PASSENGERS.drop(labels='Linienname', axis=1)


### match PASSENGERS with STOP_NAMES according to the sotp ids ("Haltestellen_Id")
passengers_stopnames = pd.merge(PASSENGERS, STOP_NAMES, how="left",
                               left_on=["Haltestellen_Id"],
                               right_on=["Haltestellen_Id"])

### match passenger_stopnames with DAY_TYPE according to the id of the day type ("Tagtyp_Id")
passengers_stopnames_daytype = pd.merge(passengers_stopnames, DAY_TYPE, how="left",
                                       left_on=["Tagtyp_Id"],
                                       right_on=["Tagtyp_Id"])

### match passenger_stopnames_daytype with LINE according to the line ids ("Linien_Id")
passengers_stopnames_daytype_line = pd.merge(passengers_stopnames_daytype, LINE, how="left",
                                            left_on=["Linien_Id"],
                                            right_on=["Linien_Id"])

### match passengers_stopnames_daytype_line with VEHICLE_CAPACITY according to the id of the scheduled trip ("Plan_Fahrt_Id")
passengers_all_data = pd.merge(passengers_stopnames_daytype_line, VEHICLE_CAPACITY, how="left",
                               left_on=["Plan_Fahrt_Id"],
                               right_on=["Plan_Fahrt_Id"])



# passengers per line per year
pax_line_year = passengers_all_data.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"])\
    [['Einsteiger','Tage_DTV']].prod(axis=1).sum(level=[0,1,2]).reset_index(name='pax_per_year').round(0)

#pax_line_year.to_csv('extracted/pax_line_year.csv')


# average passengers per day (weekday or weekend) (DTV)
avg_pax_line_alldays = passengers_all_data.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"])[['Einsteiger','Tage_DTV']].prod(axis=1).div(365).sum(level=[0,1,2]).reset_index(name='pax_per_DTV').round(0)

# average passengers per weekday(M-F) (DWV)
    # 251 weekdays
avg_pax_line_weekdays = passengers_all_data.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"])[['Einsteiger','Tage_DWV']].prod(axis=1).div(251).sum(level=[0,1,2]).reset_index(name='pax_per_DWV').round(0)

# merge the day type dataframes to a list
pax_line_year_day_type = [df.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"]) for df in [avg_pax_line_alldays, avg_pax_line_weekdays]]

# concatenate the list on columns to a dataframe
pax_line_year_day_type = pd.concat(pax_line_year_day_type, axis=1).reset_index()


#pax_line_year_day_type.to_csv('extracted/lines_pax_num_data.csv')

### Passengers per stop 

# passengers per stop per year
# group by Haltestellen_Id etc., multiply Einsteiger (= passengers getting into the vehicle) with Tage_DTV (= extrapolation factor for the whole year) and calculate the sum
pax_stop_year = passengers_all_data.set_index(["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"])[['Einsteiger','Tage_DTV']].prod(axis=1).sum(level=[0,1,2]).reset_index(name='pax_per_year').round(0)

# average passengers per day (weekday or weekend) (DTV)
avg_pax_stop_alldays = passengers_all_data.set_index(["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"])[['Einsteiger','Tage_DTV']].prod(axis=1).div(365).sum(level=[0,1,2]).reset_index(name='pax_per_DTV').round(0)

# average passengers per weekday(M-F) (DWV)
    # 251 weekdays
avg_pax_stop_weekdays = passengers_all_data.set_index(["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"])[['Einsteiger','Tage_DWV']].prod(axis=1).div(251).sum(level=[0,1,2]).reset_index(name='pax_per_DWV').round(0)

# merge the day type dataframes to a list
pax_stops_year_day_type = [df.set_index(["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"]) for df in [avg_pax_stop_alldays, avg_pax_stop_weekdays]]

# concatenate the list on columns to a data frame
pax_stops_year_day_type = pd.concat(pax_stops_year_day_type, axis=1).reset_index()

pax_stop_year.to_csv('extracted/pax_stop_year.csv')

#pax_stops_year_day_type.to_csv('extracted/stops_pax_num_data.csv')