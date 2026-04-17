# media_route.py
# Ruta para servir archivos estáticos.

# Importar módulos de Python.
import os

# Importar módulos de Django.
from django.http import FileResponse
from django.http import HttpResponse

def serve_media( request, media_path ):
    media_file_path = os.path.join( 'media', media_path )

    if os.path.exists( media_file_path ):
        return FileResponse( open( media_file_path, 'rb' ), content_type='application/pdf' )
    else:
        return HttpResponse( '<h1>404 Not Found</h1>', status=404 )
