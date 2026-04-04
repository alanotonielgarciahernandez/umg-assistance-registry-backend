# validar_JWT.py
# Validación de JWT en rutas protegidas.

# Importar módulos de Django.
from django.http import JsonResponse

# Importar módulos de JWT.
from ninja_jwt.tokens import AccessToken

# Importar modelo de usuario.
from models.usuario_model import Usuarios

def validateJWT( request ):
    # Validar que el encabezado de autorización esté presente.
    auth_header = request.headers.get( 'Authorization' )
    if not auth_header:
        return JsonResponse( { 'detail': 'El encabezado de autorización es requerido.' }, status=401 )

    # Validar que el encabezado de autorización tenga el formato correcto.
    if not auth_header.startswith( 'Bearer' ):
        return JsonResponse( { 'detail': 'Formato inválido. Use "Bearer<token>".' }, status=401 )

    # Extraer el token del encabezado de autorización.
    token = auth_header[ 6: ].strip()
    if not token:
        return JsonResponse( { 'detail': 'Token no proporcionado.' }, status=401 )

    try:
        # Para rutas protegidas se valida el ACCESS token.
        access_token = AccessToken( token )
        access_token.verify()
    except Exception:
        return JsonResponse( { 'detail': 'Token inválido o expirado.' }, status=401 )
    
    # Verificar que el usuario en el token exista en la base de datos.
    try:
        user_id = access_token[ 'user_id' ]
        Usuarios.objects.get( id_usuario=user_id )
    except ( KeyError, Usuarios.DoesNotExist ):
        return JsonResponse( { 'detail': 'Usuario no válido.' }, status=401 )

    return None