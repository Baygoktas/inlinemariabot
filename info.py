import string
import random
import re
from os import environ
import time

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y", "e"]: return True
    elif value.lower() in ["false", "no", "0", "disable", "n", "h"]: return False
    else: return default

# Bot information
SESSION = environ.get('SESSION', 'kitapmaria ' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)))
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']
botStartTime = time.time()
# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'dosyalar')

# Others
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
BUTTON_COUNT = int(environ.get('BUTTON_COUNT', 10))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'GercekArsivler')
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "@baygoktass")
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))

LOG_STR = "Current Cusomized Configurations are:-\n"
