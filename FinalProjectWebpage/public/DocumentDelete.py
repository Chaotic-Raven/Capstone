import json
from bson import json_util
from bson.json_util import loads
from pymongo import MongoClient

def deleteDocument(ticker, collection):
  query = {"Ticker" : ticker} 
  result = collection.delete_one(query)
  
  if result.deleted_count is 0:
    return False
  else:
    return True

