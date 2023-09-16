import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:1piAdFNkOc5vdyRJUIisLzhptVhsbGJV@dpg-ck2i15eru70s7382cdtg-a.singapore-postgres.render.com/aigo_t3fs'


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
