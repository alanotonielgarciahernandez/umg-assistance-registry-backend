# personas_route.py
# Definición de la ruta para listar personas.

# Importar módulos de Django.
from django.http import JsonResponse
from django.views.decorators.http import require_safe

# Importar modelo de persona.
from models.persona_model import Persona

@require_safe # Solo permite métodos GET y HEAD.
def list_personas( _ ):
    personas_lista = list( Persona.objects.values() )
    return JsonResponse( personas_lista, safe=False )