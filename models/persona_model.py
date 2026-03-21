# persona_model.py
# Modelo de personas.

# Importar módulos de Django.
from django.db import models

# Modelo de persona.
class Persona( models.Model ):
    id_persona = models.AutoField( primary_key=True )
    nombre = models.CharField( max_length=50 )
    apellido = models.CharField( max_length=50 )
    telefono = models.CharField( max_length=20, null=True )
    correo = models.CharField( max_length=100, null=True )
    tipo_persona = models.CharField( max_length=20, null=True )
    carrera = models.CharField( max_length=100, null=True )
    seccion = models.CharField( max_length=10, null=True )
    fotografia_path = models.CharField( max_length=255, null=True )
    vector_facial = models.TextField( null=True )
    carnet = models.CharField( max_length=20, null=True )
    qr_path = models.CharField( max_length=255, null=True )
    fecha_registro = models.DateTimeField( null=True )

    # Metadatos del modelo.
    class Meta:
        db_table = "personas"
        verbose_name = "Persona"

    # Representación en cadena del modelo.
    def __str__(self):
        return f"{ self.nombre } - { self.tipo_persona }"