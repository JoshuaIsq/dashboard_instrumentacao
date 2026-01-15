import pandas as pd
import numpy as np
import scipy as sp
from scipy import signal



class LogImporter():

    INDEX_COLUMN_TIME = [0, 1, 2, 3, 4, 5]
    INDEX_DATETIME = ["day", "month", "year", "hour", "minute", "second"] 

    def __init__(self):
        self.time_axe = []
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
        self.time_axe = self.df_sensors[column_times]
        self.time_axe.columns = LogImporter.INDEX_DATETIME
        timestamp = pd.to_datetime(self.time_axe) 
        df_temp = pd.DataFrame({'timestamp': timestamp}) #O que é indice temporal
        sensors = self.df_sensors.iloc[:, 6:] #O que são sensores
        for col in sensors.columns:
            sensors[col] = pd.to_numeric(sensors[col], errors='coerce')
        sensors = sensors.fillna(0.0)
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

    def rate(self):
        if len(self.time_axe) > 1:
            total_time = self.time_axe[-1] - self.time_axe[0]
            if total_time > 0:
                rate = len(self.time_axe) / total_time
            else:
                rate = 1
        else:
            rate = 1
        return rate

    def adjust_offset(self, n_linhas):
        self.sensor_axe = self.sensor_axe.copy()
        adjust = self.sensor_axe.iloc[:int(n_linhas)].mean()
        self.sensor_axe = self.sensor_axe - adjust

        return self.sensor_axe
    
    def indentify_outliers(self, window, thresh=3, verbose=False):
        self.sensor_axe = self.sensor_axe.copy()
        outlier_mask = pd.DataFrame(False, index=self.sensor_axe.index, columns=self.sensor_axe.columns)
        for col in self.sensor_axe.columns:
            series = self.sensor_axe[col]
            rolling_mean = series.rolling(window=window, min_periods=1).mean()
            rolling_std = series.rolling(window=window, min_periods=1).std()
            z_scores = (series - rolling_mean) / rolling_std
            outliers = np.abs(z_scores) > thresh
            outlier_mask[col] = outliers

        return outlier_mask
    
    def remove_outliers(self, window, thresh=3, verbose=False):
        self.sensor_axe = self.sensor_axe.copy() #Ficar de olho nessas copias
        outlier_mask = self.indentify_outliers(window, thresh, verbose)
        self.sensor_axe = self.sensor_axe.mask(outlier_mask)
        self.sensor_axe = self.sensor_axe.interpolate(method='linear', limit_direction='both').fillna(0)

        return self.sensor_axe.round(4)
        
    def moving_average(self, sash):
        self.sensor_axe = self.sensor_axe.copy() 
        self.sensor_axe = self.sensor_axe.rolling(window=int(sash), min_periods=1).mean() 

        return self.sensor_axe.round(4)
        
    def calibration(self, factors):
        self.sensor_axe = self.sensor_axe.copy()
        self.sensor_axe = self.sensor_axe.multiply(factors, axis=1)

        return self.sensor_axe.round(4)

    def lowpass_filter(self, cutoff_freq, freq_rate=None, order=5): #Realizar alteração nesse valor
        self.sensor_axe = self.sensor_axe.copy()
        if freq_rate is None:
            freq_rate = self.rate()
        nyquist = 0.5 * freq_rate
        if cutoff_freq >= nyquist:
            print(f"[Cutoff ({cutoff_freq} Hz) é muito alto para esses dados.")
            print(f"        A frequência máxima permitida (Nyquist) é {nyquist:.4f} Hz.")
            cutoff_freq = nyquist * 0.99 
            print(f"        Ajustando cutoff automaticamente para {cutoff_freq:.4f} Hz") #Nyquist é oq busco
        low_pass = cutoff_freq / nyquist
        b, a = signal.butter(order, low_pass, btype='lowpass', analog=False)
        for col in self.sensor_axe.columns:
            self.sensor_axe[col] = signal.filtfilt(b, a, self.sensor_axe[col])

        return self.sensor_axe.round(4)

        