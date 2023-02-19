import pyodbc
import pandas as pd

drivers = pyodbc.drivers()
print(drivers)

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=team.soluciondigital.com.co;DATABASE=Stok;UID=sa;PWD=Soluciondig2015')

cursor = conn.cursor()

cursor.execute("SELECT * FROM dbo.Productos")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()