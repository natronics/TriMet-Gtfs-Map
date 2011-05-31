#!/usr/bin/env python
import database

# Location of the data:
folder = "/home/natronics/Data/TriMet/"
Shapes = folder + "shapes.txt"
Trips = folder + "trips.txt"
Routs = folder + "routes.txt"
Times = folder + "stop_times.txt"
Stops = folder + "stops.txt"


# Path and name of database
Database = "./trimet-gtfs.db"

# Uncomment this if you already created the database and want to startover clean
database.Clean_Database(Database)

# Create the database
database.Create_Database(Database)

# Load the data
database.Load_Data(Database, trips=Trips)
