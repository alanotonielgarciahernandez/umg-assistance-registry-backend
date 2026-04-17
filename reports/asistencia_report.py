# asistencia_report.py
# Script para generar un reporte de asistencia en formato PDF.

# Importar módulos de Python.
from datetime import date

# Importar módulos de terceros.
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

# Importar modelos.
from models.registro_model import Asistencia
from models.curso_model import Curso
from models.persona_model import Persona

def generar_registro_asistencia( id_asignacion: int, fecha_asistencia: date, lista_asistencia: list[ dict ] ):
    course: Curso = Curso.objects.get( id_asignacion=id_asignacion )

    assitance_list: list[ Asistencia ] = [
        Asistencia(
            persona=Persona.objects.get( id_persona=assistance[ 'id_persona' ] ),
            estado=assistance[ 'estado' ],
        )
        for assistance in lista_asistencia
    ]

    # Posición vertical en donde dibujar objetos.
    canvas_y_position = 750

    # Crear un nuevo PDF.
    c = canvas.Canvas( f'media/asistencia-{ id_asignacion }-{ fecha_asistencia }.pdf', pagesize=letter )

    # Dibujar el título del reporte.
    c.setFont( 'Helvetica-Bold', 18 )
    c.drawCentredString( 306, canvas_y_position, 'Reporte de Asistencia' )
    c.setFont( 'Helvetica', 12 )
    # Mover la posición vertical hacia abajo para el contenido.
    canvas_y_position -= 20

    # Dibujar información del curso.
    c.drawString( 100, canvas_y_position, 'Curso: ' + course.nombre_curso )
    canvas_y_position -= 20

    # Dibujar información de la fecha.
    c.drawString( 100, canvas_y_position, 'Fecha: ' + str( fecha_asistencia ) )
    canvas_y_position -= 20

    # Dibujar información del horario.
    c.drawString( 100, canvas_y_position, 'Horario: ' + course.horario )
    canvas_y_position -= 20

    # Dibujar información del salón.
    c.drawString( 100, canvas_y_position, 'Salón: ' + course.salon.nombre )
    canvas_y_position -= 100

    # Crear tabla de asistencia.
    table = Table(
        # Agregar valores de la tabla.
        data = [
            # Encabezados de la tabla.
            [ 'Foto', 'Nombre', 'Estado', ],
            # Filas de datos.
            *[
                [
                    assistance.persona.fotografia_path,  # Aquí se podría agregar la lógica para mostrar la foto real.
                    f"{ assistance.persona.nombre } { assistance.persona.apellido }",
                    assistance.estado,
                ]
                for assistance in assitance_list
            ],
        ],

        # Ancho de las columnas.
        colWidths = [ 137, 137, 137 ],

        # Estilo de la tabla.
        style = TableStyle( [
            ( 'GRID', ( 0, 0 ), ( -1, -1 ), 1, colors.black ),
        ] )
    )
    
    # Dibujar la tabla en el PDF.
    table.wrapOn( c, 100, canvas_y_position )
    table.drawOn( c, 100, canvas_y_position )

    # Guardar el PDF.
    c.save()

    return f'media/asistencia-{ id_asignacion }-{ fecha_asistencia }.pdf'