import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URL")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_URL = os.environ.get("DB_URL")
    HASH_SECRET = os.environ.get("HASH_SECRET")


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True


class ProductionConfig(Config):
    DATABASE_URI = ""

