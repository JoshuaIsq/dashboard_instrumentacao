import pandas as pd
import numpy as np
import scipy as sp
from scipy import signal

class LogImporter():

    INDEX_COLUMN_TIME = [0, 1, 2, 3, 4, 5]
    INDEX_DATETIME = ["day", "month", "year", "hour", "minute", "second"] 

    def __init__(self):
        self.df_timestamp = []
        self.df_sensors = pd.DataFrame()
        self.df_full = []
        self.df_joined_files = []
        

    def import_file(self, file):
        if file.endswith('.txt'):
            print('Iniciando leitura')
            txt_file = pd.read_csv(file, sep='\t', header=None, engine='python', on_bad_lines='skip')
            print(f"Lendo arquivo {file}, colunas encontradas: {(txt_file.shape[1])}")
            self.df_sensors = txt_file
            
    
    def create_timestamp(self):
        column_times = LogImporter.INDEX_COLUMN_TIME
        for col in column_times:
            self.df_sensors[col] = pd.to_numeric(self.df_sensors[col], errors='coerce')
        self.df_sensors[column_times] =  self.df_sensors[column_times].astype(int)
        self.df_timestamp = self.df_sensors[column_times]
        self.df_timestamp.columns = LogImporter.INDEX_DATETIME
        timestamp = pd.to_datetime(self.df_timestamp) 
        df_temp = pd.DataFrame({'timestamp': timestamp}) #O que é indice temporal
        sensors = self.df_sensors.iloc[:, 6:] #O que são sensores
        self.df_full = pd.concat([df_temp, sensors], axis=1) #Os juntando como 1 coluna de timestamp e o resto de sensor
        self.df_joined_files.append(self.df_full) #Os colocando em uma lista que juntará todos arquivos
        print(f"Total de {len(self.df_joined_files)} arquivos adicionados") 

        
    def join_files(self):
        if len(self.df_joined_files) > 0:
            df_concatenaded = pd.concat(self.df_joined_files, axis=0, ignore_index=True)
            df_concatenaded = df_concatenaded.sort_values(by='timestamp').reset_index(drop=True)
            time_axe = (df_concatenaded['timestamp'].astype('int64') / 10**9).tolist() #FINAL DE TIMESTAMP MANIPULAVEL, NECESSÁRIO PROTEGER
            sensor_axe = df_concatenaded.drop(columns=['timestamp']) #FINAL DE SENSORES NECESSÁRIO PROTEGER
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
        
    



