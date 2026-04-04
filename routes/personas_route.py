# personas_route.py
# Definición de la ruta para la tabla de personas.

# Importar módulos de Django.
from django.http import JsonResponse
from django.views.decorators.http import require_safe

# Importar modelo de persona.
from models.persona_model import Persona

# Importar middleware de validación de JWT.
from middlewares.validar_JWT import validateJWT

@require_safe # Solo permite métodos GET y HEAD.
def list_personas( request ):
    validar_JWT_response = validateJWT( request )
    
    if validar_JWT_response:
        return validar_JWT_response

    return JsonResponse( list( Persona.objects.all().values() ), safe=False )