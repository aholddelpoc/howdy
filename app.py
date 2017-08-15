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
	if req.get("result").get("action") == "yahooWeatherForecast":
		baseurl = "https://query.yahooapis.com/v1/public/yql?"
		yql_query = makeYqlQuery(req)
		if yql_query is None:
			return {}
		yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
		result = urlopen(yql_url).read()
		data = json.loads(result)
		res = makeWebhookResult(data)
	elif req.get("result").get("action") == "getAtomicNumber":
		data = req
		res = makeWebhookResultForGetAtomicNumber(data)
	elif req.get("result").get("action") == "getChemicalSymbol":
		data = req
		res = makeWebhookResultForGetChemicalSymbol(data)
	elif req.get("result").get("action") == "showRestoForLocation":
		baseurl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
		req_query = makeYqlNewQuery(req)
		req_query_final = baseurl + req_query
		print(req_query_final)
		result = urlopen(req_query_final).read()
		data = json.loads(result)
		res = makeWebhookResult(data)		
	else:
		return {}
	return res

def makeWebhookResultForGetChemicalSymbol(data):
	element = data.get("result").get("parameters").get("elementname")
	chemicalSymbol = 'Unknown'
	if element == 'Carbon':
		chemicalSymbol = 'C'
	elif element == 'Hydrogen':
		chemicalSymbol = 'H'
	elif element == 'Nitrogen':
		chemicalSymbol = 'N'
	elif element == 'Oxygen':
		chemicalSymbol = 'O'
	speech = 'The Chemical symbol of '+element+' is '+chemicalSymbol
	
	return {
		"speech": speech,
		"displayText": speech,
		"source": "webhookdata"
	}
	

def makeWebhookResultForGetAtomicNumber(data):
	element = data.get("result").get("parameters").get("elementname")
	atomicNumber = 'Unknown'
	if element == 'Carbon':
		atomicNumber = '6'
	elif element == 'Hydrogen':
		atomicNumber = '1'
	elif element == 'Nitrogen':
		atomicNumber = '7'
	elif element == 'Oxygen':
		atomicNumber = '8'
	speech = 'The atomic number of '+element+' is '+atomicNumber
	
	return {
		"speech": speech,
		"displayText": speech,
		"source": "webhookdata"
	}
	

def makeYqlQuery(req):
	result = req.get("result")
	parameters = result.get("parameters")
	city = parameters.get("geo-city")
	if city is None:
		return None

	return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"
	
def makeYqlNewQuery(req):
	result = req.get("result")
	parameters = result.get("parameters")
	location = parameters.get("location")
	if location is None:
		return {
			"speech": "location should be present in parameters",
			"source": "apiai-resto-webhook"
		}
	radius = "2000"
	apiKey = "AIzaSyB456eFn6t3O2SuLmOSxxEfc3qIo5V1rsw"
	forType = "restaurant"
	url = "location=" + location
	url = url + "&radius=" + radius
	url = url + "&type=" + forType
	url = url + "&key=" + apiKey
	url = url + "&keywork=food"
	return url


def makeWebhookResult(data):
	results = data.get('results')

	if len(results) > 0:
		speech = "We found few restaurant near by you"
	else:
		speech = "Sorry, there is no good restaurant near by you"

	return {
		"speech": speech,
		"data": results,
		"source": ""source": "apiai-weather-webhook-sample""
	}


if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	print("Starting app on port %d" % port)

	app.run(debug=False, port=port, host='0.0.0.0')
