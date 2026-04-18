# instalaciones_route.py
# Definición de la ruta para la tabla de instalaciones.

# Importar módulos de Django.
from django.http import JsonResponse
from django.views import View

# Importar modelos.
from models.rol_model import Roles
from models.usuario_model import Usuario

# Importar middlewares.
from middlewares.validate_jwt import validateJWT
from middlewares.validate_role import validateRole

# Importar funciones de la base de datos.
from db.get_instalaciones import get_instalaciones

class InstalacionesView( View ):
    def get( self, request ) -> JsonResponse:
        # Validar que el encabezado de autorización esté presente.
        auth_header: str = request.headers.get( 'Authorization' )
        if not auth_header:
            return JsonResponse( { 'detail': 'El encabezado de autorización es requerido.' }, status=401 )
        
        # Validar el token JWT.
        user: Usuario = validateJWT( auth_header )
        if not user:
            return JsonResponse( { 'detail': 'Usuario no válido.' }, status=401 )
        
        # Validar rol del usuario.
        if not validateRole( user, [ Roles.ADMIN ] ):
            return JsonResponse( { 'detail': 'Rol no autorizado.' }, status=403 )
        
        # Obtener la lista de instalaciones desde la base de datos.
        list_instalaciones: list[ dict ] = get_instalaciones()

        # 4. Devolver la respuesta en formato JSON
        return JsonResponse( list_instalaciones, safe=False )