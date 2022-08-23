import os

que = {}
admins = {}

BG_IMG = os.environ.get("BG_IMG", "https://telegra.ph/file/f2a2d31f60a9e0f3dbe94.png")
START_PIC = os.environ.get("START_PIC", "https://telegra.ph/file/f2a2d31f60a9e0f3dbe94.png")
OWNER_USERNAME = os.environ.get("OWNER_USERNAME")
IMG_1 = os.environ.get("IMG_1", "https://telegra.ph/file/3b663a7e9a414304c084f.jpg")
IMG_2 = os.environ.get("IMG_2", "https://telegra.ph/file/6213d2673486beca02967.png")
IMG_3 = os.environ.get("IMG_3", "https://telegra.ph/file/f02efde766160d3ff52d6.png")
IMG_4 = os.environ.get("IMG_4", "https://telegra.ph/file/be5f551acb116292d15ec.png")

SESSION_STRING = os.environ.get("SESSION_STRING", None)
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
API_ID = int(os.environ.get("API_ID", None))
API_HASH = os.environ.get("API_HASH",None)
OWNER_ID = os.environ.get("OWNER_ID", None)
SUDOS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)
UPDATE = os.environ.get("UPDATE", None)
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
DURATION_LIMIT = int(os.environ.get("DURATION_LIMIT", "600"))
CMD_MUSIC = list(os.environ.get("CMD_MUSIC", "/ !").split())
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
LOG_CHANNEL = os.environ.get("LOG_CHANNEL", None)

SUDO_USERS = SUDOS.add(OWNER_ID)