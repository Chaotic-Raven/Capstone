import json
from bson import json_util
from bson.json_util import loads
from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

def docFind50Day(low, high):
  search = {"50-Day Simple Moving Average" : { "$gt" :  low, "$lt" : high}}
  result = collection.find(search)
  #result = collection.find_one(query)
  result = result.count()
  
  return result

def docFindIndustry(f):
  field = {"Ticker":1, "_id":0}
  search = {"Industry" : f}
  
  result = list(collection.find(search, field))
  #result = result.count()
  
  return result

def main():
  
  #Arbitrary Test Inputs
  l = 0.03
  h = 0.04

  field = "Medical Laboratories & Research"
  
  print(docFind50Day(l, h))
  docFindIndustryOutput = docFindIndustry(field)
  
  for x in docFindIndustryOutput:
    print(x)
  
  
main()