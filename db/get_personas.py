# get_personas.py
# Función para obtener todas las personas de la base de datos.

# Importar módulos de Python.
import base64

# Importar modelos.
from models.persona_model import Persona

def get_personas() -> list[ dict ]:
    # Obtener todas las personas de la base de datos.
    personas: list[ Persona ] = Persona.objects.all()

    # Serializar manualmente.
    data: list[ dict ] = [
        {
            'id_persona': persona.id_persona,
            'nombre': persona.nombre,
            'apellido': persona.apellido,
            'telefono': persona.telefono,
            'correo': persona.correo,
            'tipo_persona': persona.tipo_persona,
            'carrera': persona.carrera,
            'seccion': persona.seccion,
            'fotografia_path': persona.fotografia_path,
            'vector_facial': base64.b64encode( persona.vector_facial ).decode( 'utf-8' ) if persona.vector_facial else None,
            'carnet': persona.carnet,
            'qr_path': persona.qr_path,
            'fecha_registro': persona.fecha_registro
        }
        for persona in personas
    ]

    return data
