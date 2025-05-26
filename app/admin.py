from django.contrib import admin
from .models import Sensores, Ambientes, Historico

# Register your models here.

admin.site.register(Sensores)
admin.site.register(Ambientes)
admin.site.register(Historico)

