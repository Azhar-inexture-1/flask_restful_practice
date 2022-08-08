import os
from dotenv import load_dotenv

# take environment variables from .env.
load_dotenv()

username = os.environ.get('username')
password = os.environ.get('password')
database = os.environ.get('database')
port = os.environ.get('port')
host = os.environ.get('host')

class Config:    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{username}:{password}@{host}:{port}/{database}"
    EXPIRE_TIME_FOR_ACCESS_TOKEN_IN_MINUTES = 1440
    EXPIRE_TIME_FOR_REFRESH_TOKEN_IN_HOURS = 720
    SECRET_KEY = os.environ.get('SECRET_KEY')
    