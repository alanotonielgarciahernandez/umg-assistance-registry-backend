# validar_JWT.py
# Validación de JWT en rutas protegidas.

# Importar módulos de terceros.
from ninja_jwt.tokens import AccessToken

# Importar modelo de usuario.
from models.usuario_model import Usuario

def validateJWT( token ):
    try:
        # Para rutas protegidas se valida el ACCESS token.
        access_token = AccessToken( token )
        access_token.verify()
    except Exception:
        return None
    
    # Verificar que el usuario en el token exista en la base de datos.
    try:
        user = Usuario.objects.get( id_usuario = access_token[ 'user_id' ] )
    except ( KeyError, Usuario.DoesNotExist ):
        return None

    return user