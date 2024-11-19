from dotenv import load_dotenv
import os
load_dotenv()

class conf:
    host = os.getenv("DB_HOST", "127.0.0.1")
    database = os.getenv("DB_DATABASE", "sandwich_maker_api")
    port = int(os.getenv("DB_PORT", 3306))
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    app_host = os.getenv("APP_HOST", "localhost")
    app_port = int(os.getenv("APP_PORT", 8000))
