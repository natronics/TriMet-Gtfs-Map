#!/usr/bin/env python
from pysqlite2 import dbapi2 as sqlite

Database = "./trimet-gtfs.db"

connection = sqlite.connect(Database)
cursor = connection.cursor()

time = "06:31:02"

sql1 = """
  SELECT
      times.trip_id
    , times.arrival_time
    , times.departure_time
    , times.shape_dist_traveled
    , strftime('%%s', times.arrival_time) - strftime('%%s', '2011-01-01 %(time)s') AS timediff
  FROM times
  WHERE 
        times.trip_id = 1962252
        AND strftime('%%s', times.arrival_time) - strftime('%%s', '2011-01-01 %(time)s') > 0
  LIMIT 1
""" % {"time": time}

trip = 1962252
sql2 = """
  SELECT 
    *
  FROM trips
  JOIN (
          SELECT
              times.trip_id
            , times.arrival_time
            , times.departure_time
            , times.shape_dist_traveled
            , strftime('%%s', times.arrival_time) - strftime('%%s', '2011-01-01 %(time)s') AS timediff
          FROM times
          WHERE 
                    times.trip_id = %(trip)s
                AND timediff > 0
          ORDER BY timediff ASC
          LIMIT 1
        ) AS after ON (after.trip_id = trips.trip_id)
  JOIN ( 
          SELECT
              times.trip_id
            , times.arrival_time
            , times.departure_time
            , times.shape_dist_traveled
            , strftime('%%s', times.arrival_time) - strftime('%%s', '2011-01-01 %(time)s') AS timediff
          FROM times
          WHERE 
                    times.trip_id = %(trip)s
                AND timediff <= 0
          ORDER BY timediff DESC
          LIMIT 1
        ) AS before ON (after.trip_id = trips.trip_id)
  JOIN shapes ON (    shapes.shape_id = trips.shape_id
                  AND shapes.distance >= before.shape_dist_traveled
                  AND shapes.distance <= after.shape_dist_traveled)
  WHERE trips.trip_id = %(trip)s
""" % {"time": time, "trip": trip}

sql3 = """SELECT
      times.trip_id
    , times.arrival_time AS time
    , ending.time
  FROM times
  JOIN  (
            SELECT
                times.trip_id
              , MAX(times.arrival_time) AS time
            FROM times
            GROUP BY times.trip_id
        ) AS ending ON (ending.trip_id = times.trip_id)
  WHERE
    times.stop_sequence = 1
    AND times.trip_id IN (1975070,1975079,1975040)
    """

sql4 = """SELECT
      times.trip_id
    , MIN(times.arrival_time) AS begin_time
    , MAX(times.arrival_time) AS end_time
  FROM times
  WHERE times.trip_id = 1961857
  GROUP BY times.trip_id
"""

sql5 = """SELECT
    * 
  FROM times
  JOIN trips ON (trips.trip_id = times.trip_id)
  WHERE times.trip_id = 1961857
"""
    
cursor.execute(sql5)

i = 0
for row in cursor:
  print i, row
  i = i + 1

cursor.close()
