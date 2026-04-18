# validar_JWT.py
# Validación de JWT en rutas protegidas.

# Importar módulos de terceros.
from ninja_jwt.tokens import AccessToken

# Importar modelo de usuario.
from models.usuario_model import Usuario

def validateJWT( auth_header: str ) -> Usuario | None:
    # Validar que el encabezado de autorización tenga el formato correcto.
    if not auth_header.startswith( 'Bearer' ):
        return None

    # Extraer el token del encabezado de autorización.
    token: str = auth_header[ 6: ].strip()
    if not token:
        return None
        
    try:
        # Validar ACCESS token.
        access_token: AccessToken = AccessToken( token )
        access_token.verify()

        # Verificar que el usuario en el token exista en la base de datos.
        user: Usuario = Usuario.objects.get( id_usuario = access_token[ 'user_id' ] )
    except Exception:
        return None

    return user