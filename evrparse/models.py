from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float, Table
# from evrparse.createdb import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# declare base object
Base = declarative_base()

# decalre classes to capture in db


class Race(Base):
    __tablename__ = 'race'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    race_number = Column('race_number', Integer, nullable=False)
    season_number = Column('season_number', Integer, nullable=False)
    race_location_short = Column('race_location_short', String(3), nullable=False)
    race_location_long = Column('race_location_long', String(20), nullable=False)
    racing_drivers = relationship('Racing_Driver') 

class Racing_Driver(Base):
    __tablename__ = 'racing_driver'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    race_id = Column(Integer, ForeignKey('race.id'))
    driver_number = Column('driver_number', Integer, nullable=False)
    driver_firstname = Column('driver_firstname', String(20), nullable=False)
    driver_lastname = Column('driver_lastname', String(30), nullable=False)
    driver_shortname = Column('driver_shortname', String(3), nullable=False)
    driver_team = Column('driver_team', String(100))
    driver_vehicle = Column('driver_vehicle', String(100))

class Lap(Base):
    __tablename__ = 'lap'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    racing_driver_id = Column(Integer, ForeignKey('racing_driver.id'))
    lap_number = Column('lap_number', Integer, nullable=False)
    lap_time = Column('lap_time', Float, nullable=False)
    lap_position = Column('lap_position', Integer, nullable=False)


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