from django.http import JsonResponse
from models.usuario_model import Usuarios

def login( request ):
    usuarios_lista = list(Usuarios.objects.values())
    return JsonResponse(usuarios_lista, safe=False)
