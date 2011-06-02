#!/usr/bin/env python
import database
import datamine
import frame

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

# Do some processing
busses = datamine.Build_Busses_Db(Database)

frame = 254

print "Processing Frame %d...\n" % frame

#datamine.frame(Database, busses, frame)
