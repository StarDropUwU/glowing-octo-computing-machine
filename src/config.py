import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "qz27o8t5m9ocmufnafagnirm33ubc2sb")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL","postgresql://financial:strx4012@localhost:5432/postgres")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
