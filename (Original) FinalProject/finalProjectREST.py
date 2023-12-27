import json
from bson import json_util
from bson.json_util import loads
import bottle
from bottle import route, run, request, abort
from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

@route('/stocks/api/v1.0/createStock/<ticker>', method='POST')
def createStock(ticker):
  postdata = request.body.read()
  jOb = loads(postdata)
  
  jOb["Ticker"] = ticker
  
  try:
    result = collection.insert_one(jOb)
  except:
    abort(404)
  
  if result.inserted_id is None:
    return "\n\nERROR: DID NOT INSERT\n"
  else:
    return bottle.HTTPResponse(status=201, body=("Stock " + ticker + " created\n"))

@route('/stocks/api/v1.0/getStock/<ticker>', method='GET')
def getStock(ticker):
  
  search = {"Ticker" : ticker}
  #Executes find_one to attempt to find a matching document
  output = collection.find_one(search)
  #Returns output
  return "\n" + str(output) + "\n\n"

@route('/stocks/api/v1.0/updateStock/<ticker>', method="PUT")
def updateStock(ticker):
  
  try:
    rInput = request.body.readline()
    jOb = loads(rInput)
  except ValueError as ve:
    abort(404, str(ve))
    
  jOb["Ticker"] = ticker
  
  try:
    out = collection.update_one({"Ticker" : ticker}, {"$set" : jOb}, upsert=True)
  except:
    return abort(404)
  
  if(out.raw_result["updatedExisting"] == True):
    body = "Stock: " + ticker + " updated!\n"
    return bottle.HTTPResponse(status=200, body=body)
  elif(out.raw_result["updatedExisting"] == False):
    body = "Stock: " + ticker + " created!\n"
    return bottle.HTTPResponse(status=201, body=body)

@route('/stocks/api/v1.0/deleteStock/<ticker>')
def deleteStock(ticker):
  result = collection.delete_one({"Ticker" : ticker})
   
  if result.deleted_count is 0:
    return abort(404)
  else:
    return "\nDelete Successful\n\n"

#@route('/stocks/api/v1.0/stockReport', method='POST')
#def stockReport():
#  postdata = request.body.read()
#  postdata = postdata.replace("=", ":")
#  Dict = eval(postdata)
#  print(type(Dict)) 
#  return "\n\n"
  
  
  
  
  
if __name__ == '__main__':
  #app.run(debug=True)
  run(host='localhost', port=8080)  
  
  
  
