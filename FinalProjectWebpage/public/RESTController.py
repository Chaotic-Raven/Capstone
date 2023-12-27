#!/usr/bin/env python3
import json
from bottle import HTTPResponse, route, run, post, request, static_file, template
from pymongo import MongoClient
import bson.json_util as jUtil
import pymongo
import DocumentCreate
import DocumentRead
import DocumentUpdate
import DocumentDelete


connection = MongoClient('localhost', 27017)
db = connection['bTesting']
collection = db['testing']


@route('/')
def server_static(filepath="index.html"):
    return static_file(filepath, root='./public/')


@route('/insertDocument/<ticker>', method="POST")
def createStock(ticker):
  rawInput = request.forms.get('rawDocJSON')
  result = DocumentCreate.insertDocument(ticker, rawInput, collection)
  
  if type(result) == json.decoder.JSONDecodeError:
    return HTTPResponse(status=400, body=("Invalid POST Input - Verify JSON Formatting"))
  elif result == True:
    return HTTPResponse(status=201, body=("Stock " + ticker + " created\n"))
  elif type(result) == pymongo.errors.DuplicateKeyError:
    return HTTPResponse(status=409, body=("Stock " + ticker + " already exists.\n"))
  else:
    return HTTPResponse(status=404, body=(str(result)))

@route('/getStock/<ticker>', method="GET")
def getStock(ticker):
  #Retrieves document using ticker as index
  doc = DocumentRead.findOneStock(ticker, collection)
  output = json.loads(jUtil.dumps(doc))

  if doc is None:
    return HTTPResponse(status=400, body='Stock does not exist')
  else:
    return template('readDoc', d=output)


@route('/deleteStock/<ticker>', method="GET")
def deleteStock(ticker):
  result = DocumentDelete.deleteDocument(ticker, collection)
   
  if result:
    return HTTPResponse(status=200, body='Stock deletion completed.')
  else:
    return HTTPResponse(status=200, body='Stock deletion failed.')

@route('/updateStock/<ticker>', method="POST")
def updateStock(ticker):
  #Reads PUT data
  rawInput = request.forms.get('updateRawDocJSON')
  #Updates Document
  updateResult = DocumentUpdate.documentUpdate(ticker, rawInput, collection)
  
  if(updateResult == True):
    return HTTPResponse(status=200, body=str(ticker + ' has been updated'))
  elif(updateResult == False):
    return HTTPResponse(status=200, body=str(ticker + ' has been created.'))
  elif(updateResult == None):
    return HTTPResponse(status=400, body=str('Update request for ' + ticker + ' has failed.'))


run(host='localhost', reloader=True, port=8080, debug=True)