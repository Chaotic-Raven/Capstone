import json
from bson import json_util
from bson.json_util import loads
from pymongo import MongoClient

def findOneStock(ticker, collection):
  search = {"Ticker" : ticker}
  output = collection.find_one(search)

  return output

#def docFind50Day(low, high, collection):
##  search = {"50-Day Simple Moving Average" : { "$gt" :  low, "$lt" : high}}
 # result = collection.find(search).count()
  
 # return result

def docFindIndustry(industry, collection):
  field = {"Ticker": 1, "_id": 0}
  search = {"Industry" : industry}
  
  result = list(collection.find(search, field))
  
  return result
