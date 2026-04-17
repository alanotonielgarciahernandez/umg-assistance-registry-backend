# login_route.py
# Definición de la ruta para el inicio de sesión.

import json

# Importar módulos de Django.
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Importar modelo de usuario.
from models.usuario_model import Usuario

# Importar funciones de la base de datos.
from db.iniciar_sesion import try_login

# Importar generador de JWT.
from tokens.jwt import generate_jwt

@require_POST
def login( request ):
    try:
        # Obtener el correo y contraseña del body.
        body = json.loads( request.body )

        user: Usuario = Usuario(
            correo=body.get( 'correo' ),
            password=body.get( 'password' ),
        )
    except json.JSONDecodeError:
        return JsonResponse( { 'error': 'Usuario o contraseña incorrectos' }, status=400 )

    # Intentar iniciar sesión con las credenciales proporcionadas.
    db_user: Usuario = try_login( user.correo, user.password )
    if not db_user:
        return JsonResponse( { 'error': 'Usuario o contraseña incorrectos' }, status=401 )
    
    # Generar token JWT para el usuario autenticado.
    jwt_token = generate_jwt( db_user )
    if not jwt_token:
        return JsonResponse( { 'error': 'Error al generar token' }, status=500 )

    # Devolver el token JWT en la respuesta.
    return JsonResponse(
        {
            'access': str( jwt_token ),
            'token_type': 'Bearer',
        },
        status=200,
    )
