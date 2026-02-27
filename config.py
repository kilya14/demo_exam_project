import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-exam-key-2026'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///demo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
