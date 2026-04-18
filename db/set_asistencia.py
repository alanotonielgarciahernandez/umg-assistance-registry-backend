# guardar_registro.py
# Script para guardar un registro de asistencia en la base de datos.

# Importar módulos de Python.
from datetime import date, datetime, timezone

# Importar modelos.
from models.registro_model import Asistencia
from models.curso_model import Curso
from models.persona_model import Persona
from models.usuario_model import Usuario

def save_asistencia( id_asignacion: int, catedratico: Usuario, fecha_asistencia: date, lista_asistencia: list[ dict ] ) -> dict | None:
    # Diccionario para almacenar el resultado del proceso de guardado.
    response: dict = {
        'total_presentes': 0,
        'total_ausentes': 0,
    }

    # Obtener asistencias existentes para la misma fecha y curso, para actualizar.
    existing_assistances: list[ Asistencia ] = Asistencia.objects.filter(
        curso__id_asignacion=id_asignacion,
        fecha=fecha_asistencia,
    )

    try:
        for asistencia in lista_asistencia:
            # Variable para almacenar el ID de asistencia.
            id_asistencia: int = None

            # Verificar si ya existe un registro de asistencia para la misma persona, curso y fecha.
            for existing in existing_assistances:
                if existing.persona.id_persona == asistencia[ 'id_persona' ]:
                    # Si ya existe un registro para esa persona, actualizarlo.
                    id_asistencia = existing.id_asistencia
                    break
                    

            # Guardar cada registro de asistencia en la base de datos.
            Asistencia(
                id_asistencia=id_asistencia,
                curso=Curso.objects.get( id_asignacion=id_asignacion ),
                persona=Persona.objects.get( id_persona=asistencia[ 'id_persona' ] ),
                fecha=fecha_asistencia,
                estado=asistencia[ 'estado' ],
                confirmado_por=catedratico.id_usuario,
                fecha_confirmacion=datetime.now( timezone.utc )
            ).save()
            
            # Contar el número de presentes y ausentes para el reporte.
            if asistencia[ 'estado' ].lower() == 'presente':
                response[ 'total_presentes' ] += 1
            else:
                response[ 'total_ausentes' ] += 1
    except Exception:
        return None

    return response
