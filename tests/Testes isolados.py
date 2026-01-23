import pandas as pd
import numpy as np
import io

class BaseParser:
    def parse(self, filepath):
        raise NotImplementedError
    
class Aeron(BaseParser):
    def parse(self, filepath):
        df = pd.read_csv(filepath, sep=None, header=None, engine='python', on_bad_lines='skip')
        cols_time = [0, 1, 2, 3, 4, 5] 
        for col in cols_time:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        temp_time = df.iloc[:, :6].copy()
        temp_time.columns = ["day", "month", "year", "hour", "minute", "second"]
        timestamp = pd.to_datetime(temp_time)
        sensors = df.iloc[:, 6:]
        sensors = sensors.apply(pd.to_numeric, errors='coerce').fillna(0.0)
        
        return pd.concat([timestamp, sensors], axis=1)
    
class ESP32_isq(BaseParser):
    def parse(self, filepath):
        df = pd.read_csv(filepath, sep=';', header=None, engine='python', on_bad_lines='skip')
        
        df = df.dropna(axis=1, how='all')
    
        time_col = df.iloc[:, 0]
        sensors = df.iloc[:, 1:]
        
        clean_df = pd.concat([time_col, sensors], axis=1)
        clean_df.columns = ['timestamp'] + [f'sensor_{i}' for i in range(sensors.shape[1])]
        
        return clean_df