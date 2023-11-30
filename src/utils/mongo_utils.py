

import pymongo
import json
from pymongo import MongoClient, InsertOne

"""
Defined in mongodb docker-compose.yml
"""
user = 'root'
password = 'example'
filename = 'C:/D_drive/UCSD/Quarters/Q1/DSC202/mongodb_vol/restaurants.json'
db_name = 'dsc202'
collection_name = 'restaurants'
host='localhost'
port = 27017

class Mongo_Connector():

    def __init__(self, creds) -> None:
        self.creds = creds
        self.client = self.createConnection()


    def createConnection(self):
        client = pymongo.MongoClient(f"mongodb://{self.creds['user']}:{self.creds['password']}@{self.creds['host']}:{self.creds['port']}/")
        return client
    

    def json2Mongo(self, collection_name, input_json):
        db = self.client[self.creds['db']]
        collection = db[collection_name]
        requesting = []
        # myDict = json.loads(input_json)
        requesting.append(InsertOne(input_json))
        result = collection.bulk_write(requesting)
        return result


    def df2Mongo(self, collection_name, df):
        db = self.client[self.creds['db']]
        collection = db[collection_name]
        requesting = []

        for i,row in df.iterrows():
            r_json = json.loads(row.to_json())
            requesting.append(InsertOne(r_json))

        result = collection.bulk_write(requesting)
        return result
    

    def Mongo2json(self, collection_name, query):
        mydb = self.client[self.creds['db']]
        mycol = mydb[collection_name]
        mydoc = mycol.aggregate(query)
        returned_lst = []
        for x in mydoc:
            returned_lst.append(x)
        
        return returned_lst


    def closeConnection(self):
        self.client.close()