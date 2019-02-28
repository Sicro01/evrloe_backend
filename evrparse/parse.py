import json
from pathlib import Path


def parse_logfile(data_folder, input_log_filename, race_name):
    # open source data file
    log_data_folder = Path(data_folder + '/Source/' + race_name)
    log_file_full_path = log_data_folder / input_log_filename
    log_file = open(log_file_full_path, 'r').read()

    data = []
    date_times = []

    with open(log_file_full_path) as f:
        for line in f:
            date_times.append(line[:26])
            data.append(json.loads(line[29:]))

    cnt = 0
    current_lap_num = 0
    status_rows = []
    gps_lat_lon_rows = []
    rgps_lat_lon_rows = []
    weather_items = []
    weather_rows = []
    analysis_pitdetails_items = []
    analysis_pitdetails_rows = []
    liveevents_pitdetails_items = []
    liveevents_pitdetails_rows = []
    loop_sector_details_items = []
    loop_sector_details_rows = []
    power_mode_items = []
    power_mode_rows = []

    for line in data:

        for line_key, line_value in line.items():

            if line_key == 'gps':

                for driver_key, driver_value in line_value.items():

                    for status_lat_lon_key, status_lat_lon_value in driver_value.items():

                        if status_lat_lon_key == 'status':

                            status_row = [date_times[cnt], line_key, status_lat_lon_key, driver_key,
                                          status_lat_lon_value]
                            status_rows.append(status_row)

                        elif status_lat_lon_key in ['lat', 'lon']:

                            if status_lat_lon_key == 'lat':

                                gps_lat_lon_row = [date_times[cnt], line_key, driver_key,
                                                   status_lat_lon_key, status_lat_lon_value]

                            else:

                                gps_lat_lon_row.extend([status_lat_lon_key, status_lat_lon_value])
                                gps_lat_lon_rows.append(gps_lat_lon_row)

            elif line_key == 'rgps':

                for driver_key, driver_value in line_value.items():

                    for rgps_lat_lon_key, rgps_lat_lon_value in driver_value.items():

                        if rgps_lat_lon_key in ['lat', 'lon']:

                            if rgps_lat_lon_key == 'lat':

                                rgps_lat_lon_row = [date_times[cnt], line_key, driver_key,
                                                    rgps_lat_lon_key, rgps_lat_lon_value]

                            else:

                                rgps_lat_lon_row.extend([rgps_lat_lon_key, rgps_lat_lon_value])
                                rgps_lat_lon_rows.append(rgps_lat_lon_row)

            elif line_key == 'weather':

                weather_items = []

                for current_data_key, current_data_value in line_value.items():

                    if current_data_key == 'currentData':

                        for environment_key, environment_value in current_data_value.items():
                            weather_item = [environment_key, environment_value]
                            weather_items.extend(weather_item)

                        weather_items = [date_times[cnt], line_key] + weather_items
                        weather_rows.append(weather_items)

            elif line_key == 'timing':

                for timing_key, timing_value in line_value.items():

                    if timing_key == 'liveEvents':

                        liveevents_pitdetails_items = []

                        for liveevents_pitin_key, liveevents_pitin_value in timing_value.items():

                            for liveevents_pitdetails_key, liveevents_pitdetails_value in liveevents_pitin_value.items():
                                liveevents_pitdetails_item = [liveevents_pitdetails_key, liveevents_pitdetails_value]
                                liveevents_pitdetails_items.extend(liveevents_pitdetails_item)

                            liveevents_pitdetails_items = [date_times[cnt], line_key, timing_key, liveevents_pitin_key] \
                                                          + liveevents_pitdetails_items
                            liveevents_pitdetails_rows.append(liveevents_pitdetails_items)

                    if timing_key == 'analysis':

                        for lap_key, lap_value in timing_value.items():

                            if lap_key == 'laps':

                                for driver_key, driver_details_value in lap_value.items():

                                    for timing_details_key, timing_details_value in driver_details_value.items():

                                        if timing_details_key == 'laps':

                                            for driver_number_key, driver_number_details in timing_details_value.items():

                                                for loop_sectors_key, loop_sectors_value in driver_number_details.items():

                                                    if loop_sectors_key == 'lapNum':
                                                        lap_num = loop_sectors_value
                                                        current_lap_num = loop_sectors_value

                                                    if loop_sectors_key == 'driverLapNum':
                                                        driver_lap_num = loop_sectors_value

                                                    if loop_sectors_key in ['loopSectors', 'sectors']:

                                                        loop_sector_details_items = []

                                                        for loop_sector_key, loop_sector_value in loop_sectors_value.items():

                                                            loop_sector_details_items = []

                                                            for loop_sector_details_key, loop_sector_details_value in \
                                                                    loop_sector_value.items():
                                                                loop_sector_details_item = [loop_sector_details_key,
                                                                                            loop_sector_details_value]
                                                                loop_sector_details_items.extend(
                                                                    loop_sector_details_item)

                                                            loop_sector_details_items = [date_times[cnt], line_key,
                                                                                         lap_key, loop_sectors_key,
                                                                                         driver_key, driver_lap_num,
                                                                                         lap_num,
                                                                                         loop_sector_key] + loop_sector_details_items
                                                            loop_sector_details_rows.append(loop_sector_details_items)

            elif line_key == 'telemEvent':

                for driver_key, driver_value in line_value.items():

                    for power_mode_key, power_mode_details in driver_value.items():
                        power_mode_item = [power_mode_key, power_mode_details]
                        power_mode_items.extend(power_mode_item)

                    power_mode_items = [date_times[cnt], driver_key, current_lap_num] + power_mode_items
                    power_mode_rows.append(power_mode_items)

        # increment line count so we pick up the right date_time
        cnt += 1

    # print outputs
    print('status_rows: ', len(status_rows))
    print('gps_lat_lon_rows: ', len(gps_lat_lon_rows))
    print('rgps_lat_lon_rows: ', len(rgps_lat_lon_rows))
    print('weather_rows: ', len(weather_rows))
    print('liveevents_pitdetails_rows', len(liveevents_pitdetails_rows))
    print('loop_sector_details_rows: ', len(loop_sector_details_rows))
    print('power_mode_rows: ', len(power_mode_rows))

#     [print('\n', x) for x in status_rows]
#     [print('\n', x) for x in gps_lat_lon_rows]
#     [print('\n', x) for x in rgps_lat_lon_rows]
#     [print('\n', x) for x in weather_rows]
#     [print('\n',x) for x in liveevents_pitdetails_rows]
#     [print('\n',x) for x in loop_sector_details_rows]
#     [print('\n',x) for x in power_mode_rows]

