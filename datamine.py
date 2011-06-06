from pysqlite2 import dbapi2 as sqlite
import datetime

def interp(a,b,val):
  slope = float(b[1] - a[1]) / float(b[0] - a[0])
  inter = a[1] - slope * a[0]
  return (val * slope) + inter
  
def Build_Busses_Db(gtfs_db):
  temp_db = "./temp.db"
  connection = sqlite.connect(gtfs_db)
  cursor = connection.cursor()
  
  busses = {}


  sql = """SELECT
      times.trip_id
    , MIN(times.arrival_time) AS begin_time
    , MAX(times.arrival_time) AS end_time
  FROM times
  JOIN trips ON (trips.trip_id = times.trip_id)
  WHERE
    (   trips.service_id = 'A.302'
    OR  trips.service_id = 'W.302'
    )
  GROUP BY times.trip_id
  """
  cursor.execute(sql)
  for row in cursor:
    trip        = row[0]
    begin_time  = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
    end_time    = datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
    busses[trip] = {"begin": begin_time, "end": end_time}
  cursor.close()

  return busses

"""
0 (1975040, u'2011-01-01 15:50:00', u'2011-01-01 16:44:00')
1 (1975070, u'2011-01-01 20:43:00', u'2011-01-01 21:53:00')
2 (1975079, u'2011-01-01 23:35:00', u'2011-01-02 00:36:00')
"""

def get_bus_position(gtfs, trip, time):
  connection = sqlite.connect(gtfs)
  cursor = connection.cursor()
  sql = """
    SELECT 
        trips.shape_id
      , before.arrival_time
      , before.shape_dist_traveled
      , after.arrival_time
      , after.shape_dist_traveled
      , shapes.distance
      , shapes.lat
      , shapes.lon
    FROM trips
    JOIN (
            SELECT
                times.trip_id
              , times.arrival_time
              , times.departure_time
              , times.shape_dist_traveled
              , strftime('%%s', times.arrival_time) - strftime('%%s', '%(time)s') AS timediff
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
              , strftime('%%s', times.arrival_time) - strftime('%%s', '%(time)s') AS timediff
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
  """ % {"time": time.isoformat(), "trip": trip}
  cursor.execute(sql)
  
  dist = []
  lats = []
  lons = []
  shape_id = 0
  frame_dist = 0
  frame_lat = 0
  frame_lon = 0
  for row in cursor:
    shape_id      = int(  row[0])
    before_t      =       row[1]
    before_dist   = float(row[2])
    after_t       =       row[3]
    after_dist    = float(row[4])
    shape_dist    = float(row[5])
    lat           = float(row[6])
    lon           = float(row[7])
    dist.append(shape_dist)
    lats.append(lat)
    lons.append(lon)
  #print before_t, before_dist, after_t, after_dist, dist

  if len(dist) > 0:
    # Interpolate to the distace along the shape where this time is
    before_t = datetime.datetime.strptime(before_t, "%Y-%m-%d %H:%M:%S")
    before_t = int(before_t.strftime("%s"))
    after_t  = datetime.datetime.strptime(after_t, "%Y-%m-%d %H:%M:%S")
    after_t  = int(after_t.strftime("%s"))

    frame_dist = interp((before_t,before_dist), (after_t,after_dist), int(time.strftime("%s")))
    
    # Interpolate to the point where that distance is
    dist = sorted(dist)
    for i, d in enumerate(dist):

      if d >= frame_dist:
        frame_dist, d, dist
        break
    
    frame_lat = 0
    frame_lon = 0
    if i == 0:
      frame_lat = lats[0]
      frame_lon = lons[0]
    else:
      frame_lat = interp((dist[i-1], lats[i-1]), (dist[i], lats[i]), frame_dist)
      frame_lon = interp((dist[i-1], lons[i-1]), (dist[i], lons[i]), frame_dist)
  
  # return results
  return shape_id, {"dist": frame_dist, "lat": frame_lat, "lon":frame_lon}
     
def frame(gtfs, busses, begin_datetime, end_datetime):
  
  frame_data = {}
  
  # Get list of active trips
  active_busses = []
  for trip in busses:
    if busses[trip]["begin"] <= begin_datetime and busses[trip]["end"] >= begin_datetime:
      active_busses.append(trip)

  # Get beggining positions
  for trip in active_busses:
    shape, begin_point  = get_bus_position(gtfs, trip, begin_datetime)
    shape, end_point    = get_bus_position(gtfs, trip, end_datetime)
    frame_data[trip] = {"shape": shape, "begin_point": begin_point, "end_point": end_point}

  return {"busses": active_busses, "data": frame_data}
