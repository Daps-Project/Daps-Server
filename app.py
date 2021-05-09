import xmltodict
from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/data', methods=['GET', 'POST'])
def jsonify_XML():
    with open("Questions.xml") as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    return jsonify(data_dict)

if __name__ == '__main__':
    app.run()
