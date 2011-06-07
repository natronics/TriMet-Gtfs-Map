#!/usr/bin/env python
import datetime
import database
import datamine
import render
import matplotlib.pyplot as plt

# Location of the data:
folder = "/home/natronics/Data/TriMet/"
Trips = folder + "trips.txt"
Times = folder + "stop_times.txt"
Stops = folder + "stops.txt"
Shapes = folder + "shapes.txt"
Routs = folder + "routes.txt"

# Path and name of database
Database = "./trimet-gtfs.db"

Frames = "./frames.db"

print "Loading Database...\n"

# Uncomment this if you already created the database and want to startover clean
#database.Clean_Database(Database)

# Create the database
database.Create_Database(Database)

# Load the data
database.Load_Data(Database, trips=Trips, times=Times, stops=Stops, shapes=Shapes)

print "Mining Some Data...\n"

# Do some processing
busses = datamine.Build_Busses_Db(Database)

framedata = {}

# Start processing frames
print "Processing Frame Data:"

# figure out frame times

animation_begin_time = datetime.datetime.strptime("2011-01-01 03:30:00", "%Y-%m-%d %H:%M:%S")
animation_end_time = datetime.datetime.strptime("2011-01-01 10:00:00", "%Y-%m-%d %H:%M:%S")
speed = 50 # seconds per frame
animation_length = (animation_end_time - animation_begin_time).seconds
number_of_frames = int(animation_length / speed)


# Whole system
top_corner = (45.68, -123.32)
bot_corner = (45.25, -122.2301)

# Downtown
#top_corner = (45.5416, -122.7042)
#bot_corner = (45.4943, -122.6308)

r = render.render(top_corner, bot_corner)

# do frame
for frame_no in range(1, number_of_frames + 1):
  print "  + Frame %d out of %d" % (frame_no, number_of_frames)
  
  # Figure frame time
  frame_begin_time  = animation_begin_time + datetime.timedelta(seconds=(speed*(frame_no-1)))
  frame_end_time    = animation_begin_time + datetime.timedelta(seconds=(speed*(frame_no)))
  
  framedata = datamine.frame(Database, busses, frame_begin_time, frame_end_time)
  #print framedata 
  
  r.Render_Frame_Traces(Database, frame_no, framedata)
  #r.Render_Frame_Point(frame_no, framedata)
