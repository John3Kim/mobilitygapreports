''' 
File: DatabaseAdapter.py 
Description: This is a class that allow for the direct interaction with the 
database for the purposes of putting mobility data in there.
'''

import psycopg2 
import pandas as pd
from sqlalchemy import create_engine, text


class DatabaseAdapter: 

    def __init__(self,user:str,password:str,host:str,port:str,database:str): 
        try: 
            self.connection = psycopg2.connect(user=user,
                                               password=password,
                                               host=host,
                                               port=int(port),
                                               database=database)
            self.engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
        
        except: 
            print("Issue in connecting to database...")
            self.connection.close()    
    
    def db_latest_date(self) -> pd.DataFrame:
        latest_date_query = text("SELECT MAX(date) FROM canada_duplicate")
        latest_date = pd.read_sql(latest_date_query, self.engine)
        
        return latest_date.iloc[0,]
        

    def append_data(self, data_to_append:pd.DataFrame, target_table: str, latest_date_db:str, latest_date_csv: str) -> None:
        # get the latest date from the database 
        # get the latest date from the dataframe 
        # equality comparison
        try:
            
            if latest_date_csv != latest_date_db:
                data_to_append.to_sql(target_table, con=self.engine, if_exists="append", index=False)

        except psycopg2.errors.UndefinedTable as e: 
            print(f"Undefined table: {e}")

        finally:
            self.connection.close()
    