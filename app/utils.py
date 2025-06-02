import os
import pandas as pd
from .models import Ambientes, Historico, Sensores
from django.http import JsonResponse, HttpResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # pasta onde está o script
ambientes_excel = os.path.join(BASE_DIR, 'excel', 'ambientes.xlsx')
umidade_excel = os.path.join(BASE_DIR, 'excel', 'umidade.xlsx')
contador_excel = os.path.join(BASE_DIR, 'excel', 'contador.xlsx')
luminosidade_excel = os.path.join(BASE_DIR, 'excel', 'luminosidade.xlsx')
temperatura_excel = os.path.join(BASE_DIR, 'excel', 'temperatura.xlsx')
#arquivo = r'C:\Users\45526185800\Desktop\integrador_pwbe\app\excel\ambientes.xlsx'

def ler_excel(request):
    ler_excel_sensores()
    return JsonResponse({'mensagem': 'Os dados das planilhas excel foram importados com sucesso!'})


def ler_excel_sensores():
    df = pd.concat([pd.read_excel(umidade_excel),
                    pd.read_excel(luminosidade_excel),
                    pd.read_excel(contador_excel),
                    pd.read_excel(temperatura_excel)])
    print(df)



    for _, row in df.iterrows():

        status_convertido = normalizar_status(row['status'])
        

        sensor = criar_sensores(
            sensor = row['sensor'],
            mac_address = row['mac_address'],
            unidade_med = row['unidade_medida'],
            latitude = row['latitude'],
            longitude = row['longitude'],
            status = status_convertido
        )
        
        print(sensor)

def ler_excel_ambientes():
     df = pd.concat([pd.read_excel(ambientes_excel)])
     print(df)


# ---------------------------------------------------------------------------------------


def criar_sensores(sensor, mac_address, unidade_med, latitude, longitude, status):
    sensor = Sensores.objects.create(
        sensor=sensor,
        mac_address = mac_address,
        unidade_med = unidade_med,
        latitude = latitude,
        longitude = longitude,
        status = status
    )
    return sensor

def criar_ambiente(sig, descricao, ni, responsavel):
    ambiente = Ambientes.objects.create(
        sig=sig,
        desc=descricao,
        ni=ni,
        responsavel=responsavel
    )
    return ambiente

def exportar_sensores(request):
    todos_sensores = Sensores.objects.all().values()
    items = []
    
    for sensor in todos_sensores:
        print(sensor.values())
        items.append(list(sensor.values()))
    
    df = pd.DataFrame(items)
    
    response = HttpResponse(content="application/vnd.ms-excel")
    response['Content-Disposition'] = f'attachment; filename="output.csv"'
    
    df.to_csv(response, header=['id', 'sensor', 'mac_address', 'und_med', 'latitude', 'longitude', 'status'], index=False, sep=';')
    
    return response


# -----------------------------------------------------------------------------

def criar_historico(request):
    historico = Historico.objects.create(
        
    )




def criar_sensores(sensor, mac_address, unidade_med, latitude, longitude, status):
    sensor = Sensores.objects.create(
        sensor=sensor,
        mac_address = mac_address,
        unidade_med = unidade_med,
        latitude = latitude,
        longitude = longitude,
        status = status
    )
    return sensor

def normalizar_status(valor):
    if isinstance(valor, bool):
        return 'ativo' if valor else 'inativo'

    if isinstance(valor, str):
        valor = valor.strip().lower()
        if valor in ['true', 'ativo']:
            return 'ativo'
        elif valor in ['false', 'inativo']:
            return 'inativo'

    return 'inativo'