from urllib.parse import urlparse
from json.decoder import JSONDecodeError
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.routing import BaseConverter
import requests
from config import CONFIG

app = Flask(__name__)
CORS(app, origins=CONFIG['origins'])

ALLOWED_HOSTS = CONFIG['allowed_hosts']
should_limit_hosts = '*' not in ALLOWED_HOSTS
# TODO use one of these patterns https://mathiasbynens.be/demo/url-regex
URL_PAT = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

class RegexConverter(BaseConverter):
    '''Custom handler for regex-based routing'''
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
app.url_map.converters['regex'] = RegexConverter

class InvalidUsage(Exception):
    '''Error handler that accepts a message and status code (defaults to 400)'''
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {key: getattr(self, key) for key in ['message', 'status_code']}

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    return response

@app.route('/<regex("{}"):url>'.format(URL_PAT))
def get(url):
    print('url: {}'.format(url))
    # parse url and check a few things
    parsed = urlparse(url)
    if len(parsed.scheme) == 0:
        raise InvalidUsage('No scheme in URL (e.g. http, https)')
    if should_limit_hosts and parsed.netloc not in ALLOWED_HOSTS:
        raise InvalidUsage('Host `{}` not allowed'.format(parsed.netloc))

    r = requests.get(url, params=request.args)

    # force json, bc it seems defensive-ish and it's our only use case right now
    try:
        json = r.json()
    except JSONDecodeError:
        raise InvalidUsage('Not a valid JSON response')

    return jsonify(json)
