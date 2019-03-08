SELECT *
FROM (
	SELECT
	dls.lap_number,
	rd.driver_lastname,
	dls.elapsed_time,
	dls.lap_time,
	(2700 - (dls.elapsed_time / 1000)) AS remaining_time,
	(2700 - (dls.elapsed_time / 1000)) / (dls.lap_time / 1000)+1 AS remaining_laps,
	rank () OVER (
	PARTITION BY dls.lap_number
	ORDER BY dls.elapsed_time ASC
	) lap_position
	FROM
	driver_lap_summary AS dls,
	racing_driver AS rd
	WHERE
	rd.driver_number == dls.driver_number
	ORDER BY 1,4
)