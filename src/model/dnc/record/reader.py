import os
import re
import pandas as pd
import MrQLib as Lib
from typing import List
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

class RecordReader:
    num_latest_files: int = 10

    @staticmethod
    def readToolChange(tool_number: str) -> datetime:
        if not tool_number or not RecordReader.check_tool_number_format(tool_number): 
            print("Tool number is empty or has an incorrect format.")
            return None

        dirpath = os.path.join(os.getcwd(), os.getenv("EVENT_PATH"), r"ToolChange")
        if not os.path.isdir(dirpath): 
            print("Directory[{0}] does not exist in file system.".format(dirpath))
            return None

        files = RecordReader._get_latest_files(dirpath, RecordReader.num_latest_files)
        for filepath in files:
            df = pd.read_csv(filepath)
            # Create a boolean mask where the string is found in the specified columns
            mask = df[['toolOut', 'toolIn']].apply(lambda col: col.astype(str).str.contains(tool_number[1:], case=False)).any(axis=1)
            if df[mask].empty: return None
            record = df[mask].sort_values(by='timeStamp', ascending=False).iloc[0]
            return datetime.strptime(record['timeStamp'], "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def readErrorMessage(time: datetime) -> str:
        # Check if time parameter is empty or None
        if not time: 
            print("Time parameter is empty or None.")
            return ""
        # Construct the directory path
        dirpath = os.path.join(os.getcwd(), os.getenv("EVENT_PATH"), r"ErrorMessage")
        if not os.path.isdir(dirpath): 
            print("Directory[{0}] does not exist in file system.".format(dirpath))
            return None
        # Define paths for three consecutive days' error message files
        files = [
            os.path.join(dirpath, (time-timedelta(days=1)).strftime("%Y-%m-%d")+".csv"),
            os.path.join(dirpath, (time).strftime("%Y-%m-%d")+".csv"),
            os.path.join(dirpath, (time+timedelta(days=1)).strftime("%Y-%m-%d")+".csv")
        ]
        # Read CSV files into pandas DataFrames
        dfs = []
        for filepath in files:
            if not os.path.isfile(filepath): continue
            dfs.append(pd.read_csv(filepath))
        
        if not dfs: 
            time_str = time.strftime("%Y-%m-%d")
            return "There is no warning record for the day before and after {0}".format(time_str)
        # Concatenate DataFrames
        df_all = pd.concat(dfs, ignore_index=True)
        df_all['errorArrivedTime'] = pd.to_datetime(df_all['errorArrivedTime'])
        # Calculate the absolute difference between errorArrivedTime and given time
        df_all['diff'] = abs(df_all['errorArrivedTime'] - time)
        # Find the index of the row with the minimum timestamp difference
        nearest_index = df_all['diff'].idxmin()
        nearest_row = df_all.loc[nearest_index].copy()
        display_row = nearest_row[['errorText', 'errorArrivedTime']]
        return display_row.to_string()

    @staticmethod
    def readProgramExecution(pg: Lib.Program) -> int:
        pass

    @staticmethod
    def _get_latest_files(dirpath: str, num_files=10) -> List[str]:
        files = os.listdir(dirpath)
        # Filter out non-file items
        files = list(filter(lambda f: os.path.isfile(os.path.join(dirpath, f)), files))
        # Sort files by date (assuming file names are dates)
        files = sorted(files, reverse=True)
        # Get the latest num_files files
        latest_files = files[:num_files]
        file_paths = list(map(lambda f: os.path.join(dirpath, f), latest_files))
        return file_paths
    
    @staticmethod
    def check_tool_number_format(input_string):
        pattern = r'^T\d+$'
        return bool(re.match(pattern, input_string))