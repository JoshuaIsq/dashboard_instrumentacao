import pandas as pd
import numpy as np
import scipy as sp
from scipy import signal

class Model():

    def __init__(self):
        self.df_timestamp = []
        self.df_sensores = pd.DataFrame()
        self.df_full = []
        self.df_joinFiles = []
    
    def import_file(self, file):
        if file.endswith('.txt'):
            txt_file = pd.read_csv(file, sep='\t', header=None, engine='python', on_bad_lines='skip')
            print(f"Lendo arquivo {file}, colunas encontradas: {(txt_file.shape[1])}")
            self.df_sensores = txt_file
            
    
    def timestamp(self):
        column_times =[0, 1, 2, 3, 4, 5]
        for col in column_times:
            self.df_sensores[col] = pd.to_numeric(self.df_sensores[col], errors='coerce')
        self.df_sensores[column_times] =  self.df_sensores[column_times].astype(int)
        self.df_timestamp = self.df_sensores[column_times]
        self.df_timestamp.columns = ["day", "month", "year", "hour", "minute", "second"] 
        timestamp = pd.to_datetime(self.df_timestamp) 
        df_temp = pd.DataFrame({'timestamp': timestamp}) 
        sensors = self.df_sensores.iloc[:, 6:]
        self.df_full = pd.concat([df_temp, sensors], axis=1)
        self.df_joinFiles.append(self.df_full)
        print(len(self.df_joinFiles)) #ver quantos arquivos foram concatenados

        
    
    def join_files(self):
        if len(self.df_joinFiles) > 0:
            df_final = pd.concat(self.df_joinFiles, axis=0, ignore_index=True)
            df_final = df_final.sort_values(by='timestamp').reset_index(drop=True)
            time_axe = (df_final['timestamp'].astype('int64') / 10**9).tolist()
            sensor_axe = df_final.drop(columns=['timestamp'])
            print(f"Sucesso! Todos os {len(self.df_joinFiles)} arquivos foram unidos.")
            print(f"Tamanho final: {df_final.shape}")
            return time_axe, sensor_axe
        else:
            print("A lista está vazia. Importe e processe arquivos antes de unir.")
            return None
        
    



arquivo1 = 'C:/Users/joshua.marinho/Desktop/AngloAmerica/Logs AngloAmerican/411/LOG_1.txt'
arquivo2 = "C:/Users/joshua.marinho/Desktop/AngloAmerica/Logs AngloAmerican/411/LOG_2.txt"
a = Model()
a.import_file(arquivo1)
a.timestamp()
a.import_file(arquivo2)
a.timestamp()
resultado = a.join_files()
print(resultado)



