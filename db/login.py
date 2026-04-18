# iniciar_sesion.py
# Script para manejar el proceso de inicio de sesión.

# Importar modelo de usuario.
from models.usuario_model import Usuario

def try_login( correo: str, password: str ) -> Usuario | None:
    # Buscamos si el correo existe en la base de datos y obtenemos su modelo.
    usuario: Usuario = Usuario.objects.filter( correo=correo ).first()
    if not usuario:
        return None

    # Comparar contraseñas.
    if usuario.password != password:
        return None

    return usuario