import pymysql
from datetime import datetime
import pytz

endpoint = 'tratardadosbd.cf7azvdl423r.us-east-1.rds.amazonaws.com'
username = 'admin'
password = 'lzqld7n7el1OyNmGJsCg'
database_name = 'DADOS'

UTC = pytz.utc
dataLocal = pytz.timezone('America/Recife')
diaHorario = str(datetime.now(dataLocal))

dataHoje = diaHorario[:10]
dataAmanha = int(diaHorario[8:10])+1 
dataAmanha = diaHorario[:8]+str(dataAmanha)

if len(dataAmanha) == 9:
    dataAmanha = dataAmanha[:8]+'0'+dataAmanha[-1]

connection = pymysql.connect(
        host='tratardadosbd.cf7azvdl423r.us-east-1.rds.amazonaws.com',
        user='admin', 
        password = "lzqld7n7el1OyNmGJsCg",
        db='DADOS',
        )
queryMysql = "select SUM(CHUVA) from dadosTratados where CHUVA IS NOT NULL and createdAt >= '"+dataHoje[0:10]+" 03:00:00' and createdAt <= '"+dataAmanha[0:10]+" 02:59:59';"

def lambda_handler(event, context):
    cursor = connection.cursor()
    cursor.execute(queryMysql)
    rows = cursor.fetchall()
    resposta = "{ 'VALOR_OBSERVADO': " + str(rows[0][0])+ " }"
    return resposta
