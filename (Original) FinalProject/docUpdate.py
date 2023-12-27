import json
from bson import json_util
from bson.json_util import loads
from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

def docUpdate(query, update):
  update = {"$set" : update}
  collection.update_one(query, update)
  result = collection.find_one(query)
  
  return result

def main():
  
  #Arbitrary Test Inputs
  q = {"Ticker" : "ABC"}
  u = {"Volume" : 438825}
  print("ORIGINAL DOCUMENT\n\n\n")
  print(collection.find_one(q))
  print("\n\n\nUPDATED DOCUMENT")
  
  print(docUpdate(q, u))
  
  
main()