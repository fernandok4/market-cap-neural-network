import requests
import sys
import json
from crawler.main import dao

print(sys.version)
url = "https://api.cotacoes.uol.com/asset/interday/list/years/?format=JSON&fields=price,high,low,open,volume,close,bid,ask,change,pctChange,date&item=484&"
req = requests.get(url, headers = {"Referer": "https://economia.uol.com.br/cotacoes/bolsas/acoes/bvsp-bovespa/petr4-sa"})
if req.status_code == 200:
    print('Requisição bem sucedida!')
    jsonFormat = req.json()
    marketData = jsonFormat['docs']
    print(marketData[0])