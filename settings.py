# settings.py

import os

# Cargar variables de entorno desde el archivo .env.
def _load_env_file():
    env_path = os.path.join( os.path.dirname( __file__ ), '.env' )
    if not os.path.exists( env_path ):
        return

    with open( env_path, 'r', encoding='utf-8' ) as env_file:
        for line in env_file:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith( '#' ) or '=' not in stripped_line:
                continue

            key, value = stripped_line.split( '=', 1 )
            parsed_key = key.strip()
            parsed_value = value.strip().strip( '"' ).strip( "'" )
            os.environ.setdefault(parsed_key, parsed_value)

_load_env_file()


def _env_list( name: str, default: str = '' ) -> list[ str ]:
    value = os.getenv( name, default )
    return [ item.strip() for item in value.split(',') if item.strip() ]


# Habilitar modo de depuración.
DEBUG = True

# Clave secreta para firmar sesiones/tokens de Django.
SECRET_KEY = os.getenv( 'DJANGO_SECRET_KEY' )

# Aplicaciones activas.
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'ninja',
    'ninja_jwt',
    'corsheaders',

    'handlers',
    'models',
]

# Configuración de autenticación JWT.
from datetime import timedelta

NINJA_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta( minutes=60 ),    # short-lived access token
    'REFRESH_TOKEN_LIFETIME': timedelta( days=7 ),       # longer refresh token
    'ROTATE_REFRESH_TOKENS': True,                       # issue new refresh token on use
    'BLACKLIST_AFTER_ROTATION': True,                    # security best practice
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,                           # uses your Django SECRET_KEY
    'VERIFYING_KEY': None,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ( 'ninja_jwt.tokens.AccessToken', ),
}

# Middleware de seguridad.
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# Encabezados de Seguridad.
SECURE_HSTS_SECONDS = 0              # Desactivar HSTS
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_SSL_REDIRECT = False          # No redirigir a HTTPS, ya que el contenedor puede estar detrás de un proxy que maneja TLS.
SESSION_COOKIE_SECURE = False        # Permitir HTTP en contenedor
CSRF_COOKIE_SECURE = False           # Permitir HTTP en contenedor

# Configuración de CORS.
CORS_ALLOW_ALL_ORIGINS = False       # Permitir todas las fuentes. En producción, se recomienda restringir esto.

CORS_ALLOWED_ORIGINS = [             # Orígenes permitidos para solicitudes CORS.
    'http://localhost:5173',         # Local
]

CORS_ALLOW_CREDENTIALS = True        # Permitir el envío de cookies y encabezados de autenticación en solicitudes CORS.

CORS_ALLOW_METHODS = [               # Métodos HTTP permitidos.
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Hosts permitidos.
ALLOWED_HOSTS = _env_list( 'DJANGO_ALLOWED_HOSTS', '*' )  # Por defecto acepta todos, se puede restringir via variable de entorno

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
        'PORT': os.getenv( 'DB_PORT', '1433' ),

        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}