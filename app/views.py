from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView
from .models import Sensores, Ambientes, Historico
from .serializers import SensoresSerializer, AmbientesSerializer, HistoricoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
import pandas as pd
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AmbientesFilter, SensoresFilter, HistoricoFilter
from rest_framework.views import APIView
from django.http import Http404, JsonResponse
from rest_framework.response import Response
from .utils import ler_excel, exportar_sensores, normalizar_status, exportar_ambientes, exportar_excel


def mostrar_excel(request):
    df = pd.read_excel('meuarquivo.xlsx')
    return JsonResponse(df.to_dict(orient='records'), safe=False)

class SensoresListCreate(ListCreateAPIView):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SensoresFilter

class SensoresRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


# Mostra uma mensagem sempre que um sensor for deletado do banco de dados
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"Sensor excluído do banco de dados"})

# verifica se o sensor passado como parãmetro para o usuário existe no banco de dados
    def get_object(self):
        try:
            return super().get_object()
        except Exception:
        # Mostra uma mensagem de erro para o usuário
            raise Http404({'Erro': 'Sensor não encontrado no banco de dados'})
        
# Views dos ambientes
class AmbientesListCreate(ListCreateAPIView):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AmbientesFilter

class AmbientesRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

#------------------
#pegar do filters.py para filtrar o sig do ambiente
# class AmbienteListView(generics.ListAPIView):
#     queryset = Ambientes.objects.all()
#     serializer_class = AmbientesSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = AmbientesFilter


# Mostra uma mensagem sempre que um ambiente for deletado do banco de dados
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"Ambiente excluído do banco de dados"})

# verifica se o ambiente passado como parãmetro para o usuário existe no banco de dados
    def get_object(self):
        try:
            return super().get_object()
        except Exception:
        # Mostra uma mensagem de erro para o usuário
            raise Http404({'Erro': 'Ambiente não encontrado no banco de dados'})
        

# Views dos Históricos
class HistoricoListCreate(ListCreateAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HistoricoFilter
    

class HistoricoRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


# Mostra uma mensagem sempre que um sensor for deletado do banco de dados
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"Registro excluído do banco de dados"})
    
    
# verifica se o sensor passado como parãmetro para o usuário existe no banco de dados
    def get_object(self):
        try:
            return super().get_object()
        except Exception:
        # Mostra uma mensagem de erro para o usuário
            raise Http404({'Erro': 'Registro não encontrado no banco de dados'})
        
class Importar_Dados(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        resultado = ler_excel(request)
        return Response(resultado)
    

class Exportar_Dados(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        exportar_excel(request)
        return Response({"mensagem": "Dados exportados com sucesso"})

        
#filtros de sensores
