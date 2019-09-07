from mysql.connector import (connection)
from . import Instrument

cnx = connection.MySQLConnection(user='root', password='fernandok4',
                                 host='127.0.0.1',
                                 database='marketcap')

def insertCotacao(id_instrument, data, abertura, fechamento, variacao, minima, maxima, volume):
    cursor = cnx.cursor()
    cursor.execute("""INSERT IGNORE INTO tb_instrument_history_cotation(id_instrument, dt_trade, 
    vl_min, vl_max, vl_variation, vl_close, vl_open, qt_volume) 
    VALUES(%s, STR_TO_DATE(%s, '%d %b %Y'), %s, %s, %s, %s, %s, %s)""", (id_instrument, data, minima, maxima, variacao, 
    fechamento, abertura, volume))
    cnx.commit()
    cursor.close()

def getInstrumentsToSearch():
    cursor = cnx.cursor()
    cursor.execute("""
        SELECT id_instrument, nm_find_instrument FROM tb_instrument
    """)
    result = cursor.fetchall()
    instrumentList = []
    for (row) in result:
        instrument = Instrument.Instrument(row[0], str(row[1]))
        instrumentList.append(instrument)
    cursor.close()
    return instrumentList

    