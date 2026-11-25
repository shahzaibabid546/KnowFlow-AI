# Application settings will be implemented in Phase 1.

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is missing from .env file")


settings = Settings()
