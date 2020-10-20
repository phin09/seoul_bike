import sqlite3
import pandas as pd

con = sqlite3.connect('./db.sqlite3')
cur = con.cursor()
query = cur.execute(("select * from station"))
cols = [column[0] for column in query.description]
bike_load = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
con.close()

print(type(bike_load))
print(bike_load)
