import pandas as pd
import numpy as np
import scipy as sp
from scipy import signal

class LogImporter():

    INDEX_COLUMN_TIME = [0, 1, 2, 3, 4, 5]

    def __init__(self):
        self.df_timestamp = []
        self.df_sensors = pd.DataFrame()
        self.df_full = []
        self.df_joined_files = []
        
    def import_file(self, file):
        if file.endswith('.txt'):
            txt_file = pd.read_csv(file, sep='\t', header=None, engine='python', on_bad_lines='skip')
            print(f"Lendo arquivo {file}, colunas encontradas: {(txt_file.shape[1])}")
            self.df_sensors = txt_file
            
    
    def create_timestamp(self):
        column_times = LogImporter.INDEX_COLUMN_TIME
        for col in column_times:
            self.df_sensors[col] = pd.to_numeric(self.df_sensors[col], errors='coerce')
        self.df_sensors[column_times] =  self.df_sensors[column_times].astype(int)
        self.df_timestamp = self.df_sensors[column_times]
        self.df_timestamp.columns = ["day", "month", "year", "hour", "minute", "second"] 
        timestamp = pd.to_datetime(self.df_timestamp) 
        df_temp = pd.DataFrame({'timestamp': timestamp}) 
        sensors = self.df_sensors.iloc[:, 6:]
        self.df_full = pd.concat([df_temp, sensors], axis=1)
        self.df_joined_files.append(self.df_full)
        print(f"Total de {len(self.df_joined_files)} arquivos adicionados") 

        
    def join_files(self):
        if len(self.df_joined_files) > 0:
            df_concatenaded = pd.concat(self.df_joined_files, axis=0, ignore_index=True)
            df_concatenaded = df_concatenaded.sort_values(by='timestamp').reset_index(drop=True)
            time_axe = (df_concatenaded['timestamp'].astype('int64') / 10**9).tolist()
            sensor_axe = df_concatenaded.drop(columns=['timestamp'])
            print(f"Sucesso! Todos os {len(self.df_joined_files)} arquivos foram unidos.")
            print(f"Quantidade de pontos: {df_concatenaded.shape}")
            return time_axe, sensor_axe
        else:
            print("A lista está vazia. Importe e processe arquivos antes de unir.")
            return None
        
class Math():
    def __init__(self, time_data, sensor_data):
        self.time_axe = np.array(time_data)
        self.sensor_axe = sensor_data
    
    def adjust_offset(self, n_linhas):
        self.sensor_axe = self.sensor_axe.copy()
        adjust = self.sensor_axe.iloc[:int(n_linhas)].mean()
        self.sensor_axe = self.sensor_axe - adjust

        return self.sensor_axe
        
    



