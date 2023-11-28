import psycopg2
import pandas as pd
import psycopg2.extras as extras
from datetime import datetime
import json
from .pandas_utils import *
import math

class PostgreSQL_Connector:
    def __init__(self, creds):
        self.creds = creds
        self.connection, self.cursor = self.createConnection()


    def createConnection(self):
        pg_conn = psycopg2.connect(
            dbname=self.creds['db'],
            user=self.creds['user'],
            password=self.creds['password'],
            host=self.creds['host'],
            port=self.creds['port']
        )
        pg_conn.autocommit = True
        pg_cursor = pg_conn.cursor()
        return pg_conn, pg_cursor
    

    def insertInPostgres(self, df, table):   
        # If datatype is object, then replace NaN with None
        df = df.astype(object).where(pd.notnull(df), None)

        tuples = [tuple(x) for x in df.to_numpy()] 
    
        cols = list(df.columns)
        cols = [x.replace(' ','_') for x in cols] # Replacing space with _
        cols = ','.join(cols) 
        # SQL query to execute 
        query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols) 
        # try: 
        extras.execute_values(self.cursor, query, tuples) 
        self.connection.commit() 
        # except (Exception, psycopg2.DatabaseError) as error: 
        #     print("Error: %s" % error) 
        #     self.connection.rollback() 
        #     self.cursor.close() 
        #     return 1
        print("the dataframe is inserted") 
        
    
    def getTableStructure(self, dst_table_name):
        """
            Input: SQL table name
            Returns: Empty Pandas dataframe with the same structure as SQL Table 
        """
        self.cursor.execute(f"select * from {dst_table_name} limit 1;")
        
        # Getting 1 row of db table and converting to dataframe
        db_list = self.cursor.fetchall()
        colnames = [desc[0] for desc in self.cursor.description]
        db_table = pd.DataFrame(db_list, columns=colnames)

        db_table.drop(db_table.index, inplace=True)
        return db_table


    def runQuery(self, statement):
        # This didn't return the newly inserted rows in table
        #db_table = pd.read_sql(statement, self.connection)
        self.cursor.execute(statement)
        db_list = self.cursor.fetchall()
        colnames = [desc[0] for desc in self.cursor.description]
        db_table = pd.DataFrame(db_list, columns=colnames)
        return db_table
    

    def runSQL_noReturn(self, statement):
        self.cursor.execute(statement)

        
    def pandas2SQL(self, input_df, dst_table_name, batch_size=0):
        print(f"Inserting in {dst_table_name} ...", end=' ')
        # Get Empty dataframe with the same structure as SQL table
        db_table = self.getTableStructure(dst_table_name=dst_table_name)
        # Insert values from with common column names or for which
        # mapping in config_json["mapping_dict"] is indicated
        db_table = insertCommonColumns(src_df=input_df, dest_df=db_table)
        
        if db_table.shape[0]>0:
            # Insert data in MySQL table
            self.insertInPostgres(db_table, dst_table_name)
            return "SUCCESS"
        else:
            print(f"FAILED: Nothing inserted in {dst_table_name}")
            return "FAILED"