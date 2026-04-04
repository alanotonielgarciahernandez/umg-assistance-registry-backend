# handlers.py
# Manejadores de rutas.

# Importar módulos de Django.
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt  # 👈 Aquí traemos el pase VIP

# Importar rutas.
from routes.personas_route import list_personas
from routes.login_route import login

# rutas
urlpatterns = [
    # ruta de personas
    path( 'personas', list_personas, name='list_personas' ),
    
    # pase vip para probar login
    path( 'login', csrf_exempt(login), name='login' ),

    # Ruta para manejar cualquier otra ruta no definida (404).
    path( '', lambda _: HttpResponse( '<h1>404 Not Found</h1>', status=404 ) ),
]
