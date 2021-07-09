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
queryMysql = "SELECT HORA, DC_NOME, CD_ESTACAO, VL_LATITUDE, VL_LONGITUDE, TEM_MAX FROM dadosTratados where TEM_MAX = (select MAX(TEM_MAX) from dadosTratados where TEM_MAX IS NOT NULL) and createdAt >= '"+dataHoje[0:10]+" 03:00:00' and createdAt <= '"+dataAmanha[0:10]+" 02:59:59';"

def lambda_handler(event, context):
    cursor = connection.cursor()
    cursor.execute(queryMysql)
    rows = cursor.fetchall()
    resposta = "{ 'CODIGO_ESTACAO': " + str(rows[0][2]) + ", 'NOME_ESTACAO: " + str(rows[0][1]) + ",'LATITUDE': " + str(rows[0][3]) + ", 'LONGITUDE': " + str(rows[0][4]) + ", 'HORARIO_COLETA': " + str(rows[0][0]) + ", 'VALOR_OBSERVADO': " + str(rows[0][5]) + "}"
    return resposta