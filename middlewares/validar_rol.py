# validar_rol.py
# Validación de rol en rutas protegidas.

# Importar modelos.
from models.rol_model import Roles
from models.usuario_model import Usuario

def validateRole( user: Usuario, allowed_role: Roles ):
    if user.rol.id_rol != allowed_role.value:
        print( f'Usuario con rol { user.rol.id_rol }, se esperaba { allowed_role.value }' )
        return False
    return True