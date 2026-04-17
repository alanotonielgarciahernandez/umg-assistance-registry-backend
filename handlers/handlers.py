# handlers.py
# Manejadores de rutas.

from django.http import HttpResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from routes.personas_route import list_personas
from routes.login_route import login
from routes.instalaciones_route import list_instalaciones
from routes.reporte_puerta_route import reporte_puerta_historico, reporte_puerta_fecha
from routes.reporte_salon_route import reporte_salon_historico, reporte_salon_fecha

urlpatterns = [
    # Ruta de personas
    path('personas', list_personas, name='list_personas'),
    
    # Ruta de login con pase VIP
    path('login', csrf_exempt(login), name='login'),

    # --- PROCESO 5: Dashboard de Reportes ---
    
    # Endpoint 4: Listar instalaciones, puertas y salones
    path('instalaciones', list_instalaciones, name='list_instalaciones'),
    
    # Endpoint 5: Reporte histórico por puerta
    path('reportes/puerta/historico', reporte_puerta_historico, name='reporte_puerta_historico'),
    
    # Endpoint 6: Reporte por puerta filtrado por fecha
    path('reportes/puerta/fecha', reporte_puerta_fecha, name='reporte_puerta_fecha'),
    
    # Endpoint 7: Reporte histórico por salón
    path('reportes/salon/historico', reporte_salon_historico, name='reporte_salon_historico'),
    
    # Endpoint 8: Reporte por salón filtrado por fecha
    path('reportes/salon/fecha', reporte_salon_fecha, name='reporte_salon_fecha'),

    # ----------------------------------------

    # Ruta de salud para Kubernetes
    path('health', lambda _: HttpResponse(status=200), name='health'),

    # Manejo de rutas no definidas (404)
    path('', lambda _: HttpResponse('<h1>404 Not Found</h1>', status=404)),
]
