from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float, Table, ForeignKeyConstraint
# from evrparse.createdb import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# declare base object
Base = declarative_base()

# decalre classes to capture in db
class Race(Base):
    __tablename__ = 'race'

    race_number = Column('race_number', Integer, primary_key=True)
    season_number = Column('season_number', Integer, primary_key=True)
    race_location_short = Column('race_location_short', String(3), nullable=False)
    race_location_long = Column('race_location_long', String(20), nullable=False)

class Racing_Driver(Base):
    __tablename__ = 'racing_driver'

    driver_number = Column('driver_number', Integer, primary_key=True)
    race_number = Column('race_number', Integer, primary_key=True)
    season_number = Column('season_number', Integer, primary_key=True)
    driver_firstname = Column('driver_firstname', String(20), nullable=False)
    driver_lastname = Column('driver_lastname', String(30), nullable=False)
    driver_shortname = Column('driver_shortname', String(3), nullable=False)
    driver_team = Column('driver_team', String(100))
    driver_vehicle = Column('driver_vehicle', String(100))
    ForeignKeyConstraint(['race_number', 'season_number'], ['race.race_number', 'race.season_number'])

class Driver_Lap_Detail(Base):
    __tablename__ = 'driver_lap_detail'

    driver_number = Column('driver_number', Integer, primary_key=True)
    race_number = Column('race_number', Integer, primary_key=True)
    season_number = Column('season_number', Integer, primary_key=True)
    lap_number = Column('lap_number', Integer, primary_key=True)
    lap_loop_sector_key = Column('lap_loop_sector_key', String(6), primary_key=True)
    lap_loop_sector_number = Column('lap_loop_sector_number', Integer, primary_key=True)
    lap_datetime = Column('lap_datetime', DateTime, nullable=False)
    lap_loop_sector_time = Column('lap_loop_sector_time', Integer, nullable=False)
    lap_time = Column('lap_time', Integer, nullable=True)
    elapsed_time = Column('elapsed_time', Integer, nullable=True)
    ForeignKeyConstraint(['driver_number', 'race_number', 'season_number'], ['racing_driver.driver_number',
     'racing_driver.race_number', 'racing_driver.season_number'])

class Driver_Lap_Summary(Base):
    __tablename__ = 'driver_lap_summary'

    driver_number = Column('driver_number', Integer, primary_key=True)
    race_number = Column('race_number', Integer, primary_key=True)
    season_number = Column('season_number', Integer, primary_key=True)
    lap_number = Column('lap_number', Integer, primary_key=True)
    lap_time = Column('lap_time', Integer, nullable=False)
    elapsed_time = Column('elapsed_time', Integer, nullable=False)
    lap_datetime = Column('lap_datetime', DateTime, nullable=False)
    ForeignKeyConstraint(['driver_number', 'race_number', 'season_number'], ['racing_driver.driver_number',
     'racing_driver.race_number', 'racing_driver.season_number'])

class GPS_Lat_Lon(Base):
    __tablename__ = 'gps_lat_lon'

    gps_lat_lon_id = Column('gps_lat_lon_id', Integer, primary_key=True, autoincrement=True)
    date_time = Column('date_time', DateTime)
    line_key = Column('line_key', String)
    driver_key = Column('driver_key', Integer)
    rgps_lat_key = Column('rgps_lat_key', String)
    rgps_lat_value = Column('rgps_lat_value', Float)
    rgps_lon_key = Column('rgps_lon_key', String)
    rgps_lon_value = Column('rgps_lon_value', Float)

# instantiate the database
engine = create_engine('sqlite:///evr.db', echo=False)

# create db objects
Base.metadata.create_all(bind=engine)

# instatiate a session
Session = sessionmaker(bind=engine)
session= Session()