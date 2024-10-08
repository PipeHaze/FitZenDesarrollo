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
    img.thumbnail((default_width, default_height), Image.ANTIALIAS)

    # Guardar la imagen redimensionada
    img.save(image.path)

# Configura el cifrador
cipher_suite = Fernet(settings.SECRET_KEY.encode())

"Funcion que encripta los slug en la barra de busqueda"
def encrypt_slug(slug):
    """Encripta el slug"""
    slug_bytes = slug.encode('utf-8')
    encrypted_slug = cipher_suite.encrypt(slug_bytes)
    return base64.urlsafe_b64encode(encrypted_slug).decode('utf-8')

def decrypt_slug(encrypted_slug):
    """Desencripta el slug"""
    encrypted_slug_bytes = base64.urlsafe_b64decode(encrypted_slug)
    decrypted_slug = cipher_suite.decrypt(encrypted_slug_bytes)
    return decrypted_slug.decode('utf-8')