import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from models.usuario_model import Usuarios

@csrf_exempt
def login(request):
    # Verificamos que envíen datos
    if request.method == 'POST':
        try:
            # 1 y 2. Sacamos correo y contraseña del body
            body = json.loads(request.body)
            correo_ingresado = body.get('correo')
            password_ingresado = body.get('password')

            # 3. Buscamos si el correo existe en la base de datos
            usuario = Usuarios.objects.filter(correo=correo_ingresado).first()

            if usuario:
                # 4. Si el correo coincide, comparamos la contraseña
                if usuario.password == password_ingresado:
                    # 5. Todo coincide -> devolvemos código 200
                    return JsonResponse({"mensaje": "Login exitoso"}, status=200)
                else:
                    return JsonResponse({"error": "Contraseña incorrecta"}, status=401)
            else:
                return JsonResponse({"error": "El correo no existe"}, status=404)

        except Exception as e:
            return JsonResponse({"error": "Datos inválidos"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)
