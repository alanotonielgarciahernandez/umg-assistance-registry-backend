from django.db import models

class Instalaciones(models.Model):
    id_instalacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'instalaciones'