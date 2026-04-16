# asgi.py
# Configuración ASGI para servidores de producción.

# Importar módulos de Python.
import os

# Importar módulos de Django.
from django.core.asgi import get_asgi_application

# Establecer la variable de entorno para la configuración de Django.
os.environ.setdefault( 'DJANGO_SETTINGS_MODULE', 'settings' )

# Obtener la aplicación ASGI para servir el proyecto.
application = get_asgi_application()
