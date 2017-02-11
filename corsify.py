import os
import warnings
from urllib.parse import urlparse
from json.decoder import JSONDecodeError
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from util import RegexConverter, InvalidUsage


# config
ORIGINS = os.environ.get('CORSIFY_ORIGINS')
HOSTS = os.environ.get('CORSIFY_HOSTS')
if not ORIGINS:
    raise ValueError('Environment variables CORSIFY_ORIGINS not set')
if not HOSTS:
    raise ValueError('Environment variables CORSIFY_HOSTS not set')
ORIGINS = ORIGINS.split(',')
HOSTS = HOSTS.split(',')
SHOULD_LIMIT_HOSTS = '*' not in HOSTS
# TODO use one of these patterns https://mathiasbynens.be/demo/url-regex
# the following doesn't seem to be catching some API URLs
# URL_PAT = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
URL_PAT = '.+'

# warn on permissive hosts/origins
if '*' in ORIGINS:
    warnings.warn('A wildcard was found in ORIGINS, so they will not be '
                  'filtered.')
if '*' in HOSTS:
    warnings.warn('A wildcard was found in HOSTS, so they will not be '
                  'filtered.')

# create app
app = Flask(__name__)

# add cors
CORS(app, origins=ORIGINS)

# use regex for routing
app.url_map.converters['regex'] = RegexConverter

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Generic error handler"""
    response = jsonify(error.to_dict())
    return response

@app.route('/<regex("{}"):url>'.format(URL_PAT))
def get(url):
    """Main route for adding CORS headers to things"""

    # parse url and check for issues in request
    parsed = urlparse(url)
    if len(parsed.scheme) == 0:
        raise InvalidUsage('No scheme in URL (e.g. http, https)')
    if SHOULD_LIMIT_HOSTS and parsed.netloc not in HOSTS:
        raise InvalidUsage('Host `{}` not allowed'.format(parsed.netloc))

    # get response
    resp = requests.get(url, params=request.args)
    content_type = resp.headers['Content-Type']

    return (resp.text, resp.status_code, {'Content-Type': content_type})
