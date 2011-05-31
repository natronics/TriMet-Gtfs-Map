#!/usr/bin/env python
from pysqlite2 import dbapi2 as sqlite

Database = "./trimet-gtfs.db"

connection = sqlite.connect(Database)
cursor = connection.cursor()

sql = """SELECT 
      *
    , trips.route_id
  FROM  trips
  LIMIT 50;
"""

cursor.execute(sql)

for row in cursor:
  print row

cursor.close()
