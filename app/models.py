from django.db import models

# Create your models here.
class Sensores(models.Model):
    SENSORES_CHOICES = [
        ('U', 'Umidade'), 
        ('T', 'Temperatura'),
        ('L', 'Luminosidade'),
        ('C' , 'Contador')
    ]

    sensor = models.CharField(max_length=1, choices=SENSORES_CHOICES, default='T')
    mac_address = models.CharField(max_length=20)

    UNIDADE_CHOICES = [
        ('°C', '°C'),
        ('Lux', 'Lux'),
        ('%', '%'),
        ('Num', 'Num')
    ]

    unidade_med = models.CharField(max_length=3, choices=UNIDADE_CHOICES, default='°C')
    latitude = models.FloatField()
    longitude = models.FloatField()

    STATUS_CHOICES = [
        ('A', 'Ativo'),
        ('I', 'Inativo')
    ]

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')

    def __str__(self):
        return self.sensor


class Ambientes(models.Model):
    sig = models.IntegerField()
    descricao = models.CharField(max_length=255, blank=True, null=True)
    ni = models.CharField(max_length=20)
    responsavel = models.CharField(max_length=50)

    REQUIRED_FIELDS = ['sig', 'ni', 'responsavel']

    def __str__(self):
        return self.sig


class Historico(models.Model):
    sensor = models.ForeignKey(Sensores, on_delete=models.CASCADE)
    ambiente = models.ForeignKey(Ambientes, on_delete=models.CASCADE)
    valor = models.FloatField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.sensor



