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
    