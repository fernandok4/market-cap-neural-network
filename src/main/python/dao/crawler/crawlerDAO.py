import mysql.connector

class DAO:
    connection = mysql.connector.connect(user='root', password='fernandok4',
                                  host='127.0.0.1',
                                  database='marketcap')
    cursor = connection.cursor()
    
    def insertHistoryCotation():
        cursor.execute("SELECT 1")