# get_puerta.py
# Función para obtener los registros de una puerta específica.

# Importar modelos.
from models.puerta_model import Puerta, PuertaPrincipal

def get_puerta_historico( id_instalacion: int, id_puerta: int ) -> list[ dict ] | None:
    # Validar que la puerta exista en esa instalación.
    puerta_existe: bool = Puerta.objects.filter( id_puerta=id_puerta, instalacion__id_instalacion=id_instalacion ).exists()
    if not puerta_existe:
        return None

    # Obtener registros de personas identificadas en la puerta.
    registros: list[ PuertaPrincipal ] = PuertaPrincipal.objects.filter(
        puerta__id_puerta=id_puerta, 
        persona__id_persona__isnull=False
    ).order_by( '-fecha_hora' ) # Ordenar del más reciente al más viejo.

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
            } )

    # Convertir el diccionario agrupado a una lista.
    data: list[ dict ] = list( agruped_list.values() )

    return data

def get_puerta_fecha( id_instalacion: int, id_puerta: int, fecha: str, orden: str ) -> list[ dict ] | None:
    # Validar que la puerta exista en esa instalación.
    puerta_existe: bool = Puerta.objects.filter( id_puerta=id_puerta, instalacion__id_instalacion=id_instalacion ).exists()
    if not puerta_existe:
        return None

    # Configurar orden.
    order_prefix: str = '-' if orden == 'DESC' else ''

    # Obtener registros de la puerta para la fecha dada.
    # Nota: usamos __date para que solo busque por el día, ignorando la hora.
    registros: list[ PuertaPrincipal ] = PuertaPrincipal.objects.filter(
        puerta__id_puerta=id_puerta,
        fecha_hora__date=fecha
    ).order_by( f'{ order_prefix }fecha_hora' )

    # Serializar manualmente los registros para incluir información de la persona, si está disponible.
    data: list[ dict ] = [
        {
            'id_persona': registro.persona.id_persona if registro.persona else None,
            'nombre': registro.persona.nombre if registro.persona else 'Desconocido',
            'apellido': registro.persona.apellido if registro.persona else '',
            'correo': registro.persona.correo if registro.persona else None,
            'fotografia_path': registro.persona.fotografia_path if registro.persona else None,
            'fecha_hora': registro.fecha_hora.strftime( '%Y-%m-%dT%H:%M:%S' ),
            'estado': 'PRESENTE' if registro.persona else 'DESCONOCIDO'
        }
        for registro in registros
    ]

    return data
