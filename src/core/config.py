import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "dev")
JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALGO = os.getenv("JWT_ALGO", "HS256")
