''' 
File: GoogleCovidMobility.py 
Description: This is a class used to retrieve Google Mobility data and manipulate it

'''

from pathlib import Path
import io
import requests
import shutil
import zipfile
import pandas as pd


class GoogleCovidMobility: 

    def __init__(self):
        self.GOOGLE_MOBILITY_ZIP = 'https://www.gstatic.com/covid19/mobility/Region_Mobility_Report_CSVs.zip'


    def get_canada_mobility_report(self) -> None:
        ''' 
        Retrieves the Canada mobility data set from Google.
        '''

        try:
            get_moblity_zip = requests.get(self.GOOGLE_MOBILITY_ZIP)
            zip_file = zipfile.ZipFile(io.BytesIO(get_moblity_zip.content))
            
            Path("temp/").mkdir(parents=True, exist_ok=True)
            zip_file.extractall(Path.cwd() / "temp")
            
            Path("temp/2020_CA_Region_Mobility_Report.csv").rename("./2020_CA_Region_Mobility_Report.csv")

            shutil.rmtree("temp/")
        except:
            print("There was a problem with retrieving the zip file...")
    

    def get_data_csv(self, latest_date_db:str) -> pd.DataFrame: 
        ''' 
        Retrieves only the latest dates in the database
        
        Arguments: 
            latest_date_db: str -> A date string that is formatted as YYYY-MM-DD

        Returns: 
            A pandas dataframe containing the latest data in the csv.
        '''
        try:
            mobility_data = pd.read_csv("2020_CA_Region_Mobility_Report.csv")

            latest_date_csv = mobility_data["date"].max()
            mobility_date_range_mask = (mobility_data["date"] > latest_date_db) & (mobility_data["date"] <= latest_date_csv)
       
        except: 
            print("File issues here")

        return mobility_data.loc[mobility_date_range_mask]
    
    def latest_date_csv(self, date_column_name:str, data: pd.DataFrame) -> str: 
        ''' 
        Gets the latest date in the a csv. 

        Argument: 
            date_column_name: str -> Date column that you want filter for
            data: pd.DataFrame -> the data that you want to get the latest date for
        Returns: 
            A string containing the date in format YYYY-MM-DD
        '''
        return data[date_column_name].max()