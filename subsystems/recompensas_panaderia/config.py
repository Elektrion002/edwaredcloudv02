import os

class Config:
    # Database configuration for Subsistema 01
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://edwared_admin:MEwar3x4-12VpS@localhost:5433/db_rpanaderia001'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'recompensas-panaderia-secret-key-2026'
