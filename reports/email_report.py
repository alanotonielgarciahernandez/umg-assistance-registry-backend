# email_report.py
# Reporte de asistencia por correo electrónico.

# Importar módulos de Python.
from datetime import date
import os
import smtplib

# Importar módulos de terceros.
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# Importar modelos.
from models.curso_model import Curso
from models.usuario_model import Usuario

def enviar_email_registro_asistencia( pdf_path: str, email_receptor: str, id_asignacion: int, fecha: date, user: Usuario ) -> bool:
    # Obtener información del curso desde la base de datos.
    curso: Curso = Curso.objects.get( id_asignacion=id_asignacion )

    # Crear el mensaje de correo electrónico.
    message = MIMEMultipart()
    message[ 'From' ] = os.getenv( 'EMAIL_EMISOR' )
    message[ 'To' ] = email_receptor
    message[ 'Subject' ] = 'Registro de Asistencia'

    # Texto simple en el cuerpo del correo con información del archivo adjunto.
    body_text = (
        f'Estimado/a { user.persona.nombre } { user.persona.apellido },\n\n'
        f'Le informamos que se ha registrado su asistencia para el curso: { curso.nombre_curso } el día { fecha }.\n\n'
        'Por favor revise el documento y confirme la recepción.\n\n'
        'Saludos cordiales,\nUniversidad Mariano Gálvez de Guatemala'
    )
    message.attach( MIMEText( body_text, 'plain' ) )

    # Adjunta el archivo PDF.
    with open( pdf_path, 'rb' ) as attachment:
        part = MIMEBase( 'application', 'octet-stream' )
        part.set_payload( attachment.read() )
        encoders.encode_base64( part )

    # Agregar encabezado para indicar que es un archivo adjunto.
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= { pdf_path.split( '/' )[ -1 ] }',
    )

    # Adjuntar el archivo al mensaje.
    message.attach( part )

    # Enviar el correo electrónico.
    try:
        with smtplib.SMTP( os.getenv( 'EMAIL_SMTP_SERVER' ), int( os.getenv( 'EMAIL_SMTP_PORT', 587 ) ) ) as server:
            # Activar TLS para seguridad.
            server.starttls()

            # Iniciar sesión en el servidor SMTP.
            server.login( os.getenv( 'EMAIL_EMISOR' ), os.getenv( 'EMAIL_PASSWORD' ) )
            
            # Enviar el correo electrónico.
            server.sendmail( os.getenv( 'EMAIL_EMISOR' ), email_receptor, message.as_string() )

            # Enviar el correo electrónico al mismo emisor para mantener un registro de los correos enviados.
            server.sendmail( os.getenv( 'EMAIL_EMISOR' ), os.getenv( 'EMAIL_EMISOR' ), message.as_string() )

        return True
    except Exception:
        return False
