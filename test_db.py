#!/usr/bin/env python
from pysqlite2 import dbapi2 as sqlite

Database = "./trimet-gtfs.db"

connection = sqlite.connect(Database)
cursor = connection.cursor()

sql = """SELECT 
      *, strftime('%s', times.departure_time)
  FROM  times
  ORDER BY times.arrival_time DESC
  LIMIT 50;
"""

cursor.execute(sql)

for row in cursor:
  print row

cursor.close()
