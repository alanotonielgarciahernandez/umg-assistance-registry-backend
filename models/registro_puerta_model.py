from django.db import models
from .puerta_model import Puertas
from .persona_model import Persona 

class RegistroPuertaPrincipal(models.Model):
    id_registro = models.AutoField(primary_key=True)
    id_puerta = models.ForeignKey(Puertas, models.DO_NOTHING, db_column='id_puerta')
    # null=True porque el PDF dice que a veces entran "Desconocidos"
    id_persona = models.ForeignKey(Persona, models.DO_NOTHING, db_column='id_persona', blank=True, null=True) # 👉 Ya está corregido a 'Persona'
    fecha_hora = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'registro_puerta_principal'