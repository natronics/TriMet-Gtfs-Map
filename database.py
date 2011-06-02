from pysqlite2 import dbapi2 as sqlite

# helpful, perhaps
def run_some_sql(connection, sql):
  cursor = connection.cursor()
  cursor.execute(sql)
  connection.commit()
  cursor.close()
  
# Build out the table structure
def Create_Database(database):
  connection = sqlite.connect(database)
  
  # Create the trips Table
  sql = """CREATE TABLE trips
  (   trip_id INTEGER PRIMARY KEY
    , route_id INTEGER
    , service_id VARCHAR(6)
    , direction_id INTEGER
    , block_id INTEGER
    , shape_id INTEGER
  );"""
  run_some_sql(connection, sql)
  
  # Create the times Table
  sql = """CREATE TABLE times
  (   trip_id INTEGER 
    , arrival_time DATETIME
    , departure_time DATETIME
    , stop_id INTEGER
    , stop_sequence INTEGER
    , shape_dist_traveled REAL
  );
  """
  run_some_sql(connection, sql)
  run_some_sql(connection, "CREATE INDEX times_trip_id_idx ON times(trip_id);")
  run_some_sql(connection, "CREATE INDEX times_arrival_time_idx ON times(arrival_time);")

  # Create the stops Table
  sql = """CREATE TABLE stops
  (   stop_id INTEGER PRIMARY KEY
    , stop_name VARCHAR(64)
    , stop_lat REAL
    , stop_lon REAL
  );"""
  run_some_sql(connection, sql)
  
  # Create the shapes Table
  sql = """CREATE TABLE shapes
  (   shape_id INTEGER
    , lat REAL
    , lon REAL
    , sequence INTEGER
    , distance REAL
  );"""
  run_some_sql(connection, sql)
  run_some_sql(connection, "CREATE INDEX shapes_shape_id_idx ON shapes(shape_id);")
  run_some_sql(connection, "CREATE INDEX times_distance_idx ON shapes(distance);")
  
def Clean_Database(database):
  connection = sqlite.connect(database)
  cursor = connection.cursor()
  cursor.execute("DROP TABLE trips;")
  cursor.execute("DROP TABLE times;")
  cursor.execute("DROP TABLE stops;")
  cursor.execute("DROP TABLE shapes;")
  connection.commit()
  cursor.close()

def Load_Data(database, trips=None, times=None, stops=None, shapes=None):
  connection = sqlite.connect(database)
  cursor = connection.cursor()
  
  # Load trips Data
  if trips != None:
    f_in = open(trips, 'r')
    for line in f_in:
      if line[0] != 'r' and line[0] != "\r":
        li = line.split(",")
        route_id      = int(li[0])
        service_id    = li[1]
        trip_id       = int(li[2])
        direction_id  = int(li[3])
        block_id      = int(li[4])
        shape_id      = int(li[5])
        cursor.execute('INSERT INTO trips VALUES (?, ?, ?, ?, ?, ?);', (trip_id , route_id, service_id, direction_id, block_id, shape_id))
    f_in.close()

  # Load times data
  if times != None:
    f_in = open(times, 'r')
    for line in f_in:
      if line[0] != 't' and line[0] != "\r":
        li = line.split(",")
        trip_id               = int(li[0].strip())
        arrival_time          = li[1].strip()
        departure_time        = li[2].strip()
        stop_id               = int(li[3].strip())
        stop_sequence         = int(li[4].strip())
        shape_dist_traveled   = float(li[8].strip())
        
        # fix times that are like 25:45:19
        if arrival_time != "":
          if int(arrival_time[0:2]) > 23:
             arrival_time = "2011-01-02 " + "%02d" % (int(arrival_time[0:2]) - 24) + arrival_time[2:]
          else:
            arrival_time = "2011-01-01 " + arrival_time
        if departure_time != "":
          if int(departure_time[0:2]) > 23:
             departure_time = "2011-01-02 " + "%02d" % (int(departure_time[0:2]) - 24) + departure_time[2:]
          else:
            departure_time = "2011-01-01 " + departure_time
        
        cursor.execute("INSERT INTO times VALUES (?, ?, ?, ?, ?, ?);", (trip_id , arrival_time, departure_time, stop_id, stop_sequence, shape_dist_traveled))
    f_in.close()
    
  # Load stops data
  if stops != None:
    f_in = open(stops, 'r')
    for line in f_in:
      if line[0] != 's' and line[0] != "\r":
        li = line.split(",")
        stop_id = li[0]
        name    = li[2]
        lat     = li[4]
        lon     = li[5]
        cursor.execute("INSERT INTO stops VALUES (?, ?, ?, ?);", (stop_id, name, lat, lon))
    f_in.close()
    
  # Load shapes data
  if shapes != None:
    f_in = open(shapes, 'r')
    for line in f_in:
      if line[0] != 's' and line[0] != "\r":
        li = line.split(",")
        shape_id  = int(  li[0].strip())
        lat       = float(li[1].strip())
        lon       = float(li[2].strip())
        seq       = int(  li[3].strip())
        dist      = float(li[4].strip())
        cursor.execute("INSERT INTO shapes VALUES (?, ?, ?, ?, ?);", (shape_id, lat, lon, seq, dist))
    f_in.close()
      
  connection.commit()
  cursor.close()

def Clean_Frames_Db(db):
  connection = sqlite.connect(db)
  cursor = connection.cursor()
  cursor.execute("DROP TABLE frames;")
  cursor.execute("DROP TABLE segments;")
  connection.commit()
  cursor.close()
  
def Create_Frames_Db(db):
  connection = sqlite.connect(db)
  
  # Create the frames Table
  sql = """CREATE TABLE frames
  (   frame INTEGER
    , bus_id INTEGER
    , route INTEGER
    , segment_id INTEGER PRIMARY KEY
  );"""
  run_some_sql(connection, sql)
  
  # Create the segment Table
  sql = """CREATE TABLE segments
  (   segment_id INTEGER
    , lat REAL
    , lon REAL
    , sequence INTEGER
  );"""
  run_some_sql(connection, sql)
