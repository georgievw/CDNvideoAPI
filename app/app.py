from flask import Flask, request, jsonify, abort, make_response
from pymongo import MongoClient
from bson.json_util import dumps 
import json
import requests

DB_NAME = "test_cdn3"

GEO_URL = "https://geocode-maps.yandex.ru/1.x"
LANG = "RU" #TODO

app = Flask(__name__)
client = MongoClient("mongo", 27017)
db = client[DB_NAME]
cities = db["cities"]
cities.create_index({'coords': '2d'})

app.config['JSON_AS_ASCII'] = False

def get_city_info(city):

    payload = {"apikey": API_KEY, 
               "geocode": city, 
               "format": "json", 
               "results": 1, 
               "lang": "ru_Ru"}
    
    r = requests.get(GEO_URL, params=payload)
    city_coords = r.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    
    city_name = r.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name'] 
    
    return {"name": city_name, "coords": list(map(float, city_coords.split()))}


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)


@app.route("/api/v1.0/cities", methods=['GET'])
def get_cities():
    # city = request.args.get('city')
    data = cities.find({},{"_id": 0})
    # return json.loads(dumps(data))
    # return jsonify(dumps(data))
    return json.loads(dumps(data))

@app.route("/api/v1.0/cities", methods=['POST'])
def add_city():
    if not request.json or not "city" in request.json:
        abort(400)
    # city = request.args.get('city')
    # data = {"city": city, "x": len(city), "y": len(city)+1}
    city = request.json['city']

    city_info = get_city_info(city)

    data = {"city": city, "answer_city_name": city_info['name'], "coords": city_info['coords']} #loc
    print(data,type(data))
    cities.insert_one(data)
    print(data, type(data))
    return jsonify({"city": "OK"}), 201

@app.route("/api/v1.0/cities/<string:city_name>", methods=['GET'])
def get_city(city_name: str):
    # city = request.args.get('city')
    city = cities.find_one({"city": city_name}, {"_id": 0})
    if city is None:
        abort(404)
    return json.loads(dumps(city))

@app.route("/api/v1.0/cities/<string:city_name>/nearest", methods=['GET'])
def get_nearest_cities(city_name: str):
    n = request.args.get('n')
    
    # print(n, type(n))
    n = 2 if n is None else int(n)
    city = cities.find_one({"city": city_name}, {"_id": 0})
    if city is None:
        abort(404)
    loc = city['coords']

    near_cities = cities.find({"coords": {"$near": loc}}).skip(1).limit(n)
    if not near_cities:
        abort(404)
    return json.loads(dumps(near_cities))

@app.route("/api/v1.0/cities/<string:city_name>", methods=['PUT'])
def put_city(city_name: str):
    # if not request.json or not "city" in request.json:
        # abort(400)

    city = cities.find_one({"city": city_name})
    if city is None:
        abort(404)

    # city = request.args.get('city')
    # data = {"city": city, "x": len(city), "y": len(city)+1}
    # data = {"city": city, "coords": get_coords(city)} #loc
    
    cities.update_one({"city": city_name}, {"$set": dict(request.json)})

    return jsonify({"city": "OK"}), 201

@app.route("/api/v1.0/cities/<string:city>", methods=['DELETE'])
def delete_city(city: str):
    abort(405) 

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")