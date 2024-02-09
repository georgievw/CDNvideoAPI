from flask import Flask, request, jsonify, abort, make_response, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests
import os

DB_NAME = "dev_cdn"
API_KEY = os.environ.get("API_KEY")
GEO_URL = "https://geocode-maps.yandex.ru/1.x"
MONGODB_NAME = "mongo"
DB_PORT = 27017

app = Flask(__name__)
client = MongoClient(MONGODB_NAME, DB_PORT)
db = client[DB_NAME]
city_db = db["cities"]
city_db.create_index({'loc': '2d'})

def get_city_info(city):

    payload = {"apikey": API_KEY, 
               "geocode": city, 
               "format": "json", 
               "results": 1, 
               "lang": "ru_Ru"}
    
    r = requests.get(GEO_URL, params=payload)

    content = r.json()
    if content['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found'] == '0':
        return {}

    city_loc = content['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    
    city_name = content['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name'] 
    
    return {"name": city_name, "loc": list(map(float, city_loc.split()))}

def make_public_city(city):
    new_city = {}
    for field in city:
        if field == '_id':
            new_city['uri'] = url_for('get_city', city_id=str(city['_id']), _external=True)
        else:
            new_city[field] = city[field]
    return new_city

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)

@app.errorhandler(415)
def unsupported_media_type(error):
    return make_response(jsonify({'error': 'Unsupported Media Type'}), 415)

@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)

@app.route("/api/v1.0/cities", methods=['GET'])
def get_cities():
    cities = city_db.find()
    return jsonify({"cities": list(map(make_public_city, cities))})

@app.route("/api/v1.0/cities", methods=['POST'])
def post_city():
    if not request.json or not "name" in request.json:
        abort(400)

    name = request.json["name"]

    if city_db.find_one({"name": name}) is not None:
        abort(400)

    city_info = get_city_info(name)

    if not city_info or name != city_info["name"]:
        abort(400)

    city = request.json
    city["loc"] = city_info['loc']

    city_db.insert_one(city)
    return jsonify({"city": make_public_city(city)}), 201

@app.route("/api/v1.0/cities/<string:city_id>", methods=['GET'])
def get_city(city_id: str):
    city = city_db.find_one({"_id": ObjectId(city_id)})
    if city is None:
        abort(404)
    return jsonify({"city": make_public_city(city)})

@app.route("/api/v1.0/cities/<string:city_id>", methods=['PUT'])
def put_city(city_id: str):

    if not request.json:
        abort(400)

    city = city_db.find_one({"_id": ObjectId(city_id)})
    if city is None:
        abort(404)

    city_db.update_one({"_id": ObjectId(city_id)}, {"$set": request.json})
    city = city_db.find_one({"_id": ObjectId(city_id)})

    return jsonify({"city": make_public_city(city)}), 200

@app.route("/api/v1.0/cities/<string:city_id>", methods=['DELETE'])
def delete_city(city_id: str):
    abort(405) 

@app.route("/api/v1.0/cities/<string:city_id>/nearest", methods=['GET'])
def get_nearest_cities(city_id: str):
    n = request.args.get('n')
    
    if n is None:
        n = 2
    elif not n.isdigit():
        abort(400)

    city = city_db.find_one({"_id": ObjectId(city_id)})
    if city is None:
        abort(404)
    loc = city['loc']

    near_cities = city_db.find({"loc": {"$near": loc}}).skip(1).limit(n)
    if not near_cities:
        abort(404)
    return jsonify({"cities": list(map(make_public_city, near_cities))})

@app.route("/api/v1.0/nearest", methods=['GET'])
def get_point_nearest_cities():
    long = request.args.get('long')
    lat = request.args.get('lat')
    n = request.args.get('n')
    
    if n is None:
        n = 2
    elif not n.isdigit():
        abort(400)

    try:
        float(long), float(lat)
    except:
        abort(400)
    
    near_cities = city_db.find({"loc": {"$near": [float(long), float(lat)]}}).limit(n)
    if not near_cities:
        abort(404)
    return jsonify({"cities": list(map(make_public_city, near_cities))})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")