from dotenv import load_dotenv
import os

load_dotenv(f"{os.getcwd()}/back/utils/.env")

REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_URL = os.getenv("REDIS_URL")
DATABASE_URL = os.getenv("DATABASE_URL")