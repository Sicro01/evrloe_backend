import evrparse.parse as ps
# import evrparse.models as md
# from evrparse.createdb import Base, engine
import evrparse.savetodb as sv



def main():
    
    # test and full source files
    test_input_log_filename = 'S05R02MAR_Alkamel_FE_R - Test.log' # set name of file
    full_input_log_filename = 'S05R02MAR_Alkamel_FE_R - Full.log' # set name of file

    # folder where the 'Source' and 'Output' folder must already exist
    data_folder = "D:/Simon/Documents/pythonprojects/evrloe_backend/" # set path to file"

    # name of race related to the data we're parsing
    race_name = 'S05R02MAR'

    # parse the log file and store results in dataframes - pass full source data path and race name
    ps.parse_logfile(data_folder, test_input_log_filename, race_name)
    
    # save data to tables
    sv.save_gps_rows_to_db(ps.gps_lat_lon_rows)
    sv.save_racing_driver_rows_to_db(ps.racing_driver_rows)
    sv.save_loop_sector_details_rows_to_db(ps.loop_sector_details_rows)

    # commit changes to db
    sv.commit_db_changes()

    
