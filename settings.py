# settings.py

import os

# Cargar variables de entorno desde el archivo .env.
def _load_env_file():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_path):
        return

    with open(env_path, 'r', encoding='utf-8') as env_file:
        for line in env_file:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('#') or '=' not in stripped_line:
                continue

            key, value = stripped_line.split('=', 1)
            parsed_key = key.strip()
            parsed_value = value.strip().strip('"').strip("'")
            os.environ.setdefault(parsed_key, parsed_value)

_load_env_file()

# Habilitar modo de depuración.
DEBUG = True

# Clave secreta para firmar sesiones/tokens de Django.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY') or 'dev-secret-key-change-in-production'

# Aplicaciones activas.
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',

    'handlers',
    'models',
]

# Middleware de seguridad.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

# Encabezados de Seguridad.
SECURE_HSTS_SECONDS = 31536000       # 1 año.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Hosts permitidos.
ALLOWED_HOSTS = [ 'localhost', '127.0.0.1' ]

# URL de enrutamiento.
ROOT_URLCONF = 'handlers.handlers'

# Configuración de base de datos SQL Server.
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.getenv( 'DB_NAME', '' ),
        'USER': os.getenv( 'DB_USER', '' ),
        'PASSWORD': os.getenv( 'DB_PASSWORD', '' ),
        'HOST': os.getenv( 'DB_HOST', '' ),
        'PORT': '1433',

        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}