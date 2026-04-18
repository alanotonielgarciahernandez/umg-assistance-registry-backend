# UMG Assistance Registry Backend
#### Backend hecho con Django 6.0 que devuelve datos procesados acerca del registro de alumnos de la universidad.

## Estado actual del proyecto.
- El backend se ejecuta sin errores.
- El backend tiene conexión con la base de datos.
- El backend puede extraer datos de la base de datos y mostrarlos al usuario.
- El backend utiliza JWT para autenticaciones en endpoints e inicio de sesión.

## Endpoints.
### `POST` `/login`
Compara usuario y contraseña brindados con la base de datos para iniciar sesión y generar un JWT.

#### Body requerido
```json
{
	"correo": "user@mail.com",
	"password": "password"
}
```

#### Respuesta exitosa `200 OK`
```json
{
  "access": "<token>",
	"token_type": "Bearer"
}
```

### `GET` `/personas`
Lista todas las personas registradas.

#### Header requerido
`Authorization`: Bearer< token >

#### Respuesta exitosa `200 OK`
```json
[
	{
		"id_persona": 1,
		"nombre": "Carlos",
		"apellido": "Ramirez",
		"telefono": "11111111",
		"correo": "carlos@mail.com",
		"tipo_persona": "catedratico",
		"carrera": "N/A",
		"seccion": "N/A",
		"fotografia_path": "img/c1.jpg",
		"vector_facial": null,
		"carnet": "C001",
		"qr_path": "qr/c1.png",
		"fecha_registro": "2026-03-25T02:48:10.793Z"
	},
  ...
]
```

### `GET` `/cursos`
Lista cursos asignados al catedrático autenticado.

#### Header requerido
`Authorization`: Bearer< token > (rol: CATEDRATICO)

#### Respuesta exitosa `200 OK`
```json
[
	{ 
    "id_asignacion": 1, 
    "nombre_curso": "Programación III", 
    "horario": "Sábado 07:00–09:00", 
    "salon": { 
    "id_salon": 3, 
    "nombre": "Aula 301", 
    "nivel": "3er Nivel" 
    }
  }, 
  ...
]
```

### `GET` `/cursos/:id_asignacion/asistencia?fecha=YYY-MM-DD`
Lista todos los estudiantes del salón del curso con su estado de asistencia para la fecha indicada.

#### Header requerido
`Authorization`: Bearer< token > (rol: CATEDRATICO)

#### Path params
`id_asignacion: INT` - ID del registro en la tabla `catedratico_cursos`

#### Query params
`fecha=YYYY-MM-DD` - Opcional, si se omite usa la fecha actual del servidor .

#### Respuesta exitosa `200 OK`
```json
[
	{ 
    "id_persona": 12, 
    "nombre": "Ana",
    "apellido": "García",
    "correo": "ana@miumg.edu.gt", 
    "fotografia_path": "media/fotos/ana.jpg", 
    "estado": "PRESENTE"
  }, 
  ...
]
```

### `POST` `/cursos/:id_asignacion/asistencia`
Inserta o actualiza los registros recibidos en registro_asistencia, genera un PDF con la tabla de asistencia y lo envía al correo registrado del catedrático. Retorna también la URL del PDF generado.

#### Header requerido
`Authorization`: Bearer< token > (rol: CATEDRATICO)

#### Body requerido
```json
{ 
  "fecha": "2026-04-14", 
  "asistencias": [ 
    { "id_persona": 12, "estado": "PRESENTE" }, 
    { "id_persona": 15, "estado": "AUSENTE"  }, 
  ... 
  ] 
} 
```

#### Respuesta exitosa `200 OK`
```json
{ 
  "confirmado": true, 
  "total_presentes": 18, 
  "total_ausentes": 4, 
  "pdf_url": "media/asistencia/prog3_2026-04-14.pdf" 
} 
```

### `GET` `/instalaciones`
Lista todas las instalaciones registradas, cada una con su lista de puertas y salones.

#### Header requerido
`Authorization`: Bearer< token > (rol: ADMIN)

#### Respuesta exitosa `200 OK`
```json
[ 
  { 
    "id_instalacion": 1, 
    "nombre": "UMG La Florida Zona 19", 
    "puertas": [ 
      { "id_puerta": 1, "nombre": "Puerta Principal Norte" }, 
      { "id_puerta": 2, "nombre": "Puerta Lateral Este"    },
      ...
    ], 
    "salones": [ 
      { "id_salon": 1, "nivel": "1er Nivel", "nombre": "Aula 101" }, 
      { "id_salon": 2, "nivel": "2do Nivel", "nombre": "Aula 201" },
      ...
    ]
  },
  ...
]
```

### `GET` `/reportes/puerta/historico`
Lista todos los días con registros de ingreso para la puerta indicada, agrupados por fecha.

#### Header requerido
`Authorization`: Bearer< token > (rol: ADMIN)

#### Query params
- `id_instalacion: INT` - Requerido, ID de la instalación
- `id_puerta: INT` - Requerido, ID de la puerta

#### Respuesta exitosa `200 OK`
```json
[ 
  { 
    "fecha": "2026-04-14", 
    "total_ingresos": 23, 
    "personas": [ 
      { 
        "id_persona": 5, 
        "nombre": "Carlos", 
        "apellido": "López",
        "correo": "carlos@miumg.edu.gt", 
        "fotografia_path": "media/fotos/carlos.jpg", 
        "hora": "07:35" 
      },
      ... 
    ] 
  }, 
  ... 
]
```

### `GET` `/reportes/puerta/fecha`
Lista las personas que ingresaron por la puerta indicada en una fecha específica.

#### Header requerido
`Authorization`: Bearer< token > (rol: ADMIN)

#### Query params
- `id_instalacion: INT` - Requerido 
- `id_puerta: INT` - Requerido 
- `fecha: DATE` - Requerido, Formato (YYYY-MM-DD) 
- `orden: STRING` - Opcional, Formato ASC | DESC, por defecto ASC

#### Respuesta exitosa `200 OK`
```json
[ 
  { 
  "id_persona": 5, 
  "nombre": "Carlos", 
  "apellido": "López", 
  "correo": "carlos@miumg.edu.gt", 
  "fotografia_path": "media/fotos/carlos.jpg", 
  "fecha_hora": "2026-04-14T07:35:00", 
  "estado": "PRESENTE" 
  }, 
  { 
  "id_persona": null, 
  "nombre": "Desconocido", 
  "apellido": "", 
  "correo": null, 
  "fotografia_path": null, 
  "fecha_hora": "2026-04-14T08:12:00", 
  "estado": "DESCONOCIDO" 
  }, 
  ... 
] 
```

### `GET` `/reportes/salon/historico`
Lista todos los días con registros de ingreso al salón indicado, agrupados por fecha.

#### Header requerido
`Authorization`: Bearer< token > (rol: ADMIN)

#### Query params
- `id_instalacion: INT`- Requerido 
- `id_salon: INT`- Requerido 

#### Respuesta exitosa `200 OK`
```json
[ 
  { 
    "fecha": "2026-04-14", 
    "total_ingresos": 31, 
    "personas": [ 
      { 
        "id_persona": 8, 
        "nombre": "María", 
        "apellido": "Pérez", 
        "correo": "maria@miumg.edu.gt", 
        "fotografia_path": "media/fotos/maria.jpg", 
        "hora": "07:01", 
        "tipo_persona": "ESTUDIANTE" 
      },
      ...
    ]
  },
  ... 
]
```

### `GET` `/reportes/salon/fecha`
Lista las personas que ingresaron al salón indicado en una fecha específica, con su tipo de persona.

#### Header requerido
`Authorization`: Bearer< token > (rol: ADMIN)

#### Query params
- `id_instalacion: INT` - Requerido 
- `id_salon INT` - Requerido 
- `fecha: DATE` - Requerido, Formato (YYYY-MM-DD) 

#### Respuesta exitosa `200 OK`
```json
[ 
  { 
    "id_persona": 8, 
    "nombre": "María",
    "apellido": "Pérez",
    "correo": "maria@miumg.edu.gt", 
    "fotografia_path": "media/fotos/maria.jpg", 
    "fecha_hora": "2026-04-14T07:01:00", 
    "tipo_persona": "ESTUDIANTE" 
  },
  ...
] 
```

### `GET` `/health`
Ruta de salud utilizada por Kubernetes para verificar que el servidor esté funcionando. Responde con status code `200 OK`.

### `*`
Responde con el mensaje "404 Not Found".

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
