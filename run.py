#!/usr/bin/env python
import database
import datamine

# Location of the data:
folder = "/home/natronics/Data/TriMet/"
Trips = folder + "trips.txt"
Times = folder + "stop_times.txt"
Stops = folder + "stops.txt"
Shapes = folder + "shapes.txt"
Routs = folder + "routes.txt"

# Path and name of database
Database = "./trimet-gtfs.db"

print "Loading Database...\n"

# Uncomment this if you already created the database and want to startover clean
#database.Clean_Database(Database)

# Create the database
database.Create_Database(Database)

# Load the data
database.Load_Data(Database, trips=Trips, times=Times, stops=Stops, shapes=Shapes)


print "Mining the data...\n"

datamine.Build_Busses_Db(Database)

print "Processing frame %d" % 453

busses = datamine.Get_Buses_In_Frame(Database, 1262345400, 1262345500)

#print len(busses)

datamine.Get_Bus_Location(Database, busses[3], 1262345400, 1262345500)
