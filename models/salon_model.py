# salon_model.py
# Modelo de salones.

# Importar módulos de Django.
from django.db import models

# Importar modelos relacionados.
from models.instalacion_model import Instalacion

# Modelo de salon.
class Salon( models.Model ):
    id_salon: int = models.AutoField( primary_key=True )
    instalacion: Instalacion = models.ForeignKey( Instalacion, models.DO_NOTHING, db_column='id_instalacion', blank=True, null=True )
    nivel: str = models.CharField( max_length=20, blank=True, null=True )
    nombre: str = models.CharField( max_length=50, blank=True, null=True )

    # Metadatos del modelo.
    class Meta:
        db_table = 'salones'