import os

base_dir = os.path.dirname(os.path.abspath(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(base_dir, 'app_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    PORT = 5000