from pysqlite2 import dbapi2 as sqlite

def Render_Frame_Traces(gtfs, frame, frame_data):

  busses = frame_data["busses"]
  abus = busses[1]
  
  get_one_bus_trace(gtfs, frame_data["data"][abus])
  
def get_one_bus_trace(gtfs, end_data):
  connection = sqlite.connect(gtfs)
  cursor = connection.cursor()
  
  shape       = end_data["shape"]
  end_dist    = end_data["dist"]
  
  sql = """SELECT 
      *
  FROM shapes
  WHERE 
        shapes.shape_id = %(shape)d
    AND shapes.distance < %(ed)f
  """ % {"shape": shape, "ed": end_dist}
  
  cursor.execute(sql)
  
  for row in cursor:
    print row
   
  cursor.close()
