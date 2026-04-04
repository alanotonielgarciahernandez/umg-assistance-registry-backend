# login_route.py
# Definición de la ruta para el inicio de sesión.

import json

# Importar módulos de Django.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ninja_jwt.tokens import AccessToken

# Importar modelo de usuario.
from models.usuario_model import Usuarios

@csrf_exempt
@require_POST
def login( request ):
    try:
        # 1 y 2. Sacamos correo y contraseña del body
        body = json.loads( request.body )
        correo_ingresado = body.get( 'correo' )
        password_ingresado = body.get( 'password' )

        # 3. Buscamos si el correo existe en la base de datos
        usuario = Usuarios.objects.filter( correo=correo_ingresado ).first()

        if usuario:
            # 4. Si el correo coincide, comparamos la contraseña
            if usuario.password == password_ingresado:
                # 5. Todo coincide -> devolvemos JWT de acceso.
                access = AccessToken()
                access[ 'user_id' ] = usuario.id_usuario
                access[ 'correo' ] = usuario.correo
                access[ 'rol' ] = usuario.rol
                access[ 'id_persona' ] = usuario.id_persona.id_persona

                return JsonResponse(
                    {
                        'access': str( access ),
                        'token_type': 'Bearer',
                    },
                    status=200,
                )
            else:
                return JsonResponse( { "error": "Credenciales incorrectas" }, status=401 )
        else:
            return JsonResponse( { "error": "Credenciales incorrectas" }, status=404 )

    except Exception as e:
        return JsonResponse( { "error": "Datos inválidos" }, status=400 )
