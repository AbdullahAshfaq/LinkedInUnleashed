import neo4j
from neo4j import GraphDatabase
import json
import pandas as pd


class neo_connector():
    def __init__(self, creds):
        self.creds = creds
        self.driver = self.createDriver()

    def createDriver(self):
         uri = f"bolt://{self.creds['host']}:{self.creds['port']}"
         return GraphDatabase.driver(uri, auth=(self.creds['user'], self.creds['password']))
        
    def runQuery(self, query):
        with self.driver.session() as s:
            result = s.run(query)
            values = []
            for ix, record in enumerate(result):
                values.append(record.values())
            info = result.consume()  # discard
        return info, values
        

    def close(self):
        self.driver.close()

    # Common function
    def getNodeCount(self):
        info, values = self.runQuery("match (n) return count(n);")
        return info, values
    
    def deleteAllNodes(self):
        info, values = self.runQuery("match (n) detach delete n;")
        return 
    


