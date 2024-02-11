from flask import Flask, current_app
from config import config
from pymongo import MongoClient

# client = MongoClient(current_app.config['MONGODB_NAME'], current_app.config['DB_PORT'])
# db = client[current_app.config['DB_NAME']]
# city_db = db["cities"]
# city_db.create_index({'loc': '2d'})
# city_db = 0

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)#, url_prefix='/api/v1')

    # global city_db
    # client = MongoClient(config[config_name].MONGODB_NAME, config[config_name].DB_PORT)
    # db = client[config[config_name].DB_NAME]
    # city_db = db["cities"]
    # city_db.create_index({'loc': '2d'})

    return app