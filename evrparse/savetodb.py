import pandas as pd
from evrparse.models import session, GPS_Lat_Lon, Driver
from evrparse.parse import status_rows, gps_lat_lon_rows, rgps_lat_lon_rows, weather_rows, liveevents_pitdetails_rows, \
    loop_sector_details_rows, power_mode_rows


def save_gps_rows_to_db(my_data):
  for item in my_data:
    #print(item)
    row = GPS_Lat_Lon()
    row.date_time = pd.to_datetime(item[0])
    row.driver_key = item[1]
    row.line_key = item[2]
    row.rgps_lat_key = item[3]
    row.rgps_lat_value = item[4]
    row.rgps_lon_key = item[5]
    row.rgps_lon_value = item[6]

    # add row to table
    session.add(row)

def save_racing_driver_rows_to_db(my_data):
    for item in my_data:
      row = Driver()
      print(item)
      row.driver_number = item[0]
      row.season_number = 5
      row.driver_firstname = item[1]
      row.driver_lastname = item[2]
      row.driver_shortname = item[3]
      row.driver_team = item[4]
      row.driver_vehicle = item[5]
    
      # add row to table
      session.add(row)

def commit_db_changes():
    # commit db changes
    session.commit()
    #close db session
    session.close()
  