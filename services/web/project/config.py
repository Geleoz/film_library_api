"""
Module for configuration flask app in __init__.py file
"""
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Contains all required keys for configuration
    """
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SECRET_KEY = "7c427109c6d9bae6ad5ee982"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = "cerulean"
