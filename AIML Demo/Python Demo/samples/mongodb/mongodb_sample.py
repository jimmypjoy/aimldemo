import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["test_mongodb"]
print(myclient.list_database_names())
if "mydatabase" in myclient.list_database_names():
  print("The database exists.")

mycollection = mydb["customers"]
print(mydb.list_collection_names())
mydict = { "name": "JJ", "address": "Crocus" }
x = mycollection.insert_one(mydict)
print(x.inserted_id)

#query
myquery = { "address": "Crocus" }
mydoc = mycollection.find(myquery)
for x in mydoc:
  print(x)