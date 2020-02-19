import os

DATABASE_URL = 'sqlite:///chat.db'


PROD_PG_USER = os.getenv("PROD_DATABASE_USER", 'market_user')
PROD_PG_PASSWORD = os.getenv("PROD_DATABASE_PASSWORD", 'pass12pass')
PROD_PG_HOST = os.getenv("PROD_DATABASE_HOST", 'localhost')
PROD_PG_PORT = os.getenv("PROD_DATABASE_PORT", '5432')
PROD_PG_NAME = os.getenv("PROD_DATABASE_NAME", 'market_dev')
# PROD_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
