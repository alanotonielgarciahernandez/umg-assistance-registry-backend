from django.http import JsonResponse
from django.views.decorators.http import require_safe

# Importamos los modelos que acabas de crear
from models.instalacion_model import Instalacion
from models.puerta_model import Puerta
from models.salon_model import Salon

# Importamos el guardia de seguridad de tu compañero
from middlewares.validar_JWT import validateJWT

@require_safe
def list_instalaciones( request ):
    # 1. Validar el token de seguridad
    validar_JWT_response = validateJWT( request )
    if validar_JWT_response:
        return validar_JWT_response
    
    # 2. Traer todos los edificios (instalaciones)
    instalaciones = Instalacion.objects.all()
    resultado = []

    # 3. Recorrer cada edificio para meterle sus puertas y salones
    for instalacion in instalaciones:
        # Buscar puertas que pertenezcan a este edificio
        puertas = Puerta.objects.filter( instalacion__id_instalacion=instalacion.id_instalacion ).values( 'id_puerta', 'nombre' )
        
        # Buscar salones que pertenezcan a este edificio
        salones = Salon.objects.filter( instalacion__id_instalacion=instalacion.id_instalacion ).values( 'id_salon', 'nivel', 'nombre' )

        # Armar la "caja" con los datos del edificio y meterle las puertas y salones
        edificio_data = {
            "id_instalacion": instalacion.id_instalacion,
            "nombre": instalacion.nombre,
            "puertas": list( puertas ),
            "salones": list( salones )
        }
        resultado.append( edificio_data )

    # 4. Devolver la respuesta en formato JSON
    return JsonResponse( resultado, safe=False )