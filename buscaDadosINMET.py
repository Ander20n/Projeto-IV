import json
import requests
from datetime import datetime
import boto3
import pytz

dadosPernambuco = []
UTC = pytz.utc
dataLocal = pytz.timezone('America/Recife')
diaHorario = str(datetime.now(dataLocal))

def data_e_hora(data):
    dia = data[:10]
    hora = data[11:13] + "00"
    return dia, hora

def pegarDados(dia,hora):
    responseINMET = requests.get("https://apitempo.inmet.gov.br/estacao/dados/"+str(dia)+"/"+str(hora))
    return responseINMET
    
def isResponseValid(response):
    if response.status_code == 200:
        return True
    else:
        return print("Response is not valid " + str(response.status_code))

def filtroEstado(responseINMET):
    filtroEstado = responseINMET.json()
    return filter(lambda x: x["UF"] == "PE", filtroEstado)

def criarRecords(dadosFiltrados, hora):
    for informacao in dadosFiltrados:
        record = {
            'HORA': hora,
            'DC_NOME': informacao['DC_NOME'],
            'CD_ESTACAO': informacao['CD_ESTACAO'],
            'VL_LATITUDE': informacao['VL_LATITUDE'],
            'VL_LONGITUDE': informacao['VL_LONGITUDE'],
            'TEM_MAX': informacao['TEM_MAX'],
            'PRE_MIN': informacao['PRE_MIN'],
            'TEM_MIN': informacao['TEM_MIN'],
            'VEN_VEL': informacao['VEN_VEL'],
            'CHUVA': informacao['CHUVA']
        }
        dadosPernambuco.append(record)

def enviarDadosKinesis(dadosPernambuco):
    kinesis_client = boto3.client("kinesis", "us-east-1")
    kinesis_client.put_records(
        Records=[{
            'Data': json.dumps({"message_type": dadosPernambuco}),
            'PartitionKey': 'key'
        }],
        StreamName="recebendoDadosKDS",
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Enviado')
    }

def lambda_handler(event, context):
    
    data = diaHorario
    dia, hora = data_e_hora(data)
    responseINMET = pegarDados(dia,hora)
    
    if (isResponseValid(responseINMET)):
        dados = filtroEstado(responseINMET)
        criarRecords(dados,hora)
        asdf = enviarDadosKinesis(dadosPernambuco)
        return asdf