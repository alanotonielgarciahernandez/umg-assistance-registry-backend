# handlers.py
# Manejadores de rutas.

# Importar módulos de Django.
from django.urls import path

# Importar rutas.
from routes.personas_route import list_personas

# Definir rutas.
urlpatterns = [
    path( 'personas', list_personas, name='list_personas' ),
]