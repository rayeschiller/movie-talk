#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import datetime
import logging
import inspect

local_vars ={}

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
    if req.get("result").get("action") != "movieReleaseDate":
        return {}
      
#   search url
#    baseurl = "https://api.themoviedb.org/3/search/movie?api_key=9fe2fdf8fcbeeb11ecec17e5e4f0276a&query=Jack+Reacher"
#   movie database url    
    baseurl="https://api.themoviedb.org/3/movie/550?api_key=9fe2fdf8fcbeeb11ecec17e5e4f0276a"
    #   yql_query = makeYqlQuery(req)
    #   if yql_query is None:
    #       return {}
    #   yql_url = baseurl + yql_query
    #   print(yql_url)
    print(baseurl)   
    result = urlopen(baseurl).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    title = parameters.get("title")
#    title = "anastasia"
    if title is None:
        return None
    return title

"""
    notes: For some reason, release_date, title, and tagline fields are pulled successfully
    but popularity, budget, revenue are not.
"""
def makeWebhookResult(data):
#   This section works
#    date = data.get('release_date')
#    if date is None:
#        return {}
#    date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')
    revenue = str(data.get('revenue'))

#    movieID = data['results'][0]['id']
    speech = "The movie " + str(revenue)
    print("Response:")
    print(speech)
    
    return {
       "speech": speech,
       "displayText": speech,
       "data": ["revenue", data.get('revenue'), "budget", data.get('budget'), "popularity", data.get('popularity')],
       "contextOut": [],
       "source": "apiai-movie-db"
    }


if __name__ == '__main__':
   
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
