# wsgi.py
# Configuración WSGI para servidores de producción.

# Importar módulos de Python.
import os

# Importar módulos de Django.
from django.core.wsgi import get_wsgi_application

# Establecer la variable de entorno para la configuración de Django.
os.environ.setdefault( 'DJANGO_SETTINGS_MODULE', 'settings' )

# Obtener la aplicación WSGI para servir el proyecto.
application = get_wsgi_application()
