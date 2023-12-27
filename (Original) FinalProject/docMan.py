import json
from bson import json_util
from bson.json_util import loads
from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection['market']
collection = db['stocks']

def main():
  i = 0
  
  with open('tesc.json', 'r') as reader:
    line = reader.readline()
    line = line.strip()
    payload = loads(line)
    
    
    result = collection.insert_one(payload)
    

    while line != '':  # The EOF char is an empty string
      i += 1
      line = reader.readline()
      if(line != ''):
        line = line.strip()
        payload = loads(line)
        result = collection.insert_one(payload)
      
      
      
      

    return i
    
    reader.close()
    
  
main()