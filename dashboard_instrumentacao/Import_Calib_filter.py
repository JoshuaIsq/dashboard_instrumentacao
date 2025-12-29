import pandas as pd
import numpy as np
import scipy as sp
from scipy import signal
import dearpygui.dearpygui as dpg

class DataStorage:

    """Classe criada para armazenar listas

    o DearPygui trabalha apenas com, leitura de listas, sendo necessário adicionar
    os dados coletados pelos sensores e os timestamps em uma lista, para assim o Dpg poder
    o interpretar
    
    A classe é composta pelas listas
    df_timestamp: Armazena dados de tempo (eixo x)
    df_sensors: Armaze os dados dos sensores (eixo Y)
    checkbox_tags: Marcação de tags para selecionar sensores
    colum_view: colunas que estão marcadas
    acumullated: Arquivos acumulados para futura concatenação
    df_actual_view: Mostra o dataframe com suas respectivas modificações (filtros, offset e etc)
    """

    df_timestamp = []  
    df_sensores = pd.DataFrame() 
    checkbox_tags = {} 
    colum_view = [] 
    acumullated = [] 
    df_actual_view = pd.DataFrame() 

    #----- 1. importação e calibração ------------ #

def Load_data(filename):

    '''Função responsável por carregar os arquivos para a analise
   
    A função primeiramente verifica se o arquivo é um txt, se for ele, tranforma em lista 
    Os concatena arquivo a arquivo
    Após isso pega essas listas e a armazena na lista file_To_process (correspondente aos arquivos que serão modificados)
    junta a coluna do timestamp com a de sensores a partir da time_and_sensor
    Além de começar com a quantidade de colunas padronizada como 0
    
    Tratamos os dados separando o tempo corrido dos sensores e organizando o tempo'''
    
    if isinstance(filename, str): 
        filenames = [filename] 


    if filename:
        for f in filenames:
            if f not in DataStorage.acumullated:
                DataStorage.acumullated.append(f) #Adiciona outros arquivos um em cima do outro


    file_to_process = DataStorage.acumullated
    time_and_sensor = [] #Futura lista para armazenar o timestamp e sensores
    standart_column = None 


    for arquivo in file_to_process: 
        if arquivo.endswith('.txt'):
            #arquivo = r"C:\Users\joshua.marinho\Documents\dashboard_instrumentacao\tests\LOG_1.txt"
            txt_file = pd.read_csv(arquivo, sep='\t', header=None, engine='python', on_bad_lines='skip' )

            print(f"Lendo arquivo {arquivo}, colunas encontradas: {(txt_file.shape[1])}")

            num_colunas = txt_file.shape[1]
            if standart_column == None:
                standart_column = num_colunas
            elif standart_column != num_colunas:
                print("A quantidade de colunas do arquivo não é compativel")

            colum_time = [0, 1, 2, 3, 4, 5]
            for col in colum_time:
                txt_file[col] = pd.to_numeric(txt_file[col], errors='coerce') 
            txt_file[colum_time] = txt_file[colum_time].astype(int)
            time_cols = txt_file.iloc[:, 0:6] 
            time_cols.columns = ["day", "month", "year", "hour", "minute", "second"]
            timestamp = pd.to_datetime(time_cols) 
            df_temp = pd.DataFrame({'timestamp': timestamp}) 
            df_temp = pd.concat([df_temp, txt_file.iloc[:, 6:]], axis=1) 
            time_and_sensor.append(df_temp) 

    df_full = pd.concat(time_and_sensor, ignore_index=True) 
    df_sorted = df_full.sort_values(by='timestamp').reset_index(drop=True) #ordena os timestamps por ordem, deixando o arquivo organizado
    axe_x_time = (df_sorted['timestamp'].astype('int64') / 10**9).tolist() 
    raw_data = df_sorted.iloc[:, 1:].copy() #pego as colunas da 1 pra frente (a 0 virou um timestamp) e ficam so os sensores

    for col in raw_data.columns:
        raw_data[col] = pd.to_numeric(raw_data[col], errors='coerce')    
    sensors = raw_data.fillna(0.0)

    return axe_x_time, sensors


def calibration(df, factor):
    sensor = df.copy()
    factor_val = float(factor)
    calibration = sensor * factor_val

    return calibration


# ---- 2. Filtros e ajustes ------

"""Este trecho contem todas as funções de filtros e ajustes que podem ser aplicados

    Moving_average: Suaviza os dados aplicando uma média móvel com janela definida pelo usuário.
    Adjust_offset: Remove o offset inicial dos dados com base na média dos primeiros n pontos.
    Filter_low_pass: Aplica um filtro Butterworth passa baixa para remover ruídos de alta frequência.
    Filter_high_Pass: Aplica um filtro Butterworth passa alta para remover tendências de baixa frequência.
    Identify_outliers: Detecta pontos fora do padrão usando z-score baseado em média móvel.
    Remove_outliers: Substitui os outliers identificados por interpolação linear.
    """

def moving_average(df, janela):
    df_copia = df.copy() 
    df_copia = df_copia.rolling(window=int(janela), min_periods=1).mean() 

    return df_copia.round(4)

def adjust_offset(df, n_linhas):
    df_copia = df.copy()
    adjust = df_copia.iloc[:int(n_linhas)].mean()
    df_copia = df_copia - adjust

    return df_copia


def filter_low_pass(df, cut_freq, sample_rate, order):
    df_copia = df.copy()
    nyquisfreq = 0.5 * sample_rate
    low_pass_ratio = cut_freq/nyquisfreq
    b, a = signal.butter(order, low_pass_ratio, btype="lowpass")
    for col in df_copia.columns:
        df_copia[col] = signal.filtfilt(b, a, df_copia[col])

    return df_copia.round(4)


def filter_high_pass(df, freq_corte, freq_rate, order):
    df_copia = df.copy()
    nyquisfreq = 0.5 * freq_rate
    filter_high_pass = freq_corte/nyquisfreq
    b, a = signal.butter(order, filter_high_pass, btype="highpass")
    for col in df_copia.columns:
        df_copia[col] = signal.filtfilt(b, a, df_copia[col])

    return df_copia.round(4)

#Avaliar a possiblidade de transformar em uma função só
def indentify_outliers(df, window, thresh=3, verbose=False):
    df_copia = df.copy()
    outlier_mask = pd.DataFrame(False, index=df_copia.index, columns=df_copia.columns)
    for col in df_copia.columns:
        series = df_copia[col]
        rolling_mean = series.rolling(window=window, min_periods=1).mean()
        rolling_std = series.rolling(window=window, min_periods=1).std()
        z_scores = (series - rolling_mean) / rolling_std
        outliers = np.abs(z_scores) > thresh
        outlier_mask[col] = outliers
        if verbose:
                print(f"[INFO] Coluna: {col}")
                print(f"       Média: {series.mean():.2f}, Desvio padrão: {series.std():.2f}")
                print(f"       Outliers detectados: {outliers.sum()} de {len(series)}\n")

    return outlier_mask
    
def remove_outliers(df, window, thresh=3, verbose=False):
    df_copia = df.copy()
    outlier_mask = indentify_outliers(df_copia, window, thresh, verbose)
    df_copia = df_copia.mask(outlier_mask)
    df_copia = df_copia.interpolate(method='linear', limit_direction='both').fillna(0)

    return df_copia.round(4)

#-------3. Calculo da tendência global ---------

def tendency(df, window_size=None): 
    """
    Calcula a TENDÊNCIA GLOBAL (Regressão Linear Simples).
    Gera uma reta única que mostra a direção geral (drift) dos dados.
    """
    df_copia = df.copy()
    tendencia_df = pd.DataFrame()
    
    print("Calculando Regressão Linear")
    
    x_axis = np.arange(len(df_copia))
    
    for col in df_copia.columns:
        y_axis = df_copia[col].values
        
        try:
            #calcula a regressão linear
            coeficientes = np.polyfit(x_axis, y_axis, 1)
            
            # Cria a função da reta: f(x) = ax + b
            funcao_reta = np.poly1d(coeficientes)
            
            # Gera os pontos da reta para plotar
            tendencia_df[col] = funcao_reta(x_axis)
            
        except Exception as e:
            print(f"Erro na regressão global de {col}: {e}")
            tendencia_df[col] = y_axis 

    return tendencia_df.round(4)


def actual_tendency(janela_pontos=None):
    if DataStorage.df_visualizacao_atual.empty:
        print("[Erro] Nenhum dado disponível.")
        return None
    
    # Não precisamos mais passar janela para essa lógica global
    return tendency(DataStorage.df_visualizacao_atual)


