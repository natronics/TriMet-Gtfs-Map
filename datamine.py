from pysqlite2 import dbapi2 as sqlite
import os as os

temp_db = "./datamine.db"

def Build_Busses_Db(gtfs_db):
  global temp_db
  connection = sqlite.connect(gtfs_db)
  cursor = connection.cursor()
  
  sql = """SELECT
      trips.trip_id
    , trips.route_id
    , trips.shape_id
    , strftime('%s', times.arrival_time) AS ar_time
    , strftime('%s', times.departure_time) AS de_time
    , times.shape_dist_traveled
  FROM trips
  JOIN times ON (times.trip_id = trips.trip_id)
  WHERE 
        trips.service_id = 'A.302'
    OR  trips.service_id = 'W.302'
  """
  
  cursor.execute(sql)
  
  # Catagorize into busses
  busses = {}
  for row in cursor:
    trip = row[0]
    route = row[1]
    shape = row[2]
    ar_time = row[3]
    de_time = row[4]
    sh_dist = row[5]
    if trip not in busses:
      times = []
      times.append(int(ar_time))
      times.append(int(de_time))
      dist = []
      dist.append(float(sh_dist))
      data = {}
      data["times"] = times
      data["route"] = route
      data["shape"] = shape
      data["dists"] = dist
      busses[trip] = data
    else:
      times = busses[trip]["times"]
      times.append(int(ar_time))
      times.append(int(de_time))
      dist = busses[trip]["dists"]
      dist.append(float(sh_dist))
      busses[trip]["times"] = times
      busses[trip]["dists"] = dist
  
  cursor.close()
  
  try:
    os.remove(temp_db)
  except:
    pass
  connection = sqlite.connect(temp_db)
  cursor = connection.cursor()
  sql = """CREATE TABLE busses
  (   trip_id INTEGER 
    , begin_time DATETIME
    , end_time DATETIME
  );"""
  cursor.execute(sql)
  connection.commit()
  cursor.close()
  
  cursor = connection.cursor()
  for bus in busses:
    data = busses[bus]
    times = sorted(data["times"])
    
    cursor.execute('INSERT INTO busses VALUES (?, ?, ?);', (bus , times[0], times[-1]))
    
    """print bus, 
    print data["route"], 
    print data["shape"],
    
    times = sorted(data["times"])
    print times[0],
    print times[-1],
    
    dists = sorted(data["dists"])
    print dists[0],
    print dists[-1],
    
    print ""
    """
  connection.commit()
  cursor.close()

def Get_Buses_In_Frame(gtfs_db, begin_t, end_t):
  global temp_db
  
  connection = sqlite.connect(temp_db)
  cursor = connection.cursor()

  sql = """SELECT 
      busses.trip_id
    , busses.begin_time
    , busses.end_time
  FROM busses
  WHERE busses.begin_time <= %d AND busses.end_time >= %d
  """ % (begin_t, end_t)

  cursor.execute(sql)

  busses = []
  for row in cursor:
    trip_id = row[0]
    busses.append(trip_id)

  cursor.close()
  return busses

def Get_Bus_Location(gtfs_db, trip, begin_t, end_t):
  connection = sqlite.connect(gtfs_db)
  cursor = connection.cursor()
  
  sql = """SELECT
      strftime('%s', times.arrival_time) AS ar_time
    , strftime('%s', times.departure_time) AS de_time
    , times.shape_dist_traveled
  FROM trips
  JOIN times ON (times.trip_id = trips.trip_id)
  WHERE trips.trip_id = %s
   AND
   (    trips.service_id = 'A.302'
    OR  trips.service_id = 'W.302'
   )
  ORDER BY times.arrival_time ASC
  """ % ("%s", "%s", trip)
 
  cursor.execute(sql)
  
  for row in cursor:
    ar_time = row[0]
    de_time = row[1]
    dist = row[2]
    
    #print row
    
  cursor.close()
