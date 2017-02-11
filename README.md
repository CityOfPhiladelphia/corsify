# corsify

Proxies and adds CORS headers to things that don't have them. This is meant to allow client-side web apps to access legacy web services. Don't use for evil stuff.

## Installation

    git clone https://github.com/CityOfPhiladelphia/corsify
    cd corsify
    python -m venv venv
    source ./venv/bin/activate
    pip install -r requirements.txt

## Deployment

Corsify expects two environment variables:

* `CORSIFY_HOSTS`: comma-separated upstream hosts
* `CORSIFY_ORIGINS`: comma-separated downstream origins

You can use `*` as a wildcard, though it's probably not a good idea.

To start the development server:

    cd <path to repo>
    set FLASK_APP=corsify.py
    set CORSIFY_HOSTS=host1.com,host2.com
    set CORSIFY_ORIGINS=origin1.com,origin2.com
    flask run

See [here](http://flask.pocoo.org/docs/0.11/deploying/) for production deployment options.

## Usage

    curl http://<host>:5000/http://api.phila.gov/ais/v1/addresses/1234+MARKET+ST
