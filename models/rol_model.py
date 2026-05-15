# rol_model.py
# Modelo de roles.

# Importar módulos de Django.
from django.db import models

# Modelo de rol.
class Rol( models.Model ):
    id_rol: int = models.AutoField( primary_key=True )
    nombre: str = models.CharField( max_length=50 )
    descripcion: str = models.CharField( max_length=100, blank=True, null=True )

    class Meta:
        db_table = 'roles'
