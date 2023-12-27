import json
from bson import json_util
from bson.json_util import loads
from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

def docDelete(query):
  query = {"Ticker" : query} 
  result = collection.delete_one(query)
  
  if result.deleted_count is 0:
    return False
  else:
    return True

def main():
  
  #Arbitrary Test Inputs
  q = {"Ticker" : "ABC"}
  
  print("ORIGINAL DOCUMENT\n\n\n")
  print(collection.find_one(q))
  print("\n\n\nDELETE CONFIRMATION")
  
  print(docDelete("ABC"))
  
  
main()