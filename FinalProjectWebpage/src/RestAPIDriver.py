import json
from bson import json_util
from bson.json_util import loads
from bottle import Bottle, HTTPResponse, route, run, request, abort
from pymongo import MongoClient
import pymongo

import DocumentCreate
import DocumentRead
import DocumentUpdate
import DocumentDelete

connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

@route('/stocks/api/v1.0/createStock/<ticker>', method='POST')
def createStock(ticker):
  rawInput = request.body.read()
  result = DocumentCreate.insertDocument(ticker, rawInput, collection)
  
  if type(result) != json.decoder.JSONDecodeError:
    return HTTPResponse(status=400, body=("Invalid POST Input - Verify JSON Formatting"))
  elif result == True:
    return HTTPResponse(status=201, body=("Stock " + ticker + " created\n"))
  elif type(result) == pymongo.errors.DuplicateKeyError:
    return HTTPResponse(status=409, body=("Stock " + ticker + " already exists.\n"))
  else:
    return HTTPResponse(status=404, body=str(type(result)))
  
  



@route('/stocks/api/v1.0/updateStock/<ticker>', method="PUT")
def updateStock(ticker):
  #Reads PUT data
  rawInput = request.body.readline()
  #Updates Document
  updateResult = DocumentUpdate.documentUpdate(ticker, rawInput, collection)
  
  if(updateResult == True):
    return HTTPResponse(status=200, body=str(ticker + ' has been updated'))
  elif(updateResult == False):
    return HTTPResponse(status=200, body=str(ticker + ' has been created.'))
  elif(updateResult == None):
    return HTTPResponse(status=400, body=str('Update request for ' + ticker + ' has failed.'))
  
  

@route('/stocks/api/v1.0/deleteStock/<ticker>')
def deleteStock(ticker):
  result = DocumentDelete.deleteDocument(ticker, collection)
   
  if result:
    return HTTPResponse(status=200, body='Stock deletion completed.')
  else:
    return HTTPResponse(status=200, body='Stock deletion failed.')
  
  
  
  
if __name__ == '__main__':
  #app.run(debug=True)
  run(host='localhost', port=8080)  
  
  
  
