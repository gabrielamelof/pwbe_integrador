from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .models import Sensores, Ambientes, Historico
from .serializers import SensoresSerializer, AmbientesSerializer, HistoricoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.http import Http404
from rest_framework.response import Response

# Create your views here.
# Views dos sensores
class SensoresListCreate(ListCreateAPIView):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer
    permission_classes = [IsAuthenticated]

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

class AmbientesRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

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

        

