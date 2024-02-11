from flask import Blueprint, current_app
from pymongo import MongoClient

api = Blueprint('api', __name__)

# client = MongoClient(current_app.config['MONGODB_NAME'], current_app.config['DB_PORT'])
# db = client[current_app.config['DB_NAME']]
# city_db = db["cities"]
# city_db.create_index({'loc': '2d'})

from . import cities, errors