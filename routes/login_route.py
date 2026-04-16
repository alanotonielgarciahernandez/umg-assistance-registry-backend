# login_route.py
# Definición de la ruta para el inicio de sesión.

import json

# Importar módulos de Django.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ninja_jwt.tokens import AccessToken

# Importar modelo de usuario.
from models.usuario_model import Usuario

@csrf_exempt
@require_POST
def login( request ):
    try:
        # Obtenemos el correo y contraseña del body
        body = json.loads( request.body )
        correo_ingresado = body.get( 'correo' )
        password_ingresado = body.get( 'password' )

        # Buscamos si el correo existe en la base de datos
        usuario = Usuario.objects.filter( correo=correo_ingresado ).first()

        if usuario:
            # Si el correo existe, comparamos la contraseña
            if usuario.password == password_ingresado:
                # Si la contraseña es correcta, devolvemos JWT de acceso.
                access = AccessToken()
                access[ 'user_id' ] = usuario.id_usuario
                access[ 'correo' ] = usuario.correo
                access[ 'rol' ] = usuario.rol.id_rol
                access[ 'nombre' ] = usuario.persona.nombre
                access[ 'apellido' ] = usuario.persona.apellido
                access[ 'fotografia' ] = usuario.persona.fotografia_path

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
        print( "Error al procesar la solicitud de inicio de sesión:", e )
        return JsonResponse( { "error": "Datos inválidos" }, status=400 )
