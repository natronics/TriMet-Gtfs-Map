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


print "Mining the data...\n"

#datamine.Build_Busses_Db(Database)

# Uncomment this if you already created the database and want to startover clean
#database.Clean_Frames_Db(Frames)

# Create a database to store the mined data
database.Create_Frames_Db(Frames)

print "Processing frame %d" % 453

busses = datamine.Get_Buses_In_Frame(Database, 1262345400, 1262345500)

#print len(busses)

segment = datamine.Get_Bus_Location(Database, busses[3], 1262345400, 1262345500)

datamine.Push_Frame(Database, Frames, 342, busses[3], segment)

print "Rendering frame %d" % 453

frame.Render_Frame(Frames, 453)
