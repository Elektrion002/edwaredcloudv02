import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = True
    # PostgreSQL Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://edwared_admin:MEwar3x4-12VpS@localhost:5433/edwared_master'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
