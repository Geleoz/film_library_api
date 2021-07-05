import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SECRET_KEY = "7c427109c6d9bae6ad5ee982"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
