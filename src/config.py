import os


TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

DB_NAME = os.environ.get('DATABASE_NAME') or 'seeme'
DB_USER = os.environ.get('DATABASE_USER') or 'postgres'
DB_PASSWORD = os.environ.get('DATABASE_PASSWORD') or 'postgres'
DB_HOST = os.environ.get('DATABASE_HOST') or 'localhost'
DB_PORT = os.environ.get('DATABASE_PORT') or 5432

CACHE_URL = os.environ.get('CACHE_URL') or "redis://localhost:6379"


MEDIA_PATH = os.path.join(os.getcwd(), "www/images")

