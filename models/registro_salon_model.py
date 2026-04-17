from django.db import models
from .salon_model import Salones
from .persona_model import Persona  # 👉 Corregido a 'Persona' sin la 's'

class RegistroIngresoSalon(models.Model):
    id_registro = models.AutoField(primary_key=True)
    id_salon = models.ForeignKey(Salones, models.DO_NOTHING, db_column='id_salon')
    id_persona = models.ForeignKey(Persona, models.DO_NOTHING, db_column='id_persona', blank=True, null=True) # 👉 Corregido a 'Persona'
    fecha_hora = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'registro_ingreso_salon'