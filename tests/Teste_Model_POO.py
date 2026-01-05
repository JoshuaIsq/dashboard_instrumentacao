import pandas as pd
import numpy as np
import scipy as sp
from scipy import signal

class Model():

    def __init__(self):
        self.df_timestamp = []
        self.df_sensores = pd.DataFrame()
    
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
        self.df_timestamp.columns = ["day", "month", "year", "hour", "minute", "second"] #aqui temos 6 colunas
        timestamp = pd.to_datetime(self.df_timestamp) #quando transformei em coluna de tempo passou a ser 1 coluna só de timestamp
        df_temp = pd.DataFrame({'timestamp': timestamp}) 
        print(timestamp)
        print("separaaaaaaa")
        print(self.df_timestamp)
        print('separa dnvvvvv')
        print(df_temp)


arquivo = 'C:/Users/joshua.marinho/Desktop/AngloAmerica/Logs AngloAmerican/411/LOG_1.txt'
a = Model()
a.import_file(arquivo)
a.timestamp()



