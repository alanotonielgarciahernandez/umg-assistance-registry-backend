# registro_model.py
# Modelo de registro.

# Importar módulos de Python.
from datetime import date, datetime

# Importar módulos de Django.
from django.db import models

# Importar modelos relacionados.
from models.curso_model import Curso
from models.salon_model import Salon
from models.persona_model import Persona

# Modelo de asistencia.
class Asistencia( models.Model ):
    id_asistencia: int = models.AutoField( primary_key=True )
    curso: Curso = models.ForeignKey( Curso, models.DO_NOTHING, db_column='id_asignacion' )
    persona: Persona = models.ForeignKey( Persona, models.DO_NOTHING, db_column='id_persona' )
    fecha: date = models.DateField()
    estado: str = models.CharField( max_length=10 )
    confirmado_por: int = models.IntegerField( blank=True, null=True )
    fecha_confirmacion: datetime = models.DateTimeField( blank=True, null=True )

    # Metadatos del modelo.
    class Meta:
        db_table = 'registro_asistencia'

# Modelo de ingreso a salón.
class IngresoSalon( models.Model ):
    id_registro: int = models.AutoField( primary_key=True )
    persona: Persona = models.ForeignKey( Persona, models.DO_NOTHING, db_column='id_persona', blank=True, null=True )
    fecha_hora: datetime = models.DateTimeField( blank=True, null=True )
    ubicacion: str = models.CharField( max_length=50, blank=True, null=True )
    imagen_capturada: str = models.CharField( max_length=255, blank=True, null=True )
    salon: Salon = models.ForeignKey( Salon, models.DO_NOTHING, db_column='id_salon', blank=True, null=True )

    # Metadatos del modelo.
    class Meta:
        db_table = 'registro_ingreso_salon'