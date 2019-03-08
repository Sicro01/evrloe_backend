import pandas as pd
from sqlalchemy import exists, and_
from evrparse.models import session, GPS_Lat_Lon, Racing_Driver, Race, Driver_Lap
from evrparse.parse import status_rows, gps_lat_lon_rows, rgps_lat_lon_rows, weather_rows, liveevents_pitdetails_rows, \
    loop_sector_details_rows, power_mode_rows

def save_race_to_db():
  row = Race()
  row.race_number = 2
  row.season_number = 5
  row.race_location_short = 'MAR'
  row.race_location_long = 'Marrakesh'

  # add row to table
  session.add(row)

def save_racing_driver_rows_to_db(my_data):
  for item in my_data:
    row = Racing_Driver()
    print(item)
    row.driver_number = item[0]
    row.race_number = 2
    row.season_number = 5
    row.driver_firstname = item[1]
    row.driver_lastname = item[2]
    row.driver_shortname = item[3]
    row.driver_team = item[4]
    row.driver_vehicle = item[5]

    if session.query(exists().where(and_(
      Racing_Driver.driver_number == item[0],
      Racing_Driver.race_number == 2,
      Racing_Driver.season_number == 5))
      ).scalar():

      print(f'Driver {Racing_Driver.driver_number} record exists for season {Racing_Driver.season_number} \
         race {Racing_Driver.race_number}')
      return

    else:
      # add row to table
      print(f'Adding driver {Racing_Driver.driver_number} record for season {Racing_Driver.season_number} \
         race {Racing_Driver.race_number}')
      session.add(row)

    # ret = session.query(exists().where(and_(Someobject.field1 == value1, Someobject.field2 == value2)))

    
def save_loop_sector_details_rows_to_db(my_data):
  for item in my_data:
    row = Driver_Lap()
    row.driver_number = item[4]
    row.race_number = 2
    row.season_number = 5
    row.lap_datetime = pd.to_datetime(item[0])
    row.lap_loop_sector_key = item[3]
    row.lap_number = item[6]
    if item[3] == 'loopSectors':
      row.lap_loop_sector_number = item[11]
      row.lap_loop_sector_time = item[13]
    else:
      row.lap_loop_sector_number = item[13]
      row.lap_loop_sector_time = item[15]
    # print(f'dr num {row.driver_number}, r num {row.race_number} s num {row.season_number}l num {row.lap_number}\
    #   loop_sector_key {row.lap_loop_sector_key}, loop_sector_num {row.lap_loop_sector_number} ')

    # add row to table
    session.add(row)

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

def commit_db_changes():
    # commit db changes
    session.commit()
    #close db session
    session.close()
  