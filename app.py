#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    baseurl = "https://api.themoviedb.org/3/movie/550?api_key=9fe2fdf8fcbeeb11ecec17e5e4f0276a"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    print(yql_url)
    result = urlopen(baseurl).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")

    if city is None:
        return None
        

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
#    query = data.get('query')
#    if query is None:
#        return {}

    date = data.get('release_date')
    if date is None:
        return {}
        
    title = data.get('title')
    if title is None:
        return {}

#    channel = result.get('channel')
#    if channel is None:
#        return {}
#
#    item = channel.get('item')
#    location = channel.get('location')
#    units = channel.get('units')
#    if (location is None) or (item is None) or (units is None):
#        return {}
#
#    condition = item.get('condition')
#    if condition is None:
#        return {}

    # print(json.dumps(item, indent=4))

#    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
#             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

    speech = "The movie " + title + " was released on " + date
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
