import os

from dotenv import load_dotenv


# Загружаем переменные из .env (если файл есть).
# В Docker переменные придут из окружения, load_dotenv не помешает.
load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Please configure it in .env or environment.")

if not DB_PASSWORD:
    raise RuntimeError("DB_PASSWORD is not set. Please configure it in .env or environment.")


