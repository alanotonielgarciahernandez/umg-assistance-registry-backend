# get_cursos.py
# Función para obtener la lista de cursos desde la base de datos.

# Importar modelos.
from models.curso_model import Curso
from models.usuario_model import Usuario

def get_cursos_by_persona( user: Usuario ) -> list[ dict ]:
    # Obtener la lista de cursos asociados a la persona del usuario.
    cursos: list[ Curso ] = Curso.objects.filter( persona__id_persona=user.persona.id_persona )

    # Serializar manualmente.
    data: list[ dict ] = [
        {
            'id_asignacion': curso.id_asignacion,
            'nombre_curso': curso.nombre_curso,
            'horario': curso.horario,
            'id_persona': curso.persona.id_persona,
            'salon': {
                'id_salon': curso.salon.id_salon,
                'nombre': curso.salon.nombre,
                'nivel': curso.salon.nivel,
            } if curso.salon else None
        }
        for curso in cursos
    ]

    return data
