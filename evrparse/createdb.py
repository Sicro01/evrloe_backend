from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# declare base object
Base = declarative_base()

# instantiate the database
engine = create_engine('sqlite:///evr.db', echo=False)

# # create db objects
# Base.metadata.create_all(bind=engine)

# instatiate a session
Session = sessionmaker(bind=engine)
session= Session()