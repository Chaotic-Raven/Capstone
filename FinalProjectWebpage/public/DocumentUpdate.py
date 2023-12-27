import json
from bson import json_util
from bson.json_util import loads
from pymongo import MongoClient

#Given the stock ticker, the desired updates, and the collection the document resides, this method will update or create the document for ticker
def documentUpdate(ticker, rawInput, collection):
  stockQuery = {"Ticker": ticker}
  #print(rawInput)
  try:
    update = loads(rawInput)
    update["Ticker"] = ticker
    update = {"$set" : update}
  except ValueError as ve:
    print(str(ve))
    return None
  
  try:
    out = collection.update_one(stockQuery, update, upsert=True)
  except:
    #If update fails, return None
    return None

  #If updatedExisting == True, the document was updated; if false, a document was created for that ticker.
  if(out.raw_result["updatedExisting"] == True):
    return True
  else:
    return False