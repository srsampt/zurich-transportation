# Breaking down the code of punctuality_data.py...

![alt text](https://www.stadt-zuerich.ch/content/dam/stzh/portal/Deutsch/OGD/Bilder/ckan/zu-daten/DB_schema.png)


punctuality data of Zurich public transport lines (VBZ) - specifically from June 26 2022 - July 7 2022

## FIRST MERGE:
### match travel_times with the stop points from stop_positions, according to the DEPARTURE stop point
#### columns being matched:

halt_punkt_id_von:
* German: Fremdschlüssel zum Haltepunktstamm (halt_punkt_id); Zuordnung des «von»-Haltepunktes: Datentyp: (bigint, 19).
* English: Foreign key to the stop point master; assignment of the DEPARTURE stop

&

halt_punkt_id:
* German: Schlüsselfeld Haltepunkt. Datentyp: (bigint, 19).
* English: Stop point key field

___
    
halt_punkt_diva_von:
* German: Die VBZ-intern verwendete Haltepunktnummer der «von»-Haltestelle: Datentyp: (int, 10).
* English: The stop point number of the DEPARTURE stop (used internally by VBZ)

&

halt_punkt_diva: 
* German: Die VBZ-intern verwendete Haltepunktnummer ( redundant vorkommend in Fahrzeiten_SOLL_IST). Werte 0-99. Datentyp (int, 2).
* English: The stop point number used interally by VBZ

___


halt_id_von:
* German: Fremdschlüssel zum Haltestellenstamm (halt_id); Zuordnung der «von»-Haltestelle: Datentyp: (bigint, 19).
* English: Foreign key to the stop name master: assignment of the DEPARTURE stop

&

halt_id:
* German: Schlüsselfeld Haltestelle. Datentyp: (bigint, 19).
* English: Stop name key field



____

GPS_Bearing:
* German: Die Kompassrichtung des Haltepunktes. Datentyp (int, 10).
* English: 



## SECOND MERGE:
### match travel_times with the stop points from stop_positions according to the DESTINATION stop point
#### columns being matched:

halt_punkt_id_nach
* German: Fremdschlüssel zum Haltepunktstamm (halt_punkt_id); Zuordnung des «nach»-Haltepunktes: Datentyp: (bigint, 19).
* English: Foreign key to the stop point master; assignment of the DESTINATION stop

&

halt_punkt_id
* German: Schlüsselfeld Haltepunkt. Datentyp: (bigint, 19).
* English: Stop point key field

___


halt_punkt_diva_nach
* German: Die VBZ-intern verwendete Haltepunktnummer der «nach»-Haltestelle: Datentyp: (int, 10).
* English: The stop point number of the DESTINATION stop (used internally by the VBZ)

&

halt_punkt_diva
* German: Die VBZ-intern verwendete Haltepunktnummer ( redundant vorkommend in Fahrzeiten_SOLL_IST). Werte 0-99. Datentyp (int, 2).
* English: The stop point number used interally by VBZ

___

halt_id_nach
* German: Fremdschlüssel zum Haltestellenstamm (halt_id); Zuordnung der «nach»-Haltestelle: Datentyp: (bigint, 19).
* English: Foreign key to the stop name master; assignment of the DESTINATION stop

&

halt_id
* German: Schlüsselfeld Haltestelle. Datentyp: (bigint, 19).
* English: Stop name key field



## THIRD MERGE:
### match travel_time_departure_point with the stop names from stop_names according to the DEPARTURE stop point
#### columns being matched:

halt_id_von
* German: Fremdschlüssel zum Haltestellenstamm (halt_id); Zuordnung der «von»-Haltestelle: Datentyp: (bigint, 19).
* English: Foreign key to the stop name master: assignment of the DEPARTURE stop

& 

halt_id
* German: Schlüsselfeld Haltestelle. Datentyp: (bigint, 19).
* English: Stop name key field

___

halt_diva_von
* German: Die VBZ-intern verwendete Haltestellennummer der «von»-Haltestelle: Datentyp: (int, 10).
* English: The stop name number of the DEPARTURE stop (used internally by the VBZ)

&

halt_diva
* German: Die VBZ-intern verwendete Haltestellennummer. Datentyp: (int, 10).
* English:  The stop name number used interally by VBZ

___

halt_kurz_von1
* German: Die VBZ-intern verwendete Haltestellenabkürzung der «von»-Haltestelle: Datentyp: (varchar(8)).
* English: The stop name abbreviation of the DEPARTURE stop (used internally by the VBZ)

&

halt_kurz
* German: Die VBZ-intern verwendete Haltestellenabkürzung. Datentyp (varchar(8)).
* English: The stop name abbreviation (used internally by the VBZ)

___

## FOURTH MERGE:
### match travel_time_destination_point with the stop names from stop_names according to the DEPARTURE stop point
#### columns being matched:

halt_id_nach
* German: Fremdschlüssel zum Haltestellenstamm (halt_id); Zuordnung der «nach»-Haltestelle: Datentyp: (bigint, 19).
* English: Foreign key to the stop name master; assignment of the DESTINATION stop

&

halt_id
* German: Schlüsselfeld Haltestelle. Datentyp: (bigint, 19).
* English: Stop name key field

___

halt_diva_nach
* German: Die VBZ-intern verwendete Haltestellennummer der «nach»-Haltestelle: Datentyp: (int, 10).
* English: The stop name number of the DESTINATION stop (used internally by the VBZ)

&

halt_diva
* German: Die VBZ-intern verwendete Haltestellennummer. Datentyp: (int, 10).
* English:  The stop name number used interally by VBZ

___

halt_kurz_nach1
* German: Die VBZ-intern verwendete Haltestellenabkürzung der «nach»-Haltestelle: Datentyp: (varchar(8)).
* English: The stop name abbreviation of the DESTINATION stop (used internally by the VBZ)

&

halt_kurz
* German: Die VBZ-intern verwendete Haltestellenabkürzung. Datentyp (varchar(8)).
* English: The stop name abbreviation (used internally by the VBZ)





# passenger_data.py

![alt text](https://statistik.stadt-zuerich.ch/modules/ogd_bspe/pics/vbz/Datenschema_faga21.PNG)

looking at number of passengers per line/stop

### the tables:

**REISENDE** = *travelers*; main table, info about numbers of travelers

tables to match\
**LINIE** = *line*; info about line numbers\
**TAGTYP** = *day type*; info about the validation of timetables\
**HALTESTELLEN** = *stop names*; info about stop names\
**GEFAESSGROESSE** = *vessel size* , contains information about vehicle capacity\

the VBZ timetable is structured according to day types (Tagtyp)
using the attributes "Tage_DTV" and "Tage_DVW" in REISENDE, average values can be calculated for weekdays (M-F) or for the entire week
- DTV: average daily traffic
- DWV: average weekday traffic

---


