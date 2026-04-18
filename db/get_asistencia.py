# get_asistencia.py
# Función para obtener la lista de asistencia de un curso específico desde la base de datos.

# Importar modelos.
from models.curso_model import Curso
from models.registro_model import IngresoSalon
from models.usuario_model import Usuario

def get_curso_asistencia_by_persona( id_asignacion: int, user: Usuario, fecha: str ) -> list[ dict ] | None:
    # Validar que el curso exista y que el catedrático sea el dueño.
    curso: Curso = Curso.objects.filter( id_asignacion=id_asignacion, persona__id_persona=user.persona.id_persona ).first()
    if not curso:
        return None

    # Obtener los registros de ingreso al salón para el curso.
    ingreso_salon: list[ IngresoSalon ] = IngresoSalon.objects.filter( salon__id_salon=curso.salon.id_salon, fecha_hora__date=fecha ).order_by( '-fecha_hora' )
    
    # Serializar manualmente.
    data: list[ dict ] = [
        {
            'id_persona': ingreso.persona.id_persona,
            'nombre': ingreso.persona.nombre,
            'apellido': ingreso.persona.apellido,
            'correo': ingreso.persona.correo,
            'fotografia_path': ingreso.persona.fotografia_path,
            'estado': 'PRESENTE'
        }
        for ingreso in ingreso_salon
    ]

    return data
