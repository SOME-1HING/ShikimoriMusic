
import os

que = {}
admins = {}

BG_IMG = os.environ.get("BG_IMG", "https://i.imgur.com/W3Jyec6.jpg")
START_PIC = BG_IMG
OWNER_USERNAME = os.environ.get("OWNER_USERNAME")

SESSION_STRING = os.environ.get("SESSION_STRING", "BQA5F0_rr4R36nVsXC-sPsVRyECKiF_QyKJ6KTNlknLbnZChGkb_5q6SHRhcldbKksoi2MjQNTJPyCcy0l67swJoa7SNTGrc1pX9ZuHmvPTPSS-uJLMtO9t4mkFtQfpF-ix4zibvcrtlX9Rfu7TpYZws72EWNE23DPcUc8_jrIsZZISJ9JOcy2QiIuJn5h0gQbQYpIVRxSkGaib0lpCNek7wGM2-Q496p-NMejm3tJ1ChlT_GebLOE9U6ylKq-dndSsTKZQ4Pt3VUORSfB5eLKkJarHQdbm73Juokry1MaQlmpiXZnJy0gdDlDHx99neFbIelS5dFg-l-u2bed9y9lXGAAAAAVk96xYA")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "5701010726:AAG8G_LjfXiGvUM2O-EgrRdEFoDQ7JvpGFk")
API_ID = int(os.environ.get("API_ID", "9926217"))
API_HASH = os.environ.get("API_HASH","05425a93e4dc4a0cb14f449f01fd25e4")
OWNER_ID = int(os.environ.get("OWNER_ID", "5598826878"))
SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", "LisaXSupport")
UPDATE = os.environ.get("UPDATE", "LisaXUpdates")
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
DURATION_LIMIT = int(os.environ.get("DURATION_LIMIT", "600"))
CMD_MUSIC = list(os.environ.get("CMD_MUSIC", "/ !").split())
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", "mongodb+srv://Rick2:Pagalbot@cluster0.fhy1l28.mongodb.net/?retryWrites=true&w=majority")
LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "-1001504201905")


SUDO_USERS = (OWNER_ID, 5499316076)
