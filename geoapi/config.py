import os

class Config:
    API_KEY = os.environ.get("API_KEY")
    GEO_URL = "https://geocode-maps.yandex.ru/1.x"
    # MONGODB_NAME = "mongo"
    MONGODB_NAME = "localhost"
    DB_PORT = 27017

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    DB_NAME = "dev_cdn"

class TestingConfig(Config):
    TESTING = True
    DB_NAME = "test_cdn"
    MONGODB_NAME = "localhost"

class ProductionConfig(Config):
    DB_NAME = "prod_cdn"

config = {
    "DEV": DevelopmentConfig,
    "TEST": TestingConfig,
    "PROD": ProductionConfig,
    "DEFAULT": DevelopmentConfig
}