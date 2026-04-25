import os

DB_CONFIG = {
    "host": "localhost",
    "dbname": "hybrid_search",
    "user": "postgres",
    "password": "password",
    "port": 5432
}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")