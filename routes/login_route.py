# login_route.py
# Definición de la ruta para el inicio de sesión.

# Importar módulos de Python.
import json

# Importar módulos de Django.
from django.http import JsonResponse
from django.views import View

# Importar modelos.
from models.usuario_model import Usuario

# Importar funciones de la base de datos.
from db.login import try_login

# Importar generador de JWT.
from tokens.jwt import generate_jwt

class LoginView( View ):
    def post( self, request ) -> JsonResponse:
        try:
            # Obtener el correo y contraseña del body.
            body: dict = json.loads( request.body )

            # Crear un objeto Usuario con las credenciales proporcionadas.
            user: Usuario = Usuario(
                correo=body.get( 'correo' ),
                password=body.get( 'password' ),
            )
        except json.JSONDecodeError:
            return JsonResponse( { 'error': 'Usuario o contraseña incorrectos' }, status=400 )

        # Intentar iniciar sesión con las credenciales proporcionadas.
        db_user: Usuario = try_login( user.correo, user.password )
        if db_user is None:
            return JsonResponse( { 'error': 'Usuario o contraseña incorrectos' }, status=401 )
        
        # Generar token JWT para el usuario autenticado.
        jwt_token: str = generate_jwt( db_user )
        if jwt_token is None:
            return JsonResponse( { 'error': 'Error al generar token' }, status=500 )

        # Devolver el token JWT en la respuesta.
        return JsonResponse(
            {
                'access': str( jwt_token ),
                'token_type': 'Bearer',
            },
            status=200,
        )
