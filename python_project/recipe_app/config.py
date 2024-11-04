import os

class Config:
    SECRET_KEY = 'supersecretkey'
    JWT_SECRET_KEY = 'anothersecretkey'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:password@db/recipedb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False 
    JWT_ACCESS_COOKIE_PATH = '/' 
    JWT_COOKIE_CSRF_PROTECT = False 