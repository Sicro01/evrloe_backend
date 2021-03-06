SELECT *
FROM (
	SELECT
	dls.lap_number,
	dls.driver_number,
	rd.driver_lastname,
	dls.elapsed_time,
	rank () OVER (
	PARTITION BY dls.lap_number
	ORDER BY dls.elapsed_time ASC
	) lap_position
	FROM
	driver_lap_summary AS dls,
	racing_driver AS rd
	WHERE
	rd.driver_number == dls.driver_number	
	GROUP BY 1,2,3
)

