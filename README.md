# UMG Assistance Registry Backend
#### Backend hecho con Django 6.0 que devuelve datos procesados acerca del registro de alumnos de la universidad.

## Estado actual del proyecto.
- El backend se ejecuta sin errores.
- El backend tiene conexión con la base de datos.
- El backend puede extraer datos de la base de datos y mostrarlos al usuario.

## Endpoints.
- `/personas`: Lista los datos de las personas registradas en la tabla `dbo.personas`.
- `/login`: Lista los datos de las usuarios registrados en la tabla `dbo.usuarios` (Comparará usuario y contraseña con la base de datos para iniciar sesión y generar un JWT).
- `*`: Responde con el mensaje "404 Not Found".

## Requerimientos.
- [ Python 3.14 ]( https://www.python.org/downloads/ )
- [ Django 6 ]( https://www.djangoproject.com/download/ )
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

Seguidamente puedes ejecutar el backend utilizando:
```
py manage.py runserver
```
