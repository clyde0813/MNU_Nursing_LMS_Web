from .base import *

DEBUG = False

ALLOWED_HOSTS = ['teamkimedu.com']

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR, "NAS/file")
MEDIA_URL = '/file/'