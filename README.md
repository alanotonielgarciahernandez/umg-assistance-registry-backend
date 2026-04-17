# UMG Assistance Registry Backend
#### Backend hecho con Django 6.0 que devuelve datos procesados acerca del registro de alumnos de la universidad.

## Estado actual del proyecto.
- El backend se ejecuta sin errores.
- El backend tiene conexión con la base de datos.
- El backend puede extraer datos de la base de datos y mostrarlos al usuario.
- El backend utiliza JWT para autenticaciones en endpoints e inicio de sesión.

## Endpoints.
- `/personas`: Extrae JWT de `headers.Authorization` para listar los datos de las personas registradas en la tabla `dbo.personas`.
- `/login`: Extrae usuario y contraseña de `request.body` y compara con la base de datos para iniciar sesión y generar un JWT.
- `/instalaciones`: Lista todas las instalaciones registradas, cada una con su lista de puertas y salones.
- `/reportes/puerta/historico`: Lista todos los días con registros de ingreso para la puerta indicada, agrupados por fecha.
- `/reportes/puerta/fecha`: Lista las personas que ingresaron por la puerta indicada en una fecha específica.
- `/reportes/salon/historico`: Lista todos los días con registros de ingreso al salón indicado, agrupados por fecha.
- `/reportes/salon/fecha`: Lista las personas que ingresaron al salón indicado en una fecha específica, con su tipo de persona.
- `*`: Responde con el mensaje "404 Not Found".

## Bearer JWT como encabezado de autorización.
El backend utiliza JWT de tipo Bearer, es necesario que el encabezado `Authorization` para los endpoints que requieren el JWT comienzen con la palabra `Bearer` seguidos del JWT sin espacios.

## Requerimientos.
- [ Python 3.14 ]( https://www.python.org/downloads/ )
- [ Django 6.0.3 ]( https://www.djangoproject.com/download/ )
- [ django-cors-headers 4.9.0 ]( https://pypi.org/project/django-ninja-jwt/ )
- [ django-ninja 1.6.2 ]( https://django-ninja.dev/tutorial/ )
- [ django-ninja-jwt 5.4.4 ]( https://pypi.org/project/django-ninja-jwt/ )
- [ mssql-django 1.7 ]( https://pypi.org/project/mssql-django/ )
- [ reportlab 4.4.10 ]( https://pypi.org/project/reportlab/ )
- [ waitress 3.0.2 ]( https://pypi.org/project/django-cors-headers/ )
- [ ODBC Driver 17 for SQL Server ]( https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver17 )

## Ejecutar backend.
Es necesario definir las siguientes variables de entorno antes de iniciar el servidor:
```
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
DJANGO_SECRET_KEY=tu-clave-secreta-segura
DB_NAME=tu-nombre-de-base-de-datos-sql-server
DB_USER=tu-usuario-sql-server
DB_PASSWORD=tu-contraseña-de-usuario-sql-server
DB_HOST=tu-host-sql-server
DB_PORT=puerto-de-sql-server
```
Puedes definir las variables manualmente o en un archivo `.env` en la raíz del proyecto (se leen automáticamente).

Para desarrollo local:
```
py manage.py runserver
```

Para producción (contenedor):
```
docker build . -t umg-assistance-registry

docker run --rm -p 8000:8000 \
  -e DJANGO_SECRET_KEY=tu-clave-secreta-segura \
  -e DJANGO_DEBUG=False \
  -e DJANGO_ALLOWED_HOSTS=tu-dominio.com,localhost,127.0.0.1 \
  -e DB_NAME=tu-nombre-de-base-de-datos-sql-server \
  -e DB_USER=tu-usuario-sql-server \
  -e DB_PASSWORD=tu-contraseña-de-usuario-sql-server \
  -e DB_HOST=tu-host-sql-server \
  -e DB_PORT=puerto-de-sql-server \
  umg-assistance-registry
```
