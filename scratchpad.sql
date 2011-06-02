sql1 = """

  SELECT 
     *
  FROM  trips
  JOIN (
    SELECT 
        trips.trip_id AS trip_id
      , COUNT(times.stop_id) AS stops
      , MIN(times.arrival_time) AS begin_time
      , MAX(times.departure_time) AS end_time
    FROM  trips
    JOIN times ON (times.trip_id = trips.trip_id)
    GROUP BY trips.trip_id
    ) AS busruns ON (busruns.trip_id = trips.trip_id)
  WHERE 
    (   trips.service_id = 'A.302'
    OR  trips.service_id = 'W.302'
    )
  ORDER BY trips.trip_id ASC
"""

time = "06:31:02"
sql2 = """
  SELECT
      *
  FROM trips
  JOIN times    ON (    times.trip_id             = trips.trip_id)
  JOIN shapes   ON (    shapes.shape_id           = trips.shape_id
                    AND shapes.distance           = times.shape_dist_traveled)
  JOIN times AS begintime 
                ON (    begintime.trip_id         = trips.trip_id
                    AND begintime.stop_sequence   = 1)
  WHERE 
        trips.trip_id = 1962252
    AND times.arrival_time      >= datetime('2011-01-01 %s')
    AND begintime.arrival_time  <= datetime('2011-01-01 %s')
""" % (time, time)


sql3 = """
  SELECT
      trips.trip_id
    , times.arrival_time
    , times.departure_time
    , times.shape_dist_traveled
    , (strftime('%%s', times.arrival_time) - strftime('%%s', '2011-01-01 %(time)s')) AS Timediff
  FROM trips
  JOIN times      ON (    times.trip_id             = trips.trip_id)
  JOIN times AS begintime 
                ON (    begintime.trip_id         = trips.trip_id
                    AND begintime.stop_sequence   = 1)
  WHERE 
        trips.trip_id = 1962252
    AND Timediff <= 0
  ORDER BY Timediff DESC
  LIMIT 1
""" % {"time": time}


sql4 = """
  SELECT
      times.trip_id
    , times.arrival_time
    , times.departure_time
    , times.shape_dist_traveled
    , MIN(strftime('%%s', times.arrival_time) - strftime('%%s', '2011-01-01 %(time)s')) AS Timediff
  FROM times
  WHERE 
        times.trip_id IN (1962252, 1963965)
        AND strftime('%%s', times.arrival_time) - strftime('%%s', '2011-01-01 %(time)s') > 0
  GROUP BY times.trip_id
""" % {"time": time}

sql5 = """
  SELECT 
      trips.trip_id
    --, before.arrival_time
    , after.arrival_time
    , after.timediff
    --, shapes.*
  FROM trips
  JOIN  (
            SELECT
                times.trip_id
              , times.arrival_time
              , times.departure_time
              , times.shape_dist_traveled
              , MIN(strftime('%%s', times.arrival_time) - strftime('%%s', '2011-01-01 %(time)s')) AS timediff
            FROM times
            WHERE strftime('%%s', times.arrival_time) - strftime('%%s', '2011-01-01 %(time)s') > 0
            GROUP BY times.trip_id
        ) AS after ON (after.trip_id = trips.trip_id)
  WHERE 
      trips.trip_id IN (1962252, 1963965)
""" % {"time": time}
