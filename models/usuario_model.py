# persona_model.py
# Modelo de personas.

# Importar módulos de Django.
from django.db import models

# Importar modelos de relación.
from models.persona_model import Persona
from models.rol_model import Rol

# Modelo de usuario.
class Usuario( models.Model ):
    id_usuario: int = models.AutoField( primary_key=True )
    persona: Persona = models.ForeignKey( Persona, models.DO_NOTHING, db_column='id_persona', blank=True, null=True )
    correo: str = models.CharField( max_length=100, blank=True, null=True )
    password: str = models.CharField( max_length=100, blank=True, null=True )
    rol: Rol = models.ForeignKey( Rol, models.DO_NOTHING, db_column='id_rol', blank=True, null=True )

    class Meta:
        db_table = 'usuarios'
