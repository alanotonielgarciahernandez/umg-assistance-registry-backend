# routes.py
# Definición de rutas para la API.

# Importar módulos de Django.
from django.http import HttpResponse
from django.views.decorators.http import require_safe

# Importar modelo de persona.
from models.persona_model import Persona

@require_safe # Solo permite métodos GET y HEAD.
def list_personas( request ):
    return HttpResponse( Persona.objects.all().values() )