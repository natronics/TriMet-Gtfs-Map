from pysqlite2 import dbapi2 as sqlite

# A way to store a conceptual bus.
# Class bus # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class bus:

  trip_id = 0
  
  def __init__(self, trip):
    trip_id = trip
    
  def __cmp__(self, other):
    if other.trip_id == self.trip_id:
      return 0
    return 1

def Get_Data(database):
  connection = sqlite.connect(database)
  cursor = connection.cursor()
  
  sql = """SELECT 
      trips.route_id
    , trips.block_id
    , trips.shape_id
    , strftime('%s', times.departure_time)
    , times.shape_dist_traveled
  FROM  times
  JOIN  trips ON (trips.trip_id = times.trip_id)
  WHERE 
        trips.service_id = 'A.302'
    OR  trips.service_id = 'W.302'
  ORDER BY times.departure_time DESC
  LIMIT 50;
  """
  cursor.execute(sql)
  
  for row in cursor:
    print row
  
  cursor.close()
  
  return "neat"
