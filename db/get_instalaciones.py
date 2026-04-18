# get_instalaciones.py
# Función para obtener la lista de instalaciones desde la base de datos.

# Importar modelos.
from models.instalacion_model import Instalacion
from models.puerta_model import Puerta
from models.salon_model import Salon

def get_instalaciones() -> list[ dict ]:
    # Obtener la lista de instalaciones desde la base de datos.
    instalaciones: list[ Instalacion ] = Instalacion.objects.all()

    # Obtener la lista de puertas.
    puertas: list[ Puerta ] = Puerta.objects.all()

    # Obtener la lista de salones.
    salones: list[ Salon ] = Salon.objects.all()

    # Serializar manualmente.
    data: list[ dict ] = [
        {
            'id_instalacion': instalacion.id_instalacion,
            'nombre': instalacion.nombre,
            'puertas': [
                {
                    'id_puerta': puerta.id_puerta,
                    'nombre': puerta.nombre
                }
                for puerta in puertas if puerta.instalacion_id == instalacion.id_instalacion
            ],
            'salones': [
                {
                    'id_salon': salon.id_salon,
                    'nivel': salon.nivel,
                    'nombre': salon.nombre
                }
                for salon in salones if salon.instalacion_id == instalacion.id_instalacion
            ]
        }
        for instalacion in instalaciones
    ]
    
    return data
