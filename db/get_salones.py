# get_salones.py
# Función para obtener la lista de salones de una instalación específica.

# Importar modelos.
from models.registro_model import IngresoSalon
from models.salon_model import Salon

def get_salones_historico( id_instalacion: int, id_salon: int ) -> list[ dict ] | None:
    # Validar que el salón exista en la instalación.
    salon_exists: bool = Salon.objects.filter( id_salon=id_salon, instalacion__id_instalacion=id_instalacion ).exists()
    if not salon_exists:
        return None

    # Obtener los registros de ingreso al salón agrupados por fecha.
    registros: list[ IngresoSalon ] = IngresoSalon.objects.filter(
        salon__id_salon=id_salon,
        persona__id_persona__isnull=False
    ).order_by( '-fecha_hora' )

    # Lista de registros agrupados por fecha.
    agruped_list: dict = {}

    for registro in registros:
        # Validar que ya existe una entrada para la fecha del registro, si no crearla.
        if agruped_list.get( registro.fecha_hora.strftime( '%Y-%m-%d' ) ) is None:
            # Si no existe una entrada para esa fecha, crearla con el primer registro.
            agruped_list[ registro.fecha_hora.strftime( '%Y-%m-%d' ) ] = {
                'fecha': registro.fecha_hora.strftime( '%Y-%m-%d' ), 
                'total_ingresos': 1, 
                'personas': [
                    { 
                        'id_persona': registro.persona.id_persona, 
                        'nombre': registro.persona.nombre, 
                        'apellido': registro.persona.apellido, 
                        'correo': registro.persona.correo, 
                        'fotografia_path': registro.persona.fotografia_path, 
                        'hora': registro.fecha_hora.strftime( '%H:%M:%S' ),
                        'tipo_persona': getattr( registro.persona, 'tipo_persona', 'ESTUDIANTE' ) # Obtenemos el tipo_persona (si no existe en tu modelo actual, por defecto ponemos ESTUDIANTE) [cite: 286]
                    }
                ]
            }
        else:
            # Si ya existe una entrada para esa fecha, agregar el nuevo registro a la lista de personas y actualizar el total de ingresos.
            agruped_list[ registro.fecha_hora.strftime( '%Y-%m-%d' ) ]['total_ingresos'] += 1
            agruped_list[ registro.fecha_hora.strftime( '%Y-%m-%d' ) ]['personas'].append( {
                'id_persona': registro.persona.id_persona,
                'nombre': registro.persona.nombre,
                'apellido': registro.persona.apellido,
                'correo': registro.persona.correo,
                'fotografia_path': registro.persona.fotografia_path,
                'hora': registro.fecha_hora.strftime( '%H:%M:%S' ),
                'tipo_persona': getattr( registro.persona, 'tipo_persona', 'ESTUDIANTE' )
            } )

    # Convertir el diccionario agrupado a una lista.
    data: list[ dict ] = list( agruped_list.values() )

    return data

def get_salones_fecha( id_instalacion: int, id_salon: int, fecha: str ) -> list[ dict ] | None:
    # Validar que el salón exista en esa instalación.
    salon_existe: bool = Salon.objects.filter( id_salon=id_salon, instalacion__id_instalacion=id_instalacion ).exists()
    if not salon_existe:
        return None

    # Obtener registros del salón para la fecha dada.
    registros: list[ IngresoSalon ] = IngresoSalon.objects.filter(
        salon__id_salon=id_salon,
        fecha_hora__date=fecha,
        persona__id_persona__isnull=False
    ).order_by( 'fecha_hora' )

    # Serializar manualmente los registros para incluir información de la persona, si está disponible.
    data: list[ dict ] = [
        {
            'id_persona': registro.persona.id_persona,
            'nombre': registro.persona.nombre,
            'apellido': registro.persona.apellido,
            'correo': registro.persona.correo,
            'fotografia_path': registro.persona.fotografia_path,
            'fecha_hora': registro.fecha_hora.strftime( '%Y-%m-%dT%H:%M:%S' ),
            'tipo_persona': getattr( registro.persona, 'tipo_persona', 'ESTUDIANTE' )
        }
        for registro in registros
    ]

    return data
