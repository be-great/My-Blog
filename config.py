class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///DB/database.db'
    SECRET_KEY = 'dkmwkefwoefwoef34324kfjew'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
