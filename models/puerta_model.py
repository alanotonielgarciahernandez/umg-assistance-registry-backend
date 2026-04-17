# puerta_model.py
# Modelo de puertas.

# Importar módulos de Python.
from datetime import datetime

# Importar módulos de Django.
from django.db import models

# Importar modelos relacionados.
from models.instalacion_model import Instalacion
from models.persona_model import Persona

# Modelo de puerta.
class Puerta( models.Model ):
    id_puerta: int = models.AutoField( primary_key=True )
    instalacion: Instalacion = models.ForeignKey( Instalacion, models.DO_NOTHING, db_column='id_instalacion' )
    nombre: str = models.CharField( max_length=50 )

    class Meta:
        managed = False
        db_table = 'puertas'

# Modelo de Puerta Principal.
class PuertaPrincipal( models.Model ):
    id_registro: int = models.AutoField( primary_key=True )
    persona: Persona = models.ForeignKey( Persona, models.DO_NOTHING, db_column='id_persona', blank=True, null=True )
    fecha_hora: datetime = models.DateTimeField( blank=True, null=True )
    imagen_capturada: str = models.CharField( max_length=255, blank=True, null=True )
    puerta: Puerta = models.ForeignKey( Puerta, models.DO_NOTHING, db_column='id_puerta', blank=True, null=True )

    class Meta:
        managed = False
        db_table = 'registro_puerta_principal'