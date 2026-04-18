# validar_rol.py
# Validación de rol en rutas protegidas.

# Importar modelos.
from models.rol_model import Roles
from models.usuario_model import Usuario

def validateRole( user: Usuario, allowed_role: list[ Roles ] ) -> bool:
    # Validar que el rol del usuario esté en la lista de roles permitidos.
    if user.rol.id_rol not in [ role.value for role in allowed_role ]:
        return False
    
    return True