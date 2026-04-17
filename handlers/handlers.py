# handlers.py
# Manejadores de rutas.

# Importar módulos de Django.
from django.http import HttpResponse
from django.urls import path

# Importar rutas.
from routes.personas_route import list_personas
from routes.cursos_route import CursosView, AsistenciaView
from routes.instalaciones_route import list_instalaciones
from routes.reporte_puerta_route import reporte_puerta_historico, reporte_puerta_fecha
from routes.reporte_salon_route import reporte_salon_historico, reporte_salon_fecha
from routes.media_route import serve_media
from routes.login_route import login

# Rutas.
urlpatterns = [
    # Ruta de login.
    path( 'login', login, name='login' ),

    # Ruta de personas.
    path( 'personas', list_personas, name='personas' ),

    # Ruta de cursos.
    path( 'cursos', CursosView.as_view(), name='cursos' ),
    path( 'cursos/<int:id_asignacion>/asistencia', AsistenciaView.as_view(), name='asistencia' ),

    # Ruta de instalaciones.
    path( 'instalaciones', list_instalaciones, name='list_instalaciones' ),
    
    # Ruta de reportes de puerta.
    path( 'reportes/puerta/historico', reporte_puerta_historico, name='puerta_historico' ),
    path( 'reportes/puerta/fecha', reporte_puerta_fecha, name='puerta_fecha' ),

    # Ruta de reportes de salón.
    path( 'reportes/salon/historico', reporte_salon_historico, name='salon_historico' ),
    path( 'reportes/salon/fecha', reporte_salon_fecha, name='salon_fecha' ),

    # Ruta para servir archivos multimedia.
    path( 'media/<str:media_path>', serve_media, name='media' ),

    # Ruta de salud utilizada por Kubernetes para verificar que el servidor esté funcionando.
    path( 'health', lambda _: HttpResponse( status=200 ), name='health' ),

    # Ruta para manejar cualquier otra ruta no definida (404).
    path( '', lambda _: HttpResponse( '<h1>404 Not Found</h1>', status=404 ) ),
]
