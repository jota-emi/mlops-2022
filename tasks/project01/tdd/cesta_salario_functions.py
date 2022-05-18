import pandas as pd
import matplotlib.style as style
import matplotlib.pyplot as plt
import logging
from datetime import datetime

def read_data(file_path):
    """Read data from csv.

    Args:
        file_path (str): file path to read.
    
    Return:
        df_file (DataFrame): returns the file read as a dataframe.
    """
    try:
        df = pd.read_csv(file_path)
        logging.info("SUCCESS : File {} is read without erros".format(file_path))
        return df
    except FileNotFoundError:
        logging.error("ERROR : There's no such {}".format(file_path))

def apply_datetime(df, date_column, original_format):
    try:
        df_after = df.copy()
        df_after[date_column] = pd.to_datetime(df_after[date_column], format=original_format)

        df_after[date_column] = df_after[date_column].dt.date

        df_after.sort_values(date_column, inplace=True)
        df_after.reset_index(drop=True, inplace=True) 
        logging.info("SUCCESS : Datetime conversion is executed without erros")   
        return df_after
    except:
        logging.error("ERROR : Datetime conversion not work")
        return None