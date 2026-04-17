# personas_route.py
# Definición de la ruta para la tabla de personas.

# Importar módulos de Django.
from django.http import JsonResponse
from django.views.decorators.http import require_safe
import base64

# Importar modelo de persona.
from models.persona_model import Persona

# Importar middleware de validación de JWT.
from middlewares.validar_JWT import validateJWT

@require_safe # Solo permite métodos GET y HEAD.
def list_personas( request ):
    validar_JWT_response = validateJWT( request )
    
    if validar_JWT_response:
        return validar_JWT_response
    
    personas = Persona.objects.all().values()
    personas_data = list( personas )
    
    # Convertir campos bytes a base64 para serialización JSON
    for persona in personas_data:
        if persona.get( 'vector_facial') and isinstance( persona[ 'vector_facial' ], bytes  ):
            persona[ 'vector_facial' ] = base64.b64encode( persona[ 'vector_facial' ] ).decode( 'utf-8' )

    return JsonResponse( personas_data, safe=False )