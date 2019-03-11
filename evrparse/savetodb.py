import pandas as pd
from sqlalchemy import exists, and_, func, select, MetaData
from sqlalchemy.engine import reflection
from evrparse.models import engine, session, GPS_Lat_Lon, Racing_Driver, Race, Driver_Lap
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
      _sector_number = item[11]
      _sector_time = item[13]
    else:
      _sector_number = item[13]
      _sector_time = item[15]
    
    row.lap_loop_sector_number = _sector_number
    row.lap_loop_sector_time = _sector_time

    if session.query(exists().where(and_(
      Driver_Lap.driver_number == item[4],
      Driver_Lap.race_number == 2,
      Driver_Lap.season_number == 5,
      Driver_Lap.lap_number == item[6],
      Driver_Lap.lap_loop_sector_key == item[3],
      Driver_Lap.lap_loop_sector_number == _sector_number))
      ).scalar():
      print('driver lap exists')
    else:
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

    meta = MetaData(engine, reflect=True)
    driver_lap_t = meta.tables['driver_lap']

    # select_st = select([driver_lap_t]). \
    #   select([driver_lap_t.c.driver_number, driver_lap_t.c.lap_number, driver_lap_t.c.lap_loop_sector_time, max(driver_lap_t.c.lap_loop_sector_number)],\
    #     dense_rank() OVER )
    

    subquery = session.query(
    Driver_Lap,
    func.dense_rank().over(
        partition_by=driver_lap_t.c.lap_number,
        order_by=driver_lap_t.c.lap_loop_sector_time.asc()
    ).label('timernk')
    ).subquery()

    query = session.query(subquery).filter(
    subquery.c.timernk==1
    )

    for i in query.driver_lap:
      print(i)
    # print(query.all())

    #close db session
    session.close()
  