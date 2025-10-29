import os
from sqlalchemy import Column, Interger, String, Foreignkey
from sqlalchemy.orm import relationship
from app import db

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}

# Relationship ---
class PL(db.Model):
    __tablename__ = 'parents'
    id = Column(Integer, primary_key=True)
    children = relationship('Child', backref='parent', lazy=True)

class Child(db.Model):
    __tablename__ = 'children'
    id = Column(Integer, primary_key=True)

