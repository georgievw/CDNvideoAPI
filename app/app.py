from flask import Flask, request
from pymongo import MongoClient
from bson.json_util import dumps 

app = Flask(__name__)
DB_NAME = "test_cdn"
client = MongoClient("mongo", 27017)
db = client[DB_NAME]
cities = db["cities"]

@app.route("/", methods=['GET'])
def get_city():
    city = request.args.get('city')
    data = cities.find({"city": city}, {"_id": 0})
    return dumps(data)

@app.route("/add", methods=['GET'])
def add_city():
    city = request.args.get('city')
    data = {"city": city, "x": len(city), "y": len(city)+1}
    cities.insert_one(data)
    return "OK"

# @app.route("/", methods=['POST'])
# def post_city():
#     city_name = request.args.get
#     return "CITY"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")