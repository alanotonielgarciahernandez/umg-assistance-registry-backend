# signature_report.py
# Firma digital de documentos PDF.

# Importar módulos de Python.
import os

# Importar módulos de terceros.
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers

def firmar_pdf( pdf_path: str ):
    # Cargar el certificado digital desde un archivo.
    try:
        signer = signers.SimpleSigner.load_pkcs12(
            pfx_file=os.getenv( 'CERT_PATH' ),
            passphrase=bytes( os.getenv( 'CERT_PASSWORD' ), 'utf-8' )
        )
    except Exception as e:
        # Ignorar el error de carga del certificado y continuar sin firmar.
        return

    # Abrir el PDF y preparar para la firma.
    with open( pdf_path, 'rb' ) as doc:
        w = IncrementalPdfFileWriter( doc )
        
        # Firmar el PDF.
        out = signers.sign_pdf(
            w,
            signers.PdfSignatureMetadata(
                field_name='Signature1',
            ),
            signer=signer,
        )

    # Guardar el PDF firmado sobre el archivo original.
    with open( pdf_path, 'wb') as f:
        f.write( out.getvalue() )
