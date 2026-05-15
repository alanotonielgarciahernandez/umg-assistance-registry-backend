# validate_role.py
# Script para validar el rol del usuario durante el proceso de inicio de sesión.

# Importar módulos de Python.
import os

# Importar modelo de usuario.
from models.usuario_model import Usuario

def validateRole( usuario: Usuario ) -> bool:
    if usuario.rol.id_rol == int( os.getenv( 'ROL_CATEDRATICO', 2 ) ):
        return True
    return False
