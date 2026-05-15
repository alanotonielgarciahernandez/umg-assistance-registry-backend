# validar_JWT.py
# Validación de JWT en rutas protegidas.

# Importar módulos de terceros.
from ninja_jwt.tokens import AccessToken

# Importar middlewares.
from middlewares.validate_role import validateRole

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

        # Verificar que el rol del usuario en el token sea válido.
        if validateRole( user ) is False:
            return None
    except Exception as e:
        print( f"Error al validar el token JWT: { e }" )
        return None

    return user
