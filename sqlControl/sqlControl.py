import pyodbc
import pandas as pd

class Sql_conexion:

    def __init__(self,query):
        self.server = 'team.soluciondigital.com.co'
        self.bd = 'Stok'
        self.bd2 = 'TipsII'
        self.usuario = 'sa'
        self.contraseña = 'Soluciondig2015'

        self.conn_key = ('Driver= {ODBC Driver 17 for SQL Server};'
                    f'Server={self.server};'
                    f'Database={self.bd};'
                    f'UID={self.usuario};'
                    f'PWD={self.contraseña}'
                )

        self.query = query

        self.conn = pyodbc.connect(self.conn_key)
        self.conn.setdecoding(pyodbc.SQL_CHAR, encoding='latin-1')
        self.conn.setencoding('latin-1')
        self.data = pd.read_sql_query(self.query, self.conn)
    
    def get_data(self):
        return self.data
