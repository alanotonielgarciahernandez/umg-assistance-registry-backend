# guardar_registro.py
# Script para guardar un registro de asistencia en la base de datos.

# Importar módulos de Python.
from datetime import date, datetime, timezone

# Importar modelos.
from models.registro_model import Asistencia
from models.curso_model import Curso
from models.persona_model import Persona
from models.usuario_model import Usuario

def guardar_registro( id_asignacion: int, catedratico: Usuario, fecha_asistencia: date, lista_asistencia: list[ dict ] ) -> dict:
    response = {
        'total_presentes': 0,
        'total_ausentes': 0,
    }

    try:
        for asistencia in lista_asistencia:
            Asistencia(
                curso=Curso.objects.get( id_asignacion=id_asignacion ),
                persona=Persona.objects.get( id_persona=asistencia[ 'id_persona' ] ),
                fecha=fecha_asistencia,
                estado=asistencia[ 'estado' ],
                confirmado_por=catedratico.id_usuario,
                fecha_confirmacion=datetime.now( timezone.utc )
            ).save()
            
            if asistencia[ 'estado' ].lower() == 'presente':
                response[ 'total_presentes' ] += 1
            else:
                response[ 'total_ausentes' ] += 1
    except Exception as e:
        print( f'Error al guardar el registro: { e }' )
        return None

    return response
