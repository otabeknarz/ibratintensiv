import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.BOT_TOKEN = os.getenv("BOT_TOKEN")
        self.ADMINS = {
            "Otabek": 5551503420,
            "Umida": 1499657324,
        }

        self.CHANNEL = os.getenv("CHANNEL")
        self.GIFT_GROUP = os.getenv("GIFT_GROUP")

        # URLs
        self.URL = "https://otabek.me/ibrat/"
        self.STATS_URL = self.URL + "stats/"
        self.ADD_PEOPLE_URL = self.URL + "add-tg-people/"
        self.GET_PEOPLE_URL = self.URL + "get-tg-people/"
        self.INVITE_TG_FRIEND = self.URL + "invite-tg-friend/"
        self.GET_PEOPLE_IDS = self.URL + "get-people-ids/"
        self.HAS_INVITED_PEOPLE_IDS = self.URL + "has-invited-people-ids"


@lru_cache
def get_settings():
    return Settings()
