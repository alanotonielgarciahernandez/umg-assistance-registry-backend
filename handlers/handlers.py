# handlers.py
# Manejadores de rutas.

# Importar módulos de Django.
from django.http import HttpResponse
from django.urls import path

# Importar rutas.
from routes.personas_route import PersonasView
from routes.cursos_route import CursosView, AsistenciaView
from routes.instalaciones_route import InstalacionesView
from routes.puerta_route import PuertaFechaView, PuertaHistoricoView
from routes.salon_route import SalonFechaView, SalonHistoricoView
from routes.media_route import MediaView
from routes.login_route import LoginView

# Rutas.
urlpatterns = [
    # Ruta de login.
    path( 'login', LoginView.as_view(), name='login' ),

    # Ruta de personas.
    path( 'personas', PersonasView.as_view(), name='personas' ),

    # Ruta de cursos.
    path( 'cursos', CursosView.as_view(), name='cursos' ),
    path( 'cursos/<int:id_asignacion>/asistencia', AsistenciaView.as_view(), name='asistencia' ),

    # Ruta de instalaciones.
    path( 'instalaciones', InstalacionesView.as_view(), name='instalaciones' ),
    
    # Ruta de reportes de puerta.
    path( 'reportes/puerta/historico', PuertaHistoricoView.as_view(), name='puerta_historico' ),
    path( 'reportes/puerta/fecha', PuertaFechaView.as_view(), name='puerta_fecha' ),

    # Ruta de reportes de salón.
    path( 'reportes/salon/historico', SalonHistoricoView.as_view(), name='salon_historico' ),
    path( 'reportes/salon/fecha', SalonFechaView.as_view(), name='salon_fecha' ),

    # Ruta para servir archivos multimedia.
    path( 'media/<str:media_path>', MediaView.as_view(), name='media' ),

    # Ruta de salud utilizada por Kubernetes para verificar que el servidor esté funcionando.
    path( 'health', lambda _: HttpResponse( status=200 ), name='health' ),

    # Ruta para manejar cualquier otra ruta no definida (404).
    path( '', lambda _: HttpResponse( '<h1>404 Not Found</h1>', status=404 ) ),
]
