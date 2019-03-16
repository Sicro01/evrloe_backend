import pandas as pd
import sqlite3
from sqlalchemy import exists, and_, MetaData, Column, update, func
from sqlalchemy.engine import reflection
from evrparse.models import engine, session, GPS_Lat_Lon, Racing_Driver, Race, Driver_Lap_Detail, Driver_Lap_Summary
from evrparse.parse import status_rows, gps_lat_lon_rows, rgps_lat_lon_rows, weather_rows, liveevents_pitdetails_rows, \
    loop_sector_details_rows, power_mode_rows

race_number = 2
season_number = 5
race_location_short = 'MAR'
race_location_long = 'Marrakesh'


def save_race_rows():
  row = Race()
  row.race_number = race_number
  row.season_number = season_number
  row.race_location_short = race_location_short
  row.race_location_long = race_location_long

  if session.query(exists().where(and_(
    Race.race_number == race_number,
    Race.season_number == season_number))
    ).scalar():
    pass
  else:
    # add row to table
    session.add(row)


def save_racing_driver_rows(my_data):
  for item in my_data:
    row = Racing_Driver()
    row.driver_number = item[0]
    row.race_number = race_number
    row.season_number = season_number
    row.driver_firstname = item[1]
    row.driver_lastname = item[2]
    row.driver_shortname = item[3]
    row.driver_team = item[4]
    row.driver_vehicle = item[5]

    if session.query(exists().where(and_(
      Racing_Driver.driver_number == item[0],
      Racing_Driver.race_number == race_number,
      Racing_Driver.season_number == season_number))
      ).scalar():
      pass
    else:
      # add row to table
      session.add(row)


def save_driver_lap_detail_rows(my_data):
  for item in my_data:
    row = Driver_Lap_Detail()
    row.driver_number = item[4]
    row.race_number = race_number
    row.season_number = season_number
    row.lap_datetime = pd.to_datetime(item[0])
    row.lap_loop_sector_key = item[3]
    row.lap_number = item[6]
    row.lap_time = 0
    row.elapsed_time = 0
    
    if item[3] == 'loopSectors':
      _sector_number = item[11]
      _sector_time = item[13]
    else:
      _sector_number = item[13]
      _sector_time = item[15]
    
    row.lap_loop_sector_number = _sector_number
    row.lap_loop_sector_time = _sector_time

    if session.query(exists().where(and_(
      Driver_Lap_Detail.driver_number == item[4],
      Driver_Lap_Detail.race_number == race_number,
      Driver_Lap_Detail.season_number == season_number,
      Driver_Lap_Detail.lap_number == item[6],
      Driver_Lap_Detail.lap_loop_sector_key == item[3],
      Driver_Lap_Detail.lap_loop_sector_number == _sector_number))
      ).scalar():
      pass
    else:
      # add row to table
      session.add(row)


def save_driver_lap_summary_rows(my_data):
  for item in my_data:
    row = Driver_Lap_Summary()
    row.driver_number = item[4]
    row.race_number = race_number
    row.season_number = season_number
    row.lap_number = item[2]
    row.lap_time = item[3]
    row.elapsed_time = item[1]
    row.lap_datetime = pd.to_datetime(item[0])

    if session.query(exists().where(and_(
        Driver_Lap_Summary.driver_number == item[4],
        Driver_Lap_Summary.race_number == race_number,
        Driver_Lap_Summary.season_number == season_number,
        Driver_Lap_Summary.lap_number == item[2]))
        ).scalar():
        pass
    else:
        # add row to table
        session.add(row)


def save_gps_rows(my_data):
  for item in my_data:
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

def print_lap_leader():
  qry = session.query(
    Driver_Lap_Summary.lap_number,
    Driver_Lap_Summary.driver_number,
    func.min(
      Driver_Lap_Summary.elapsed_time
      ).label(
      'fastest_time')
  ).group_by(
    Driver_Lap_Summary.lap_number,
  ).order_by(
    Driver_Lap_Summary.lap_number,
    Driver_Lap_Summary.driver_number
  )

  for a,b,c in qry:
    print(a,b,c)

def commit_db_changes():
    # commit db changes
    session.commit()
  
    #close db session
    session.close()
  

# session.query(
  #   Driver_Lap_Detail
  # ).filter(
  #   Driver_Lap_Detail.driver_number == Driver_Lap_Summary.driver_number
  # ).filter(
  #   Driver_Lap_Detail.race_number == Driver_Lap_Summary.race_number
  # ).filter(
  #   Driver_Lap_Detail.season_number == Driver_Lap_Summary.season_number
  # ).filter(
  #   Driver_Lap_Detail.lap_number == Driver_Lap_Summary.lap_number 
  # ).update(
  #   {Driver_Lap_Detail.lap_time: Driver_Lap_Summary.lap_time},
  #   synchronize_session='fetch'
  # )


  # meta = MetaData(engine, reflect=True)
    # driver_lap_t = meta.tables['driver_lap']

    # select_st = select([driver_lap_t]). \
    #   select([driver_lap_t.c.driver_number, driver_lap_t.c.lap_number, driver_lap_t.c.lap_loop_sector_time, max(driver_lap_t.c.lap_loop_sector_number)],\
    #     dense_rank() OVER )
    
    # session.query(Driver_Lap).all()
    # for instance in session.query(Driver_Lap):
    #   print(instance.driver_number,
    #         instance.race_number)



    # sq = session.query(
    #   Driver_Lap.driver_number,
    #   Driver_Lap.lap_number,
    #   Driver_Lap.lap_loop_sector_time,
    #   func.max(Driver_Lap.lap_loop_sector_number),
    #   func.dense_rank().over(
    #     partition_by=Driver_Lap.lap_number,
    #     order_by=Driver_Lap.lap_loop_sector_time.asc()
    # ).label('lap_rank')
    # ).group_by(Driver_Lap.driver_number, Driver_Lap.lap_number).subquery('sq')

    # query = session.query(sq).filter(
    #   sq.c.lap_rank==1
    # )
    
    # for i in query:
    #   pass

    # test = session.query(
    #   Driver_Lap.driver_number,
    #   Driver_Lap.lap_number,
      
    #   func.rank().over( 
    #     partition_by=Driver_Lap.lap_number,
    #     order_by=Driver_Lap.lap_loop_sector_time.asc()
    #   ).label('laprank')
      
    #   ).subquery('test')
    
      # func.dense_rank().over(
      #   partition_by=Driver_Lap.lap_number,
      #   order_by=Driver_Lap.lap_loop_sector_time.asc()
# func.max(Driver_Lap.lap_loop_sector_number).label('maxsect'),
# ).group_by(Driver_Lap.driver_number, Driver_Lap.lap_number
    # query = session.query(test)
    

    # for dn,ln,sn,x  in query:
    #   print(dn, ln, sn,x)

    

    
    # sql = text('                          \
    #                                       \
    #           SELECT                      \
    #           driver_number,              \
    #           lap_number,                 \
    #           lap_loop_sector_time        \
    #           FROM (                      \
    #             SELECT                    \
    #             lap_number                \
    #             max(lap_loop_sector_time) \
    #             FROM                      \
    #             driver_lap                \
    #             group by 1                \
    #             )                         \
    #                                       \
    #           ')

    # result = engine.execute(sql)

    # for i in result:
    #   print(i[0])