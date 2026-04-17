# instalacion_model.py
# Modelo de instalaciones.

# Importar módulos de Django.
from django.db import models

# Modelo de instalación.
class Instalacion( models.Model ):
    id_instalacion: int = models.AutoField( primary_key=True )
    nombre: str = models.CharField( max_length=50 )
    direccion: str = models.CharField( max_length=100, blank=True, null=True )

    class Meta:
        db_table = 'instalaciones'
