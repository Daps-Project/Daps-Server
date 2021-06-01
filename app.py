import xmltodict
from flask import Flask, request
from flask import jsonify
import requests, json
from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/data', methods=['GET', 'POST'])
def jsonify_XML():
    with open("Questions.xml") as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    return jsonify(data_dict)



@app.route("/survey_data", methods=["GET", "POST"])
@cache.cached(timeout=120)
def googlePlaces():
    if request.method == 'POST':
        responses = request.json
        query = (responses['responses'])
        #         // https://developers.google.com/maps/documentation/places/android-sdk/start
        api_key = 'AIzaSyDrzDcMBvxz0DSFIhm0vrzRDAaZi1VOOjs'
        query = "%20".join(query)
        # url variable store url
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        apiRequest = requests.get(url + 'input=' + query + '&inputtype=textquery&fields=place_id' +
                         '&key=' + api_key)
        requestJSON = apiRequest.json()

        resultDicts = requestJSON['results']
        place_id = []

        if resultDicts:
            for i in range(len(resultDicts)):
                print(resultDicts[i])
                if resultDicts[i]['business_status'] == "OPERATIONAL":
                    place_id.append(resultDicts[i]['place_id'])
            print(resultDicts)
            print(jsonify(place_id))

            return jsonify(place_id)
        else:
            return "No results"

    if request.method == 'GET':
        return cache


if __name__ == '__main__':
    app.run()
