from django.db import models

# Create your models here.
class TranslateProduct(models.Model):
    equipo = models.CharField(max_length=255, unique=True)
    stok = models.CharField(max_length=255)
    iva = models.CharField(max_length=255)
    active = models.CharField(max_length=255)

