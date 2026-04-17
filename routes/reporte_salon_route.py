from django.http import JsonResponse
from django.views.decorators.http import require_safe

from models.salon_model import Salon
from models.registro_model import IngresoSalon
from middlewares.validar_JWT import validateJWT

@require_safe
def reporte_salon_historico( request ):
    validar_JWT_response = validateJWT(request)
    if validar_JWT_response: return validar_JWT_response

    id_instalacion = request.GET.get( 'id_instalacion' )
    id_salon = request.GET.get( 'id_salon' )

    if not id_instalacion or not id_salon:
        return JsonResponse( { 'error': 'Faltan parámetros' }, status=400 )

    # Validar que el salón exista en la instalación [cite: 283]
    if not Salon.objects.filter( id_salon=id_salon, instalacion__id_instalacion=id_instalacion ).exists():
        return JsonResponse( { 'error': 'El salón no pertenece a la instalación' }, status=400 )

    # Traer ingresos del salón ordenados del más nuevo al más viejo [cite: 285]
    registros = IngresoSalon.objects.filter(
        salon__id_salon=id_salon,
        persona__id_persona__isnull=False
    ).order_by( '-fecha_hora' )

    agrupado = {}

    for reg in registros:
        fecha_str = reg.fecha_hora.strftime( '%Y-%m-%d' )
        hora_str = reg.fecha_hora.strftime( '%H:%M' )

        if fecha_str not in agrupado:
            agrupado[ fecha_str ] = { "fecha": fecha_str, "total_ingresos": 0, "personas": [] }
        
        agrupado[ fecha_str ][ "total_ingresos" ] += 1
        persona = reg.persona
        
        # Obtenemos el tipo_persona (si no existe en tu modelo actual, por defecto ponemos ESTUDIANTE) [cite: 286]
        tipo = getattr( persona, 'tipo_persona', 'ESTUDIANTE' )

        agrupado[ fecha_str ][ "personas" ].append( {
            "id_persona": persona.id_persona,
            "nombre": persona.nombre,
            "apellido": persona.apellido,
            "correo": persona.correo,
            "fotografia_path": persona.fotografia_path,
            "hora": hora_str,
            "tipo_persona": tipo
        } )

    return JsonResponse( list( agrupado.values() ), safe=False )


@require_safe
def reporte_salon_fecha( request ):
    validar_JWT_response = validateJWT( request )
    if validar_JWT_response: return validar_JWT_response

    id_instalacion = request.GET.get( 'id_instalacion' )
    id_salon = request.GET.get( 'id_salon' )
    fecha = request.GET.get( 'fecha' )

    if not id_instalacion or not id_salon or not fecha:
        return JsonResponse( { 'error': 'Faltan parámetros' }, status=400 )

    if not Salon.objects.filter( id_salon=id_salon, instalacion__id_instalacion=id_instalacion ).exists():
        return JsonResponse( { 'error': 'El salón no pertenece a la instalación' }, status=400 )

    # Traer ingresos de esa fecha específica [cite: 327]
    registros = IngresoSalon.objects.filter(
        salon__id_salon=id_salon,
        fecha_hora__date=fecha,
        persona__id_persona__isnull=False
    ).order_by( 'fecha_hora' )

    resultado = []

    for reg in registros:
        persona = reg.persona
        tipo = getattr( persona, 'tipo_persona', 'ESTUDIANTE' )
        resultado.append( {
            "id_persona": persona.id_persona,
            "nombre": persona.nombre,
            "apellido": persona.apellido,
            "correo": persona.correo,
            "fotografia_path": persona.fotografia_path,
            "fecha_hora": reg.fecha_hora.strftime( '%Y-%m-%dT%H:%M:%S' ),
            "tipo_persona": tipo
        } )

    return JsonResponse( resultado, safe=False )