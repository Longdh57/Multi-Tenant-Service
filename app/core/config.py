import os

from dotenv import load_dotenv
from pydantic import BaseSettings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Settings(BaseSettings):
    PROJECT_NAME = os.getenv('PROJECT_NAME', '')
    DEBUG = os.getenv('DEBUG', True)
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    BACKEND_CORS_ORIGINS = ['*']
    BASE_API_PREFIX = '/api'
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # Token expired after 7 days
    SECURITY_ALGORITHM = 'HS256'
    LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, 'logging.ini')

    DATABASE_URL = os.getenv('SQL_DATABASE_URL', '')
    VNLIFE_DATABASE_URL = os.getenv('VNLIFE_DATABASE_URL', '')
    PV_VNSHOP_KA_DATABASE_URL = os.getenv('PV_VNSHOP_KA_DATABASE_URL', '')

    AUTHENTICATION_SERVICE = ''

settings = Settings()
