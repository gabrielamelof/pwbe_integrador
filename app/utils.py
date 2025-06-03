import os
import re
import io
import zipfile
import pandas as pd
from .models import Ambientes, Historico, Sensores
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # pasta onde está o script
umidade_excel = os.path.join(BASE_DIR, 'excel', 'umidade.xlsx')
contador_excel = os.path.join(BASE_DIR, 'excel', 'contador.xlsx')
luminosidade_excel = os.path.join(BASE_DIR, 'excel', 'luminosidade.xlsx')
temperatura_excel = os.path.join(BASE_DIR, 'excel', 'temperatura.xlsx')

#excel de ambientes
ambientes_excel = os.path.join(BASE_DIR, 'excel', 'ambientes.xlsx')

#excel de historico
historico_excel = os.path.join(BASE_DIR, 'excel', 'historico.xlsx')
#arquivo = r'C:\Users\45526185800\Desktop\integrador_pwbe\app\excel\ambientes.xlsx'

def ler_excel(request):
    ler_excel_sensores()
    ler_excel_ambientes()
    ler_excel_historico()
    return "Dados das planilhas importados com sucesso!"


def ler_excel_sensores():
    df = pd.concat([pd.read_excel(umidade_excel),
                    pd.read_excel(luminosidade_excel),
                    pd.read_excel(contador_excel),
                    pd.read_excel(temperatura_excel)])
    #print(df)



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
        
        # print(sensor)

def ler_excel_ambientes():
    df = pd.concat([pd.read_excel(ambientes_excel)])
    #print(df)

    for _, row in df.iterrows():
        ambiente = criar_ambiente(
            sig = row['sig'],
            descricao = row['descricao'],
            ni = row['ni'],
            responsavel = row['responsavel'],
        )
        
        print(ambiente)

def ler_excel_historico():
    df = pd.concat([pd.read_excel(historico_excel)])
    #print(df)

    for _, row in df.iterrows():
        historico = criar_historico(
            sensor = row['sensor'],
            ambiente = row['ambiente'],
            valor = row['valor'],
            timestamp = row['timestamp'],
        )
        
    #     print(historico)



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
        descricao=descricao,
        ni=ni,
        responsavel=responsavel
    )
    return ambiente

def criar_historico(sensor, ambiente, valor, timestamp):
    sensor_obj = get_object_or_404(Sensores, id=sensor)
    ambiente_obj = get_object_or_404(Ambientes, id=ambiente)

    historico = Historico.objects.create(
        sensor=sensor_obj,
        ambiente=ambiente_obj,
        valor=valor,
        timestamp=timestamp
    )
    return historico

def exportar_sensores(request):
    todos_sensores = Sensores.objects.all().values()
    items = []
    
    for sensor in todos_sensores:
        print(sensor.values())
        items.append(list(sensor.values()))
    
    df = pd.DataFrame(items)
    
    response = HttpResponse(content="application/vnd.ms-excel")
    response['Content-Disposition'] = f'attachment; filename="output.csv"'
    
    df.to_csv(response, header=['id', 'sensor', 'mac_address', 'und_med', 'latitude', 'longitude', 'status'], index=False, sep=';', encoding='utf-8-sig')
    
    return response

# def exportar_ambientes(request):
#     todos_ambientes = Ambientes.objects.all().values()
#      df = pd.
#     items = []
    
#     for ambiente in todos_ambientes:
#         item = [
#             str(ambiente['id']),
#             str(ambiente['sig']).strip(),
#             limpar_texto(ambiente['descricao']),
#             limpar_texto(ambiente['ni']),
#             limpar_texto(ambiente['responsavel']),
#         ]
#         items.append(item)
#         # items.append(list(ambiente.values()))
    
#     df = pd.DataFrame(items)
    
#     response = HttpResponse(content_type="text/csv")
#     response['Content-Disposition'] = f'attachment; filename="ambientes.csv"'
#     df.to_csv(response, header=['id', 'sig', 'descricao', 'ni', 'responsavel'], index=False, sep=';', encoding='utf-8')
    
#     return response


# -----------------------------------------------------------------------------

# def criar_historico(request):
#     historico = Historico.objects.create(
        
#     )




# def criar_sensores(sensor, mac_address, unidade_med, latitude, longitude, status):
#     sensor = Sensores.objects.create(
#         sensor=sensor,
#         mac_address = mac_address,
#         unidade_med = unidade_med,
#         latitude = latitude,
#         longitude = longitude,
#         status = status
#     )
#     return sensor

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

def limpar_texto(texto):
    if pd.isna(texto):
        return ''
    
    texto = str(texto)
    # Remove BOM, espaços não separáveis, etc.
    texto = texto.replace('\ufeff', '')  # BOM (Byte Order Mark)
    texto = texto.replace('\xa0', ' ')   # Espaço não separável
    #texto = re.sub(r'\s+', ' ', texto)   # Remove espaços duplicados
    return texto.strip()
    # return str(texto).replace('\xa0', ' ').strip()


#exportar historico
def exportar_historico(request):
    historico = Historico.objects.all().values()
    df = pd.DataFrame(list(historico))
    return df

#exportar ambientes
def exportar_ambientes(request):
    ambientes = Ambientes.objects.all().values()
    df = pd.DataFrame(list(ambientes))
    return df

#exportar sensores
def exportar_sensores(request):
    todos_sensores = Ambientes.objects.all().values()
    df = pd.DataFrame(list(todos_sensores))
    return df

def exportar_excel(request):
    # arquivo zip
    zip_buffer = io.BytesIO()  

    # abrir e escrever dentro do arquivo
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        # Exportar ambientes
        ambientes = Ambientes.objects.all().values()
        df_ambientes = pd.DataFrame(ambientes)
        ambiente_csv = io.StringIO()
        
        # abre o arquivo para colocar dentro, ele salva e cria
        df_ambientes.to_csv(ambiente_csv, index=False, sep=';')
        zf.writestr('ambientes.csv', ambiente_csv.getvalue())

        # Exportar sensores
        sensores = Sensores.objects.all().values()
        df_sensores = pd.DataFrame(sensores)
        sensores_csv = io.StringIO()
        df_sensores.to_csv(sensores_csv, index=False, sep=';')
        zf.writestr('sensores.csv', sensores_csv.getvalue())

        #exportar historico
        historico = Historico.objects.all().values()
        df_historico = pd.DataFrame(historico)
        historico_csv = io.StringIO()

        df_historico.to_csv(historico_csv, index=False, sep=';')
        zf.writestr('historico.csv', historico_csv.getvalue())

    zip_buffer.seek(0)

    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="dados.zip"'
    return response