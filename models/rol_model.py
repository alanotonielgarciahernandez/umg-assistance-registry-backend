# rol_model.py
# Modelo de roles.

from enum import Enum

# Importar módulos de Django.
from django.db import models

class Roles( Enum ):
    ADMIN = 1
    CATEDRATICO = 2
    ESTUDIANTE = 3

class Rol( models.Model ):
    id_rol = models.AutoField( primary_key=True )
    nombre = models.CharField( max_length=50 )
    descripcion = models.CharField( max_length=100, blank=True, null=True )

    class Meta:
        db_table = 'roles'
