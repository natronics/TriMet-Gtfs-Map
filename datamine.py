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

def interp(a,b,val):
  slope = float(b[1] - a[1]) / float(b[0] - a[0])
  inter = a[1] - slope * a[0]
  return (val * slope) + inter
  
def interpolate_table(x, y, x_0):
  for i, x_i in enumerate(x):
    #print i, x_i - 1262340000, x_0 - 1262340000
    if x_i >= x_0:
      break
  
  if x_i == x_0: return y[i]
  if i != 0:
    a = (x[i-1], y[i-1])
    b = (x[i], y[i])
    dist = interp(a,b,x_0)
    return dist
  #print i, x_i, x_0
  return 0
   
def Get_Bus_Location(gtfs_db, trip, begin_t, end_t):
  connection = sqlite.connect(gtfs_db)
  cursor = connection.cursor()
  
  sql = """SELECT
      strftime('%s', times.arrival_time) AS ar_time
    , strftime('%s', times.departure_time) AS de_time
    , times.shape_dist_traveled
  FROM trips
  JOIN times ON (times.trip_id = trips.trip_id)
  WHERE trips.trip_id = %d
   AND
   (    trips.service_id = 'A.302'
    OR  trips.service_id = 'W.302'
   )
  ORDER BY times.arrival_time ASC
  """ % ("%s", "%s", trip)
 
  cursor.execute(sql)
  
  times = []
  dists = []
  for row in cursor:
    ar_time  = int(  row[0])
    de_time  = int(  row[1])
    dist     = float(row[2])
    
    if ar_time == de_time:
      times.append(ar_time)
      dists.append(dist)
    else:
      print "stop"
    #print row
  
  #print times, dists
  
  dist_begin = interpolate_table(times, dists, begin_t)
  dist_end = interpolate_table(times, dists, end_t)
  
  #print dist_begin, dist_end
  
  sql = """SELECT
      shapes.lat
    , shapes.lon
    , shapes.distance
    , shapes.sequence
  FROM shapes
  JOIN trips ON (trips.shape_id = shapes.shape_id)
  WHERE trips.trip_id = %d
  ORDER BY shapes.sequence ASC
  """ % trip
  
  cursor.execute(sql)
  
  lats = []
  lons = []
  dists = []
  for row in cursor:
    lat = float(row[0])
    lon = float(row[1])
    dist = float(row[2])
    
    lats.append(lat)
    lons.append(lon)
    dists.append(dist)
    
    #print row
  cursor.close()
  
  lat_begin = interpolate_table(dists, lats, dist_begin)
  lon_begin = interpolate_table(dists, lons, dist_begin)
  
  lat_end = interpolate_table(dists, lats, dist_end)
  lon_end = interpolate_table(dists, lons, dist_end)
  
  lats_frame = []
  lons_frame = []
  lats_frame.append(lat_begin)
  lons_frame.append(lon_begin)
  for i, dist in enumerate(dists):
    if dist >= dist_begin and dist <= dist_end:
      lats_frame.append(lats[i])
      lons_frame.append(lons[i])
  lats_frame.append(lat_end)
  lons_frame.append(lon_end)
  
  """

  import matplotlib.pyplot as plt

  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.plot(lons, lats)
  
  ax.plot(lons_frame, lats_frame, 'r-')
  
  ax.plot(lons, lats, "g+")
  plt.show()
  """
  
  return lons_frame, lats_frame
