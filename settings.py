from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.BOT_TOKEN = getenv("BOT_TOKEN")

        self.DEEPSEEK_API_KEY = getenv("DEEPSEEK_API_KEY")
        self.DEEPSEEK_ENDPOINT = getenv("DEEPSEEK_ENDPOINT")
        self.MODEL = getenv("MODEL")
        self.TEMPERATURE = getenv("TEMPERATURE")
        self.MAX_TOKENS = getenv("MAX_TOKENS")


config = Config()