# curso_model.py
# Modelo de cursos.

# Importar módulos de Django.
from django.db import models

# Importar modelos relacionados.
from models.salon_model import Salon
from models.persona_model import Persona

# Modelo de curso.
class Curso( models.Model ):
    id_asignacion: int = models.AutoField( primary_key=True )
    persona: Persona = models.ForeignKey( Persona, models.DO_NOTHING, db_column='id_persona', blank=True, null=True )
    nombre_curso: str = models.CharField( max_length=100, blank=True, null=True )
    horario: str = models.CharField( max_length=50, blank=True, null=True )
    salon: Salon = models.ForeignKey( Salon, models.DO_NOTHING, db_column='id_salon', blank=True, null=True )

    # Metadatos del modelo.
    class Meta:
        db_table = 'catedratico_cursos'