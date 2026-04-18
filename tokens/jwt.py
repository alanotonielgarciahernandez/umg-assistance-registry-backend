# jwt.py
# Script para generar tokens JWT.

# Importar módulos de Python.
from datetime import timedelta

# Importar módulos de terceros.
from ninja_jwt.tokens import AccessToken

# Importar modelos.
from models.usuario_model import Usuario

def generate_jwt( user: Usuario ) -> str | None:
    try:
        # Crear el token JWT con la información del usuario.
        access: AccessToken = AccessToken()
        access[ 'user_id' ] = user.id_usuario
        access[ 'correo' ] = user.correo
        access[ 'rol' ] = user.rol.id_rol
        access[ 'nombre' ] = user.persona.nombre
        access[ 'apellido' ] = user.persona.apellido
        access.set_exp( lifetime=timedelta( hours=24 ) )  # Establecer la expiración del token.
    except Exception:
        return None
    
    return str( access )
