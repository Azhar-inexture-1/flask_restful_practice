import os
from dotenv import load_dotenv

# take environment variables from .env.
load_dotenv()

username = os.environ.get('username')
password = os.environ.get('password')
database = os.environ.get('database')
port = os.environ.get('port')
host = os.environ.get('host')

SECRET_KEY = os.environ.get('SECRET_KEY')

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

TWITTER_CLIENT_ID = os.environ.get('TWITTER_CLIENT_ID')
TWITTER_CLIENT_SECRET = os.environ.get('TWITTER_CLIENT_SECRET')

GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')


class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{username}:{password}@{host}:{port}/{database}"

    PROPAGATE_EXCEPTIONS = True
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    EXPIRE_TIME_FOR_ACCESS_TOKEN_IN_MINUTES = 1440
    EXPIRE_TIME_FOR_REFRESH_TOKEN_IN_HOURS = 720

    SECRET_KEY = SECRET_KEY

    GOOGLE_CLIENT_ID = GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET = GOOGLE_CLIENT_SECRET

    TWITTER_CLIENT_ID = TWITTER_CLIENT_ID
    TWITTER_CLIENT_SECRET = TWITTER_CLIENT_SECRET

    GITHUB_CLIENT_ID = GITHUB_CLIENT_ID
    GITHUB_CLIENT_SECRET = GITHUB_CLIENT_SECRET
    