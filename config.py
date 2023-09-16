import os

class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    LINE_PAY_ID = '2000605545'
    LINE_PAY_SECRET = '4709c50681e7176c83fd68c6c753859f'

    STORE_IMAGE_URL = 'https://i.imgur.com/OJ2iFOQ.png'

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:umzbQfh2wm5m4ZQaJtZSsyOaoV1z7Wbc@dpg-ck2jvsr6fquc73dcsl1g-a.singapore-postgres.render.com/aigodb_m9m0'
    
class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')



    

    

