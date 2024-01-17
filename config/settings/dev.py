from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

MEDIA_ROOT = os.path.join(BASE_DIR, 'file')
MEDIA_URL = '/file/'
