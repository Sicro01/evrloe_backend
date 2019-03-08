SELECT dl.driver_number, dl.lap_number, dl.lap_loop_sector_number, dl.lap_loop_sector_time FROM driver_lap dl
INNER JOIN
	(SELECT driver_number, lap_number, lap_loop_sector_time, max(lap_loop_sector_number) AS maxloop
	FROM driver_lap
	WHERE lap_loop_sector_key = 'loopSectors'
	GROUP BY driver_number) AS gdl
ON dl.driver_number = gdl.driver_number
AND dl.lap_loop_sector_number = gdl.maxloop
AND dl.lap_loop_sector_time = gdl.lap_loop_sector_time
AND dl.lap_number = gdl.lap_number


