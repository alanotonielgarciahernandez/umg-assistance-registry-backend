from django.http import JsonResponse
from django.views.decorators.http import require_safe

# Importamos los modelos
from models.puerta_model import Puertas
from models.registro_puerta_model import RegistroPuertaPrincipal
from middlewares.validar_JWT import validateJWT

@require_safe
def reporte_puerta_historico(request):
    # 1. El guardia revisa el token
    validar_JWT_response = validateJWT(request)
    if validar_JWT_response:
        return validar_JWT_response
    
    # 2. Agarramos los datos que nos mandan en la URL (id_instalacion y id_puerta)
    id_instalacion = request.GET.get('id_instalacion')
    id_puerta = request.GET.get('id_puerta')

    if not id_instalacion or not id_puerta:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

    # 3. Validar que la puerta de verdad pertenezca a ese edificio
    puerta_existe = Puertas.objects.filter(id_puerta=id_puerta, id_instalacion=id_instalacion).exists()
    if not puerta_existe:
        return JsonResponse({'error': 'La puerta no pertenece a la instalación'}, status=400)

    # 4. Traemos todos los ingresos de esa puerta donde SÍ se identificó a la persona
    registros = RegistroPuertaPrincipal.objects.filter(
        id_puerta=id_puerta, 
        id_persona__isnull=False
    ).select_related('id_persona').order_by('-fecha_hora') # order_by('-fecha_hora') los ordena del más reciente al más viejo

    # 5. Aquí vamos a agrupar todo por fecha usando un diccionario
    agrupado = {}

    for reg in registros:
        # Sacamos la fecha (Ej. 2026-04-14) y la hora (Ej. 07:35)
        fecha_str = reg.fecha_hora.strftime('%Y-%m-%d')
        hora_str = reg.fecha_hora.strftime('%H:%M')

        # Si esta fecha aún no existe en nuestro grupo, la creamos vacía
        if fecha_str not in agrupado:
            agrupado[fecha_str] = {
                "fecha": fecha_str,
                "total_ingresos": 0,
                "personas": []
            }
        
        # Le sumamos 1 al total de ingresos de ese día
        agrupado[fecha_str]["total_ingresos"] += 1

        # Metemos a la persona en la lista de ese día
        persona = reg.id_persona
        agrupado[fecha_str]["personas"].append({
            "id_persona": persona.id_persona,
            "nombre": persona.nombre,
            "apellido": persona.apellido,
            "correo": persona.correo,
            "fotografia_path": persona.fotografia_path,
            "hora": hora_str
        })

    # 6. Convertimos nuestro diccionario a una lista normal para enviarlo
    resultado = list(agrupado.values())

    return JsonResponse(resultado, safe=False)


@require_safe
def reporte_puerta_fecha(request):
    # 1. El guardia revisa el token
    validar_JWT_response = validateJWT(request)
    if validar_JWT_response:
        return validar_JWT_response
    
    # 2. Agarramos los datos que nos mandan (instalación, puerta, fecha y orden)
    id_instalacion = request.GET.get('id_instalacion')
    id_puerta = request.GET.get('id_puerta')
    fecha = request.GET.get('fecha')
    orden = request.GET.get('orden', 'ASC').upper() # Por defecto los ordenamos normal (ASC)

    if not id_instalacion or not id_puerta or not fecha:
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)

    # 3. Validar que la puerta exista en ese edificio
    puerta_existe = Puertas.objects.filter(id_puerta=id_puerta, id_instalacion=id_instalacion).exists()
    if not puerta_existe:
        return JsonResponse({'error': 'La puerta no pertenece a la instalación'}, status=400)

    # 4. Configurar si los queremos del más viejo al más nuevo o al revés
    order_prefix = '-' if orden == 'DESC' else ''

    # 5. Buscar TODOS los registros de esa puerta en esa fecha específica
    # Nota: usamos __date para que solo busque por el día, ignorando la hora
    registros = RegistroPuertaPrincipal.objects.filter(
        id_puerta=id_puerta,
        fecha_hora__date=fecha
    ).select_related('id_persona').order_by(f"{order_prefix}fecha_hora")

    resultado = []

    # 6. Recorrer la lista y armar las cajitas de respuesta
    for reg in registros:
        persona = reg.id_persona
        
        # Si sí detectamos quién era:
        if persona:
            resultado.append({
                "id_persona": persona.id_persona,
                "nombre": persona.nombre,
                "apellido": persona.apellido,
                "correo": persona.correo,
                "fotografia_path": persona.fotografia_path,
                "fecha_hora": reg.fecha_hora.strftime('%Y-%m-%dT%H:%M:%S'),
                "estado": "PRESENTE"
            })
        # Si fue alguien que no se identificó:
        else:
            resultado.append({
                "id_persona": None,
                "nombre": "Desconocido",
                "apellido": "",
                "correo": None,
                "fotografia_path": None,
                "fecha_hora": reg.fecha_hora.strftime('%Y-%m-%dT%H:%M:%S'),
                "estado": "DESCONOCIDO"
            })

    return JsonResponse(resultado, safe=False)
