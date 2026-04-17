# cursos_route.py
# Definición de la ruta para la tabla de cursos.

# Importar módulos de Python.
import json
from datetime import date

# Importar módulos de Django.
from django.http import JsonResponse
from django.views import View

# Importar middleware de validación de JWT.
from middlewares.validar_JWT import validateJWT
from middlewares.validar_rol import validateRole

# Importar modelos.
from models.curso_model import Curso
from models.rol_model import Roles
from models.registro_model import IngresoSalon

# Importar funciones de la base de datos.
from db.guardar_registro import guardar_registro

# Importar funciones de reportes.
from reports.asistencia_report import generar_registro_asistencia

class CursosView( View ):
    def get( self, request ):
        # Validar que el encabezado de autorización esté presente.
        auth_header = request.headers.get( 'Authorization' )
        if not auth_header:
            return JsonResponse( { 'detail': 'El encabezado de autorización es requerido.' }, status=401 )

        # Validar que el encabezado de autorización tenga el formato correcto.
        if not auth_header.startswith( 'Bearer' ):
            return JsonResponse( { 'detail': 'Formato de token inválido.' }, status=401 )

        # Extraer el token del encabezado de autorización.
        token = auth_header[ 6: ].strip()
        if not token:
            return JsonResponse( { 'detail': 'Token no proporcionado.' }, status=401 )
        
        # Validar el token JWT.
        user = validateJWT( token )
        if not user:
            return JsonResponse( { 'detail': 'Usuario no válido.' }, status=401 )

        # Validar rol del usuario.
        if not validateRole( user, Roles.CATEDRATICO ):
            return JsonResponse( { 'detail': 'Rol no autorizado.' }, status=403 )

        cursos = Curso.objects.filter( persona__id_persona=user.persona.id_persona )

        # Serializar manualmente.
        data = [
            {
                'id_asignacion': curso.id_asignacion,
                'nombre_curso': curso.nombre_curso,
                'horario': curso.horario,
                'id_persona': curso.persona.id_persona,
                'salon': {
                    'id_salon': curso.salon.id_salon,
                    'nombre': curso.salon.nombre,
                    'nivel': curso.salon.nivel,
                } if curso.salon else None
            }
            for curso in cursos
        ]

        return JsonResponse( data, safe=False )

class AsistenciaView( View ):
    # Obtener la lista de asistencia para un curso específico.
    def get( self, request, id_asignacion ):
        fecha = request.GET.get( 'fecha', date.today() )  # Opcional, para filtrar por fecha específica.

        # Validar que el encabezado de autorización esté presente.
        auth_header = request.headers.get( 'Authorization' )
        if not auth_header:
            return JsonResponse( { 'detail': 'El encabezado de autorización es requerido.' }, status=401 )

        # Validar que el encabezado de autorización tenga el formato correcto.
        if not auth_header.startswith( 'Bearer' ):
            return JsonResponse( { 'detail': 'Formato de token inválido.' }, status=401 )

        # Extraer el token del encabezado de autorización.
        token = auth_header[ 6: ].strip()
        if not token:
            return JsonResponse( { 'detail': 'Token no proporcionado.' }, status=401 )
        
        # Validar el token JWT.
        user = validateJWT( token )
        if not user:
            return JsonResponse( { 'detail': 'Usuario no válido.' }, status=401 )

        # Validar rol del usuario.
        if not validateRole( user, Roles.CATEDRATICO ):
            return JsonResponse( { 'detail': 'Rol no autorizado.' }, status=403 )

        # Validar que el curso exista y que el catedrático sea el dueño.
        curso = Curso.objects.filter( id_asignacion=id_asignacion, persona__id_persona=user.persona.id_persona ).first()
        if not curso:
            return JsonResponse( { 'detail': 'Curso no encontrado.' }, status=404 )
        
        print( str( fecha ) )

        # Obtener los registros de ingreso al salón para el curso.
        ingreso_salon = IngresoSalon.objects.filter( salon__id_salon=curso.salon.id_salon, fecha_hora__date=fecha ).order_by( '-fecha_hora' )
        
        # Serializar manualmente.
        data = [
            {
                'id_persona': ingreso.persona.id_persona,
                'nombre': ingreso.persona.nombre,
                'apellido': ingreso.persona.apellido,
                'correo': ingreso.persona.correo,
                'fotografia_path': ingreso.salon.id_salon,
                'estado': 'PRESENTE'
            }
            for ingreso in ingreso_salon
        ]

        return JsonResponse( data, safe=False )
    
    def post( self, request, id_asignacion ):
        # Validar que el encabezado de autorización esté presente.
        auth_header = request.headers.get( 'Authorization' )
        if not auth_header:
            return JsonResponse( { 'detail': 'El encabezado de autorización es requerido.' }, status=401 )

        # Validar que el encabezado de autorización tenga el formato correcto.
        if not auth_header.startswith( 'Bearer' ):
            return JsonResponse( { 'detail': 'Formato de token inválido.' }, status=401 )

        # Extraer el token del encabezado de autorización.
        token = auth_header[ 6: ].strip()
        if not token:
            return JsonResponse( { 'detail': 'Token no proporcionado.' }, status=401 )
        
        # Validar el token JWT.
        user = validateJWT( token )
        if not user:
            return JsonResponse( { 'detail': 'Usuario no válido.' }, status=401 )

        # Validar rol del usuario.
        if not validateRole( user, Roles.CATEDRATICO ):
            return JsonResponse( { 'detail': 'Rol no autorizado.' }, status=403 )
        
        # Obtenemos datos de asistencia del cuerpo de la solicitud.
        body = json.loads( request.body )

        status = guardar_registro( id_asignacion, user, body.get( 'fecha', date.today() ), body.get( 'asistencias', [] ) )
        if not status:
            return JsonResponse( { 'detail': 'Error al guardar el registro.' }, status=500 )
        
        pdf_path = generar_registro_asistencia( id_asignacion, body.get( 'fecha', date.today() ), body.get( 'asistencias', [] ) )

        # Serializar manualmente.
        data = {
            'confirmado': True,
            'total_presentes': status[ 'total_presentes' ],
            'total_ausentes': status[ 'total_ausentes' ],
            'pdf_url': pdf_path
        }

        return JsonResponse( data, safe=False )
