from pysqlite2 import dbapi2 as sqlite
import matplotlib.pyplot as plt

def Render_Frame_Traces(gtfs, frame, frame_data, fig):

  # Whole system
  top_corner = (45.68, -123.32)
  bot_corner = (45.25, -122.2301)

  # Downtown
  #top_corner = (45.5416, -122.7042)
  #bot_corner = (45.4943, -122.6308)

  busses = frame_data["busses"]
  
  ax = fig.add_subplot(111)
  
  for bus in busses:
    lats, lons = get_one_bus_trace(gtfs, frame_data["data"][bus])
    ax.plot(lons, lats)
  
  ax.axis([top_corner[1], bot_corner[1], bot_corner[0], top_corner[0]])

  plt.savefig("frames/traces/%04d" % frame, dpi=90)
  plt.clf()
  
def get_one_bus_trace(gtfs, bus):
  connection = sqlite.connect(gtfs)
  cursor = connection.cursor()
  
  shape        = bus["shape"]
  begin_point  = bus["begin_point"]
  end_point    = bus["end_point"]
  
  lats = []
  lons = []
  
  lat = begin_point["lat"]
  lon = begin_point["lon"]
  if lat != 0 and lon != 0:
      lats.append(lat)
      lons.append(lon)
  
  #print begin_dist, end_dist
  
  
  sql = """SELECT 
      shapes.lat
    , shapes.lon
  FROM shapes
  WHERE 
        shapes.shape_id = %(shape)d
    AND shapes.distance > %(bd)f
    AND shapes.distance < %(ed)f
  """ % {"shape": shape, "bd": begin_point["dist"], "ed": end_point["dist"]}
  
  cursor.execute(sql)
  
  for row in cursor:
    lat = float(row[0])
    lon = float(row[1])
    if lat != 0 and lon != 0:
      lats.append(lat)
      lons.append(lon)
  
  lat = end_point["lat"]
  lon = end_point["lon"]
  if lat != 0 and lon != 0:
      lats.append(lat)
      lons.append(lon)
  cursor.close()
  
  return lats, lons
