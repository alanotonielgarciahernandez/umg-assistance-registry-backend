# env_helpers.py
# Módulo de ayuda para cargar variables de entorno desde un archivo .env y obtener listas a partir de variables de entorno.

# Importar módulos de Python.
import os
from pathlib import Path

# Cargar variables de entorno desde un archivo .env.
def load_env_file():
    # Usar el .env en la raíz del proyecto.
    resolved_env_path = Path( __file__ ).resolve().parent.parent / '.env'

    if not resolved_env_path.exists() or not resolved_env_path.is_file():
        return

    with resolved_env_path.open( 'r', encoding = 'utf-8' ) as env_file:
        for line in env_file:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith( '#' ) or '=' not in stripped_line:
                continue

            key, value = stripped_line.split( '=', 1 )
            parsed_key = key.strip()
            parsed_value = value.strip().strip( '"' ).strip( "'" )
            os.environ.setdefault( parsed_key, parsed_value )

# Función para obtener una lista de valores a partir de una variable de entorno separada por comas.
def env_list( name: str, default: str = '' ) -> list[ str ]:
    value = os.getenv( name, default )
    return [ item.strip() for item in value.split( ',' ) if item.strip() ]
