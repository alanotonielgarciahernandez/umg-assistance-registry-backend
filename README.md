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
- `*`: Responde con el mensaje "404 Not Found".

## Bearer JWT como encabezado de autorización.
El backend utiliza JWT de tipo Bearer, es necesario que el encabezado `Authorization` para los endpoints que requieren el JWT comienzen con la palabra `Bearer` seguidos del JWT sin espacios.

## Requerimientos.
- [ Python 3.14 ]( https://www.python.org/downloads/ )
- [ Django 6 ]( https://www.djangoproject.com/download/ )
- [ django-ninja ]( https://django-ninja.dev/tutorial/ )
- [ django-ninja-extra ]( https://pypi.org/project/django-ninja-extra/ )
- [ django-ninja-jwt ]( https://pypi.org/project/django-ninja-jwt/ )
- [ mssql-django ]( https://pypi.org/project/mssql-django/ )
- [ ODBC Driver 17 for SQL Server ]( https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver17 )

## Ejecutar backend.
Es necesario definir las siguientes variables de entorno antes de iniciar el servidor:
```
DJANGO_SECRET_KEY=tu-clave-secreta-segura
DB_NAME=tu-nombre-de-base-de-datos-sql-server
DB_USER=tu-usuario-sql-server
DB_PASSWORD=tu-contraseña-de-usuario-sql-server
DB_HOST=tu-host-sql-server
```
Puedes definir las variables manualmente o en un archivo `.env` en la raíz del proyecto (se leen automáticamente).

Para desarrollo local:
```
py manage.py runserver
```
