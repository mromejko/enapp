import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(env_path):
    load_dotenv(env_path)

def set_boolean(_val):
    if str.lower(_val) == 'true':
        return True
    return False

EXTENSIONS = [
    'api.extensions:db',
    'api.extensions:migrate'
]

class Config(object):
    # APP CONFIG
    SECRET_KEY = os.getenv('SECRET_KEY')
    API_KEY = os.getenv('API_KEY')
    DEBUG = set_boolean(os.getenv('DEBUG'))
    FLASK_ENV = os.getenv('FLASK_ENV')
    FLASK_APP = os.getenv('FLASK_APP')
    SERVER_NAME = os.getenv('SERVER_NAME')
    SESSION_COOKIE_DOMAIN = os.getenv('SERVER_HOST')

    # DB CONFIG
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = set_boolean(os.getenv('SQLALCHEMY_ECHO'))
    SQLALCHEMY_TRACK_MODIFICATIONS = set_boolean(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))

    # RABBITMQ
    RABBIT_HOST = os.getenv('RABBIT_HOST')
    RABBIT_PORT = os.getenv('RABBIT_PORT')
    RABBIT_QUEUE = os.getenv('RABBIT_QUEUE')