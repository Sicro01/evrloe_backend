# import json
# from pathlib import Path
# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship
import evrparse.parse as parse


def main():
    # test and full source files
    test_input_log_filename = 'S05R02MAR_Alkamel_FE_R - Test.log' # set name of file
    full_input_log_filename = 'S05R02MAR_Alkamel_FE_R - Full.log' # set name of file

    # folder where the 'Source' and 'Output' folder must already exist
    data_folder = "C:/Users/770000411/OneDrive - Genpact/02 - Personal/Jupyter Projects/EVR/Data/" # set path to file"

    # name of race related to the data we're parsing
    race_name = 'S05R02MAR'

    # parse the log file and store results in dataframes - pass full source data path and race name
    parse.parse_logfile(data_folder, test_input_log_filename, race_name)




    # Base = declarative_base()
    #
    #
    # class User(Base):
    #
    #     __tablename__ = 'person'
    #
    #     id = Column('id', Integer, primary_key=True)
    #     username = Column('username', String, unique=True)
    #
    #
    # engine = create_engine('sqlite:///users.db', echo=True)
    # Base.metadata.create_all(bind=engine)
    # Session = sessionmaker(bind=engine)
    #
    # session = Session()
    # users = session.query(User).all()
    # for user in users:
    #     print('User with username {} and id {}'.format(user.username, user.id))
    # user = User()
    # # user.id = 0
    # user.username = 'alice'
    #
    # session.add(user)
    # session.commit()
    # session.close()