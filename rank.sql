SELECT *
FROM (
	SELECT
	driver_number,
	lap_number,
	lap_loop_sector_time,
	max(lap_loop_sector_number),
	dense_rank () OVER (
	PARTITION BY lap_number
	ORDER BY lap_loop_sector_time ASC
	) TimeRank
	FROM
	driver_lap
	GROUP BY 1,2
	)
WHERE TimeRank = 1
