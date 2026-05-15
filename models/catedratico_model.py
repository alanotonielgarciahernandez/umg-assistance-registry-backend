# catedratico_model.py
# Modelo de catedráticos.

# Importar módulos de Django.
from django.db import models

# Importar modelos relacionados.
from models.persona_model import Persona

# Modelo de catedrático.
class Catedratico( models.Model ):
    id_catedratico: int = models.AutoField( primary_key=True )
    persona: Persona = models.ForeignKey( Persona, models.DO_NOTHING, db_column='id_persona' )

    # Metadatos del modelo.
    class Meta:
        db_table = 'catedraticos'
