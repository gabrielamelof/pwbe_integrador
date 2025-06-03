import django_filters
from .models import Sensores, Ambientes, Historico

#filtrar pelo sig do ambiente
class AmbientesFilter(django_filters.FilterSet):
    sig = django_filters.NumberFilter(field_name="sig", lookup_expr="icontains") #pega o valor exato

    class Meta:
        model = Ambientes
        fields = ['sig']

# Filtrar o sensor por seu tipo
class SensoresFilter(django_filters.FilterSet):
    sensor = django_filters.CharFilter(field_name="sensor", lookup_expr="exact") #pega o valor exato

    class Meta:
        model = Sensores
        fields = ['sensor']


class HistoricoFilter(django_filters.FilterSet):
    timestamp = django_filters.CharFilter(field_name="timestamp", lookup_expr="icontains") #pega o valor exato

    class Meta:
        model = Historico
        fields = ['timestamp']
