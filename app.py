#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import pymongo

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


uri = 'mongodb://howdy:howdy@ds157723.mlab.com:57723/howdy'
client = pymongo.MongoClient(uri)
db = client.get_default_database()
cursor = db.product.find({'product_id': {'$gt': 1}})

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
	elif req.get("result").get("action") == "WineByTaste":
		data = req
		res = makeWebhookResultForWineByTaste(data)
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
	
def makeWebhookResultForWineByTaste(data):
	
	# mongo db result
	for doc in cursor:
		dbRes1, dbRes2 = doc['product_id'], doc['name']
		
	col = data.get("result").get("parameters").get("color")
	st_of_col = data.get("result").get("parameters").get("style_of_color")
	WineTaste = 'Unknown'
	if col == 'Pink(Rose/Blush)' and st_of_col =='Light & Bubbly':
		WineTaste = "Sparkling Wine (Rose)\
			A crisp, sparkling blush wine with flavours of red berries\
			Highly rated wines\
			Domaine Carneros Brut Rose Cuvee de la Pompadour Sparkling wine (Rose)\
			Sipping Point Picks\
			Jacob’s Creek Rose Moscato Sparkling Wine Banfi Rosa Regale Sparkling Red Brachetto\
			Value $10 & under\
			Cook’s Sparkling Wine (Rose)"
	elif col == 'Red' and st_of_col =='Dry & Fruity':
		WineTaste = '''
		{
  "id": "fc5dedd0-3fe4-4d0f-b27e-9b2263e36e48",
  "timestamp": "2017-08-24T10:41:58.209Z",
  "lang": "en",
  "result": {
    "source": "agent",
    "resolvedQuery": "Wine as a gift",
    "action": "",
    "actionIncomplete": false,
    "parameters": {},
    "contexts": [
      {
        "name": "winegift",
        "parameters": {},
        "lifespan": 5
      }
    ],
    "metadata": {
      "intentId": "5162d46a-f265-4fa7-b918-72f2bc3131c5",
      "webhookUsed": "false",
      "webhookForSlotFillingUsed": "false",
      "intentName": "sipping point - Wine gift"
    },
    "fulfillment": {
      "speech": "",
      "messages": [
        {
          "type": 4,
          "platform": "skype",
          "payload": {
            "skype": {
              "type": "message",
              "attachmentLayout": "carousel",
              "text": "Please select your food.",
              "attachments": [
                {
                  "contentType": "application/vnd.microsoft.card.hero",
                  "content": {
                    "title": "Highly rated wines",
                    "subtitle": "Piccolo Tesoro ΓÇ£PTΓÇ¥ Rose Moscato 750 mL $12.99",
                    "images": [
                      {
                        "url": "https://mydeploy.azurewebsites.net/sushi.png"
                      }
                    ],
                    "buttons": [
                      {
                        "type": "imBack",
                        "title": "View",
                        "value": "View"
                      },
                      {
                        "type": "imBack",
                        "title": "Add To Cart",
                        "value": "Add To Cart"
                      },
                      {
                        "type": "imBack",
                        "title": "Favourites",
                        "value": "Favourites"
                      },
                      {
                        "type": "imBack",
                        "title": "Wishlist",
                        "value": "Wishlist"
                      }
                    ]
                  }
                },
                {
                  "contentType": "application/vnd.microsoft.card.hero",
                  "content": {
                    "title": "Sipping Point Picks",
                    "subtitle": "Louis M. Martini Amabile Moscato 750 mL $28.00",
                    "images": [
                      {
                        "url": "https://mydeploy.azurewebsites.net/tenpura.jpg"
                      }
                    ],
                    "buttons": [
                      {
                        "type": "imBack",
                        "title": "View",
                        "value": "View"
                      },
                      {
                        "type": "imBack",
                        "title": "Add To Cart",
                        "value": "Add To Cart"
                      },
                      {
                        "type": "imBack",
                        "title": "Favourites",
                        "value": "Favourites"
                      },
                      {
                        "type": "imBack",
                        "title": "Wishlist",
                        "value": "Wishlist"
                      }
                    ]
                  }
                },
                {
                  "contentType": "application/vnd.microsoft.card.hero",
                  "content": {
                    "title": "Value $10 & under",
                    "subtitle": "Barefoot Moscato 750 mL $7.99",
                    "images": [
                      {
                        "url": "https://mydeploy.azurewebsites.net/tofu.jpg"
                      }
                    ],
                    "buttons": [
                      {
                        "type": "imBack",
                        "title": "View",
                        "value": "View"
                      },
                      {
                        "type": "imBack",
                        "title": "Add To Cart",
                        "value": "Add To Cart"
                      },
                      {
                        "type": "imBack",
                        "title": "Favourites",
                        "value": "Favourites"
                      },
                      {
                        "type": "imBack",
                        "title": "Wishlist",
                        "value": "Wishlist"
                      }
                    ]
                  }
                }
              ]
            }
          }
        },
        {
          "type": 2,
          "platform": "skype",
          "title": "View the Items in your Cart",
          "replies": [
            "View Cart"
          ]
        },
        {
          "type": 0,
          "speech": ""
        }
      ]
    },
    "score": 1.0
  },
  "alternateResult": {
    "source": "domains",
    "resolvedQuery": "Wine as a gift",
    "actionIncomplete": false,
    "metadata": {},
    "fulfillment": {},
    "score": 0.0
  },
  "status": {
    "code": 200,
    "errorType": "success"
  },
  "sessionId": "adc20fc68b624027904ef61167b67ca5"
}
		'''
	elif col == 'White' and st_of_col =='Sweet':
		WineTaste = str(dbRes1) + str(dbRes2)
	elif col == 'White' and st_of_col =='Semi-sweet':
		WineTaste = 'O'
	speech = WineTaste
	skype_message = {
  				"skype": {
    				"text": WineTaste
  				}
			}
	
	return {
		"speech": speech,
		"displayText": speech,
		"data": {"skype": skype_message},
		"source": "webhookdata",
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


def makeWebhookResult(data):
	query = data.get('query')
	if query is None:
		return {}

	result = query.get('results')
	if result is None:
		return {}

	channel = result.get('channel')
	if channel is None:
		return {}

	item = channel.get('item')
	location = channel.get('location')
	units = channel.get('units')
	if (location is None) or (item is None) or (units is None):
		return {}

	condition = item.get('condition')
	if condition is None:
		return {}

	# print(json.dumps(item, indent=4))

	speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
			 ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

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
