from pysqlite2 import dbapi2 as sqlite

def Render_Frame(db, frame):
  connection = sqlite.connect(db)
  cursor = connection.cursor()
  
  sql = """SELECT 
      * 
  FROM frames 
  JOIN segments ON (segments.segment_id = frames.segment_id)
  ;"""
  cursor.execute(sql)
  
  for row in cursor:
    print row
   
  cursor.close()
