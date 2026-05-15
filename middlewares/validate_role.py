# validate_role.py
# Script para validar el rol del usuario durante el proceso de inicio de sesión.

# Importar modelo de usuario.
from models.usuario_model import Usuario

# Constante para el ID del rol de "catedrático".
ROL_CATEDRATICO = 2

def validateRole( usuario: Usuario ) -> bool:
    if usuario.rol.id_rol == ROL_CATEDRATICO:
        return True
    return False
