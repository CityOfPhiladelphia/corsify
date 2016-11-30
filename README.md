# corsify

Proxies and adds CORS headers to City APIs that do not currently have them. Limited to a few internal hosts and restricted by origin (see `config.py`).

## Installation

This is for Windows, but should work in other environments with a few modifications.

    git clone https://github.com/CityOfPhiladelphia/corsify
    cd corsify
    python -m venv venv
    cd venv\Scripts
    activate
    cd ..\..
    pip install -r requirements.txt

## Deployment

To start the development server:

    cd <path to repo>
    set FLASK_APP=corsify.py
    flask run 8080

See [here](http://flask.pocoo.org/docs/0.11/deploying/) for production deployment options.

## Usage

    curl http://<host>:8080/http://api.phila.gov/ais/v1/addresses/1234+MARKET+ST
