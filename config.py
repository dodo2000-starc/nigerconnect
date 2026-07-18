import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nigerconnect-secret-key-2024-change-me'
    
    # Base de données
    # Sur Render : utilise PostgreSQL (variable DATABASE_URL fournie automatiquement)
    # En local : utilise SQLite
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///nigerconnect.db')
    
    # Render fournit "postgres://" mais SQLAlchemy veut "postgresql://"
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-niger-secret-change-me'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    ITEMS_PER_PAGE = 12
    
    SMS_API_KEY = os.environ.get('SMS_API_KEY') or ''
    SMS_SENDER = 'NigerConnect'
    
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or ''

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}