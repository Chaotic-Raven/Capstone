import json
import array as arr
from bson import json_util
from bson.json_util import loads
from pymongo import MongoClient


# Provided the file name, this method will read a file line by line and insert any valid MongoDB documents into the provided collection.
# Returns results (type - int array) - Index 0 is successful inserts, and Index 1 is failed inserts
def insertFromFile(fileName, collection):

  line = 'EMPTY'
  results = arr.array('i', [0,0])

  with open(fileName, 'r') as reader:
    while line != '':  # The EOF char is an empty string
      line = reader.readline()
      if(line != ''):
        line = line.strip()
        payload = loads(line)
        collection.insert_one(payload)
        results[0] += 1 
      else:
        results[1] += 1

  #Properly closes file reader    
  reader.close()
  
  return results

# Inserts a ticker document with the provided ticker, raw JSON input, and the collection to insert the document.
# Returns True if document was inserted properly
# Returns False if the document insert failed
# Returns None if a ValueError exception is thrown

def insertDocument(ticker, rawInput, collection):
  try:
    documentInput = json.loads(rawInput)
    documentInput["Ticker"] = ticker
    result = collection.insert_one(documentInput)
  except Exception as e:
    return e

  if(result.inserted_id != None):
    return True
  else:
    return False

