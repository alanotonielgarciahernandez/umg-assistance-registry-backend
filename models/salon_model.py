from django.db import models
from .instalacion_model import Instalaciones

class Salones(models.Model):
    id_salon = models.AutoField(primary_key=True)
    id_instalacion = models.ForeignKey(Instalaciones, models.DO_NOTHING, db_column='id_instalacion')
    nombre = models.CharField(max_length=100)
    nivel = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'salones'