# salon_route.py
# Definición de la ruta para los reportes de salón.

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
from db.get_salones import get_salones_fecha, get_salones_historico

class SalonHistoricoView( View ):
    def get( self, request ) -> JsonResponse:
        # Obtener Query Parameters.
        id_instalacion: int = request.GET.get( 'id_instalacion' )
        id_salon: int = request.GET.get( 'id_salon' )

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
        if not id_instalacion or not id_salon:
            return JsonResponse( { 'error': 'Faltan parámetros' }, status=400 )

        list_ingresos: list[ dict ] = get_salones_historico( id_instalacion, id_salon )
        if list_ingresos is None:
            return JsonResponse( { 'error': 'El salón no pertenece a la instalación o no existe' }, status=400 )

        return JsonResponse( list( list_ingresos ), safe=False )


class SalonFechaView( View ):
    def get( self, request ) -> JsonResponse:
        id_instalacion: int = request.GET.get( 'id_instalacion' )
        id_salon: int = request.GET.get( 'id_salon' )
        fecha: str = request.GET.get( 'fecha' )

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
        if not id_instalacion or not id_salon or not fecha:
            return JsonResponse( { 'error': 'Faltan parámetros' }, status=400 )

        # Obtener registros del salón para la fecha dada.
        list_ingresos: list[ dict ] = get_salones_fecha( id_instalacion, id_salon, fecha )
        if list_ingresos is None:
            return JsonResponse( { 'error': 'El salón no pertenece a la instalación o no existe' }, status=400 )

        return JsonResponse( list_ingresos, safe=False )