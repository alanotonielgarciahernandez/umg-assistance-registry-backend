# media_route.py
# Ruta para servir archivos estáticos.

# Importar módulos de Python.
import os

# Importar módulos de Django.
from django.http import FileResponse
from django.http import HttpResponse
from django.views import View

class MediaView( View ):
    def get( self, request, media_path ) -> FileResponse | HttpResponse:
        # Construir la ruta completa al archivo multimedia.
        media_file_path: str = os.path.join( 'media', media_path )

        # Verificar si el archivo existe y servirlo, o devolver un error 404 si no se encuentra.
        if os.path.exists( media_file_path ):
            return FileResponse( open( media_file_path, 'rb' ), content_type='application/pdf' )
        else:
            return HttpResponse( '<h1>404 Not Found</h1>', status=404 )
