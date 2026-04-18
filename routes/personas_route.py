# personas_route.py
# Definición de la ruta para la tabla de personas.

# Importar módulos de Django.
from django.http import JsonResponse
from django.views import View

# Importar middleware de validación de JWT.
from middlewares.validate_jwt import validateJWT

# Importar funciones de la base de datos.
from db.get_personas import get_personas

class PersonasView( View ):
    def get( self, request ) -> JsonResponse:
        # Validar que el encabezado de autorización esté presente.
        auth_header: str = request.headers.get( 'Authorization' )
        if not auth_header:
            return JsonResponse( { 'detail': 'El encabezado de autorización es requerido.' }, status=401 )
         
        # Validar el token JWT.
        if validateJWT( auth_header ) is None:
            return JsonResponse( { 'detail': 'Usuario no válido.' }, status=401 )
        
        # Obtener la lista de personas desde la base de datos.
        persona_list: list[ dict ] = get_personas()

        return JsonResponse( persona_list, safe=False )