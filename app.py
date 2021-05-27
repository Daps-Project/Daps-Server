import xmltodict
from flask import Flask, request
from flask import jsonify
import requests, json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/data', methods=['GET', 'POST'])
def jsonify_XML():
    with open("Questions.xml") as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    return jsonify(data_dict)


@app.route("/survey_data", methods=["GET", "POST"])
def surveyComplete():
    responses = request.json
    query = (responses['responses'])
    googlePlaces(query)


def googlePlaces(query):
    #         // https://developers.google.com/maps/documentation/places/android-sdk/start
    api_key = 'AIzaSyDrzDcMBvxz0DSFIhm0vrzRDAaZi1VOOjs'
    query = "%20".join(query)
    # url variable store url
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    request = requests.get(url + 'input=' + query + '&inputtype=textquery&fields=place_id' +
                     '&key=' + api_key)
    requestJSON = request.json()

    resultDicts = requestJSON['results']

    for i in range(len(resultDicts)):
        print(requestJSON)
        print(resultDicts[i]['name'])

    return requestJSON



if __name__ == '__main__':
    app.run()
