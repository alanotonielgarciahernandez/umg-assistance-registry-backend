# puerta_route.py
# Definición de las rutas para los reportes de puerta.

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
from db.get_puerta import get_puerta_fecha, get_puerta_historico

class PuertaHistoricoView( View ):
    def get( self, request ) -> JsonResponse:
        # Obtener Query Parameters.
        id_instalacion: int = request.GET.get( 'id_instalacion' )
        id_puerta: int = request.GET.get( 'id_puerta' )

        # Validar que el encabezado de autorización esté presente.
        auth_header: str = request.headers.get( 'Authorization' )
        if not auth_header:
            return JsonResponse( { 'detail': 'El encabezado de autorización es requerido.' }, status=401 )
        
        # Validar el token JWT.
        user: Usuario = validateJWT( auth_header )
        if user is None:
            return JsonResponse( { 'detail': 'Usuario no válido.' }, status=401 )

        # Validar rol del usuario.
        if not validateRole( user, [ Roles.ADMIN ] ):
            return JsonResponse( { 'detail': 'Rol no autorizado.' }, status=403 )

        # Validar que se hayan proporcionado los parámetros necesarios.
        if not id_instalacion or not id_puerta:
            return JsonResponse( { 'error': 'Faltan parámetros' }, status=400 )

        # Obtener los datos de la puerta desde la base de datos.
        resultado: list[ dict ] = get_puerta_historico( id_instalacion, id_puerta )
        if resultado is None:
            return JsonResponse( { 'error': 'La puerta no pertenece a la instalación' }, status=400 )

        return JsonResponse( resultado, safe=False )


class PuertaFechaView( View ):
    def get( self, request ) -> JsonResponse:
        # Obtener Query Parameters.
        id_instalacion: int = request.GET.get( 'id_instalacion' )
        id_puerta: int = request.GET.get( 'id_puerta' )
        fecha: str = request.GET.get( 'fecha' )
        orden: str = request.GET.get( 'orden', 'ASC' ).upper() # Por defecto los ordenamos normal (ASC)

        # Validar que el encabezado de autorización esté presente.
        auth_header: str = request.headers.get( 'Authorization' )
        if not auth_header:
            return JsonResponse( { 'detail': 'El encabezado de autorización es requerido.' }, status=401 )
        
        # Validar el token JWT.
        user: Usuario = validateJWT( auth_header )
        if user is None:
            return JsonResponse( { 'detail': 'Usuario no válido.' }, status=401 )

        # Validar rol del usuario.
        if not validateRole( user, [ Roles.ADMIN ] ):
            return JsonResponse( { 'detail': 'Rol no autorizado.' }, status=403 )
        
        # Validar que se hayan proporcionado los parámetros necesarios.
        if not id_instalacion or not id_puerta or not fecha:
            return JsonResponse( { 'error': 'Faltan parámetros' }, status=400 )

        # Obtener los datos de la puerta desde la base de datos.
        resultado: list[ dict ] = get_puerta_fecha( id_instalacion, id_puerta, fecha, orden )

        return JsonResponse( resultado, safe=False )
