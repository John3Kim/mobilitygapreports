''' 
File: run.py 
Description: The main class, where we run the code.
'''

from DatabaseAdapter import DatabaseAdapter 
from GoogleCovidMobility import GoogleCovidMobility
from decouple import config


if __name__ == "__main__": 
    user = config("DB_USER")
    password = config("DB_PASSWORD")
    host = config("DB_HOST")
    port = config("DB_PORT")
    database = config("DB_NAME")

    db_adapter = DatabaseAdapter(user,password,host,port,database)
    latest_date_db = db_adapter.db_latest_date()
    latest_date_db = latest_date_db.values[0]

    mobility_data = GoogleCovidMobility()
    mobility_data.get_canada_mobility_report()
    latest_data_csv = mobility_data.get_data_csv(latest_date_db)
    latest_date_csv = mobility_data.latest_date_csv("date", latest_data_csv)
   
    db_adapter.append_data("canada_duplicate", latest_data_csv, latest_date_db, latest_date_csv)