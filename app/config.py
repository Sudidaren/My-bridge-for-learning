import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-key-change-this')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'surveyjs')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour