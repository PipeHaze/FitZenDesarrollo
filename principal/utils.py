from PIL import Image
from django.conf import settings
from cryptography.fernet import Fernet
import base64

def resize_image(image):
    # Obtener el tamaño predeterminado de las imágenes
    default_width = settings.DEFAULT_WIDTH
    default_height = settings.DEFAULT_HEIGHT

    # Abrir la imagen utilizando Pillow
    img = Image.open(image)

    # Redimensionar la imagen al tamaño predeterminado
    img.thumbnail((default_width, default_height), Image.LANCZOS)

    # Guardar la imagen redimensionada
    img.save(image.path)

# Configura el cifrador
cipher_suite = Fernet(settings.SECRET_KEY.encode())

"Funcion que encripta los slug en la barra de busqueda"

def encrypt_slug(slug):
    slug_bytes = slug.encode('utf-8')
    encoded_slug = base64.urlsafe_b64encode(slug_bytes).decode('utf-8')
    return encoded_slug.rstrip('=')  # Elimina el relleno '='

def decrypt_slug(encrypted_slug):
    # Añade el relleno '=' si es necesario
    padding_needed = len(encrypted_slug) % 4
    if padding_needed:
        encrypted_slug += '=' * (4 - padding_needed)
    slug_bytes = base64.urlsafe_b64decode(encrypted_slug.encode('utf-8'))
    return slug_bytes.decode('utf-8')