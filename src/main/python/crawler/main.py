import requests
import sys
import json
from bs4 import BeautifulSoup
import dao.crawlerDAO as dao

def translateDate(data):
    english = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    portuguese = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    mes = portuguese.index(str(str(data)[3:6]))
    stringValue = str(data).replace(portuguese[mes], english[mes])
    return stringValue

def readPageNmInstrumentFind(id_instrument, nm_instrument_find, current):
    url = "https://br.advfn.com/bolsa-de-valores/bovespa/{}/historico/mais-dados-historicos?current={}&Date1=01/01/12&Date2=25/10/19".format(str(nm_instrument_find), current)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    result = soup.find_all("tr", {"class":"result"})
    count = 0
    print(url)
    for (row) in result:
        children = row.findChildren("td" , recursive=False)
        data = translateDate(children[0].decode_contents(formatter="html")).strip()
        fechamento = children[1].decode_contents(formatter="html").replace(",", ".")
        variacao = children[2].decode_contents(formatter="html").replace(",", ".")
        abertura = children[4].decode_contents(formatter="html").replace(",", ".")
        maxima = children[5].decode_contents(formatter="html").replace(",", ".")
        minima = children[6].decode_contents(formatter="html").replace(",", ".")
        volume = children[7].decode_contents(formatter="html").replace(".", "")
        dao.insertCotacao(id_instrument, data, abertura, fechamento, variacao, minima, maxima, volume)
        count = count + 1
    return count

instruments = dao.getInstrumentsToSearch()
for (instrument) in instruments:
    current = 0
    finish = 0
    while(finish != 1):
        finish = readPageNmInstrumentFind(instrument.id_instrument, instrument.nm_find_instrument, current)
        current = current + 1