from pysqlite2 import dbapi2 as sqlite

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
  GROUP BY times.trip_id
  """
  cursor.execute(sql)
  for row in cursor:
    trip        = row[0]
    begin_time  = row[1]
    end_time    = row[2]
    busses[trip] = {"begin": begin_time, "end": end_time}
  cursor.close()

  return busses

"""
0 (1975040, u'2011-01-01 15:50:00', u'2011-01-01 16:44:00')
1 (1975070, u'2011-01-01 20:43:00', u'2011-01-01 21:53:00')
2 (1975079, u'2011-01-01 23:35:00', u'2011-01-02 00:36:00')
"""

def frame(gtfs, frame):

  # Get list of active trips
  connection = sqlite.connect(gtfs)
  cursor = connection.cursor()

  time = "06:31:02"
  sql = """
  SELECT
      times.trip_id
    , times.arrival_time
  FROM times
  WHERE  (
        times.arrival_time      <= datetime('2011-01-01 %(time)s')
    AND times.stop_sequence = 1)
  GROUP BY times.trip_id
  
  UNION
  
  SELECT
      times.trip_id
    , times.arrival_time
  FROM times
  WHERE  
        times.arrival_time      >= datetime('2011-01-01 %(time)s')
  GROUP BY times.trip_id
  """ % {"time": time}
  
  cursor.execute(sql)

  trips = []

  i = 0
  for row in cursor:
    print i, row
    i = i + 1

  cursor.close()
