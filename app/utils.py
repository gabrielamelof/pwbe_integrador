# # import pandas as pd 
# # from .models import Sensores

# # ambientes = pd.ler_excel('excel/ambientes.xlsx')
# # contador = pd.ler_excel('excel/contador.xlsx')

# # for _, row ambientes.iterrows():
# #     Sensores.objects.create(
# #         sig=row['sig']
# #         descricao=row['descricao']
# #         ni=row['ni']
# #         responsavel=row['responsavel']
# #     )

# import os
# import openpyxl
# from .models import Sensores, Ambientes, Historico

# pasta = 'excel'

# # Função genérica para carregar um Excel
# def carregar_excel(caminho_arquivo):
#     wb = openpyxl.load_workbook(pasta)
#     return wb.active  # aba ativa

# # 1. Ambientes
# ws = carregar_excel_ambientes(os.path.join(pasta, 'ambientes.xlsx'))
# for row in ws.iter_rows(min_row=2, values_only=True):
#     sig, descricao, ni, responsavel = row
#     if sig:
#         Ambiente.objects.get_or_create(
#             sig = sig,
#             defaults = {
#                 'descricao': descricao,
#                 'ni': ni,
#                 'responsavel': responsavel
#             }
#         )

# # 2. Contador
# ws = carregar_excel(os.path.join(pasta, 'contador.xlsx'))
# for row in ws.iter_rows(min_row=2, values_only=True):
#     data, valor = row
#     if data and valor is not None:
#         Contador.objects.create(data=data, valor=valor)

# # 3. Histórico
# ws = carregar_excel(os.path.join(pasta, 'historico.xlsx'))
# for row in ws.iter_rows(min_row=2, values_only=True):
#     nome_ambiente, data, evento = row
#     ambiente = Ambiente.objects.filter(nome=nome_ambiente).first()
#     if ambiente:
#         Historico.objects.create(ambiente=ambiente, data=data, evento=evento)

# # 4. Luminosidade
# ws = carregar_excel(os.path.join(pasta, 'luminosidade.xlsx'))
# for row in ws.iter_rows(min_row=2, values_only=True):
#     nome_ambiente, valor, data = row
#     ambiente = Ambiente.objects.filter(nome=nome_ambiente).first()
#     if ambiente:
#         Luminosidade.objects.create(ambiente=ambiente, valor=valor, data=data)

# # 5. Temperatura
# ws = carregar_excel(os.path.join(pasta, 'temperatura.xlsx'))
# for row in ws.iter_rows(min_row=2, values_only=True):
#     nome_ambiente, valor, data = row
#     ambiente = Ambiente.objects.filter(nome=nome_ambiente).first()
#     if ambiente:
#         Temperatura.objects.create(ambiente=ambiente, valor=valor, data=data)

# # 6. Umidade
# ws = carregar_excel(os.path.join(pasta, 'umidade.xlsx'))
# for row in ws.iter_rows(min_row=2, values_only=True):
#     nome_ambiente, valor, data = row
#     ambiente = Ambiente.objects.filter(nome=nome_ambiente).first()
#     if ambiente:
#         Umidade.objects.create(ambiente=ambiente, valor=valor, data=data)

# print("Importação concluída com sucesso!")

import os
import pandas as pd
from .models import Ambientes, Historico, Sensores
from django.http import JsonResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # pasta onde está o script
arquivo_excel = os.path.join(BASE_DIR, 'excel', 'ambientes.xlsx')

#arquivo = r'C:\Users\45526185800\Desktop\integrador_pwbe\app\excel\ambientes.xlsx'

def ler_excel(request):
    df = pd.read_excel(arquivo_excel)
    #importados os ambientes
    for _, row in df.iterrows():
        criar_ambiente(
            sig=row['sig'],
            descricao=row['descricao'],
            ni=row['ni'],
            responsavel=row['responsavel']
        )
    # data = df.to_dict(orient='records')
    # ambiente = criar_ambiente(45874, "aluno", "F123R", "Gabriela Melo")
    # print(ambiente)
    return JsonResponse({'mensagem': 'ambientes importados com sucesso!'})

def criar_ambiente(sig, descricao, ni, responsavel):
    ambiente = Ambientes.objects.create(
        sig=sig,
        descricao=descricao,
        ni=ni,
        responsavel=responsavel
    )
    return ambiente


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # pasta onde está o script
arquivo_historico = os.path.join(BASE_DIR, 'excel', 'histórico.xlsx')

#arquivo = r'C:\Users\45526185800\Desktop\integrador_pwbe\app\excel\ambientes.xlsx'

def ler_historico(request):
    df = pd.read_excel(arquivo_historico)
    #importados os ambientes
    for _, row in df.iterrows():
        criar_historico(
            sensor=row['sensor'],
            ambiente=row['ambiente'],
            valor=row['valor'],
            timestamp=row['timestamp']
        )
    # data = df.to_dict(orient='records')
    # ambiente = criar_ambiente(45874, "aluno", "F123R", "Gabriela Melo")
    # print(ambiente)
    return JsonResponse({'mensagem': 'Históricos importados com sucesso!'})

def criar_historico(sensor, ambiente, valor, timestamp):
    historico = Historico.objects.create(
        sensor=sensor,
        ambiente=ambiente,
        valor=valor,
        timestamp=timestamp
    )
    return historico

# ---------------------------------------------------------------------------------------

def ler_sensores(request):
    df = pd.read_excel(arquivo_historico)
    #importados os ambientes
    for _, row in df.iterrows():
        criar_historico(
            sensor=row['sensor'],
            ambiente=row['ambiente'],
            valor=row['valor'],
            timestamp=row['timestamp']
        )
    # data = df.to_dict(orient='records')
    # ambiente = criar_ambiente(45874, "aluno", "F123R", "Gabriela Melo")
    # print(ambiente)
    return JsonResponse({'mensagem': 'Históricos importados com sucesso!'})

def criar_sensores(sensor, ambiente, valor, timestamp):
    historico = Historico.objects.create(
        sensor=sensor,
        ambiente=ambiente,
        valor=valor,
        timestamp=timestamp
    )
    return historico


     


# def importar_dados_excel(pasta):
#     mensagens = []

#     # Importar ambientes.xlsx
#     df_amb = pd.read_excel(os.path.join(pasta, 'ambientes.xlsx'))
#     for _, row in df_amb.iterrows():
#         ambiente, created = Ambiente.objects.update_or_create(
#             sig=row['sig'],
#             defaults={
#                 'descricao': row['descricao'],
#                 'ni': row['ni'],
#                 'responsavel': row['responsavel']
#             }
#         )
#         mensagens.append(f"Ambiente {'criado' if created else 'atualizado'}: {row['sig']}")

#     # Importar historico.xlsx
#     df_hist = pd.read_excel(os.path.join(pasta, 'historico.xlsx'))
#     for _, row in df_hist.iterrows():
#         ambiente = Ambiente.objects.filter(sig=row['sig']).first()
#         if ambiente:
#             Historico.objects.create(
#                 ambiente=ambiente,
#                 data=row['data'],
#                 evento=row['evento']
#             )
#             mensagens.append(f"Histórico criado para {row['sig']} em {row['data']}")

#     # Importar sensores
#     tipos = ['temperatura', 'umidade', 'luminosidade', 'contador']
#     for tipo in tipos:
#         caminho = os.path.join(pasta, f'{tipo}.xlsx')
#         if os.path.exists(caminho):
#             df = pd.read_excel(caminho)
#             for _, row in df.iterrows():
#                 ambiente = Ambiente.objects.filter(sig=row['sig']).first()
#                 if ambiente:
#                     Sensor.objects.create(
#                         tipo=tipo,
#                         valor=row['valor'],
#                         data=row['data'],
#                         ambiente=ambiente
#                     )
#                     mensagens.append(f"{tipo.capitalize()} registrada para {row['sig']}")

#     return mensagens
