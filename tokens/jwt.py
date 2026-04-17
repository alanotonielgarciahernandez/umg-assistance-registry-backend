# jwt.py
# Script para generar tokens JWT.

# Importar módulos de terceros.
from datetime import timedelta

from ninja_jwt.tokens import AccessToken

def generate_jwt( user ):
    try:
        access = AccessToken()
        access[ 'user_id' ] = user.id_usuario
        access[ 'correo' ] = user.correo
        access[ 'rol' ] = user.rol.id_rol
        access[ 'nombre' ] = user.persona.nombre
        access[ 'apellido' ] = user.persona.apellido
        access.set_exp( lifetime=timedelta( hours=24 ))  # Establecer la expiración del token.
    except Exception as e:
        print( f'Error al generar JWT: { e }' )
        return None
    
    return str( access )
