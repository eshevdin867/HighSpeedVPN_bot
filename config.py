from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
AMNEZIA_API_URL = os.getenv("AMNEZIA_API_URL")
AMNEZIA_API_KEY = os.getenv("AMNEZIA_API_KEY")
DEFAULT_PROTOCOL = os.getenv(
    "DEFAULT_PROTOCOL",
    "amneziawg2"
)
TARIFFS = {
    "1m": {
        "title": "1 месяц",
        "days": 30,
        "price": 139,
    },
    "3m": {
        "title": "3 месяца",
        "days": 90,
        "price": 379,
    },
    "6m": {
        "title": "6 месяцев",
        "days": 180,
        "price": 659,
    },
    "12m": {
        "title": "12 месяцев",
        "days": 365,
        "price": 1199,
    },
}
