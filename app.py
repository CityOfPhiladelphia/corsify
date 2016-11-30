from json.decoder import JSONDecodeError
from flask import Flask, abort, jsonify as flask_jsonify, request
from flask_cors import CORS
from werkzeug.routing import BaseConverter
import requests
from config import CONFIG

app = Flask(__name__)
CORS(app, origins=CONFIG['origins'])

class RegexConverter(BaseConverter):
    '''Custom handler for regex-based routing'''
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
app.url_map.converters['regex'] = RegexConverter

@app.route('/<regex(".*"):url>')
def get(url):
    r = requests.get(url, params=request.args)

    # force json, bc it seems defensive-ish and it's our only use case right now
    try:
        json = r.json()
    except JSONDecodeError:
        abort(400)

    return flask_jsonify(json)
