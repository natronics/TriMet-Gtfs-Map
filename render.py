from pysqlite2 import dbapi2 as sqlite
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches

class render:

  fig = {}
  border = []
  
  xax = 0
  yax = 0
  
  def __init__(self, top_corner, bot_corner):
    self.border = (top_corner, bot_corner)
    
    grid_x = (bot_corner[1] - top_corner[1]) * 0.701375935
    grid_y = (top_corner[0] - bot_corner[0])

    xax = 10
    yax = 10
    if grid_x < grid_y:
      xax = 10 / (grid_y/float(grid_x))
    else:
      yax = 10 / (grid_x/float(grid_y))
      
    self.xax = xax
    self.yax = yax

    self.fig = plt.figure(figsize=(xax,yax), frameon=False)
  
  def pick_color(self, route):
    if   route == 90:  return "#ff5555"   # red
    elif route == 100: return "#4499ee"   # blue
    elif route == 190: return "#eedd44"   # yellow
    elif route == 200: return "#55cc44"   # green
   
    return "#e7e7e7"
    
  def Render_Frame_Traces(self, gtfs, frame, frame_data):

    busses = frame_data["busses"]
    
    ax = plt.axes([0,0,1,1])
   
    Path = mpath.Path
    pathdata = [
       (   Path.MOVETO, (self.border[0][1], self.border[0][0])),
       (   Path.LINETO, (self.border[0][1], self.border[1][0])),
       (   Path.LINETO, (self.border[1][1], self.border[1][0])),
       (   Path.LINETO, (self.border[1][1], self.border[0][0])),
       (Path.CLOSEPOLY, (self.border[0][1], self.border[0][0])),
    ]

    codes, verts = zip(*pathdata)
    path = mpath.Path(verts, codes)
    patch = mpatches.PathPatch(path, facecolor='black', alpha=0.3)
    ax.add_patch(patch)
      
    for bus in busses:
      lats, lons = get_one_bus_trace(gtfs, frame_data["data"][bus])
      c = self.pick_color(frame_data["data"][bus]["route"])
      ax.plot(lons, lats, '-', solid_capstyle='butt', color=c, linewidth=0.8, alpha=0.4)

    
    ax.axis([self.border[0][1], self.border[1][1], self.border[1][0], self.border[0][0]])
    plt.axis('off')

    plt.savefig("frames/traces/%04d" % frame, dpi=192, Transparent='Transparent')
    plt.clf()

  def Render_Frame_Point(self, frame, frame_data):
    busses = frame_data["busses"]
    
    self.fig = plt.figure(figsize=(self.xax, self.yax), frameon=False)
    ax = plt.axes([0,0,1,1])

    for bus in busses:
      end_point = frame_data["data"][bus]["end_point"]
      lat = end_point["lat"]
      lon = end_point["lon"]
      ax.plot(lon, lat, '.', color="#eeeeee", markersize=0.8)
    ax.axis([self.border[0][1], self.border[1][1], self.border[1][0], self.border[0][0]])
    plt.axis('off')
    plt.savefig("frames/points/%04d" % frame, dpi=192, Transparent='Transparent')
    plt.close()
    
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
