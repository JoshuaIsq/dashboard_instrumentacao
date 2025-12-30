import pandas as pd
import numpy as np
import scipy as sp
from scipy import signal
import dearpygui.dearpygui as dpg
from dashboard_instrumentacao.Model import DataStorage as ds
from dashboard_instrumentacao.Model import Load_data, remove_outliers, adjust_offset, moving_average, filter_low_pass, filter_high_pass, calibration

"""Criado para processar as informações contidas nos gráficos e dados manipulados, e os exporta pro gráfico
Contem as funções 
Process: Tem como objetivo pegar a lista de sensores com dados já importados,
e aplicar calibração, offset e filtros
callback_zoom: Adicionar zoom ao gráfico
def_select_archive: função para escolher qual arquivo você irá plotar"""

"Nenhuma das classes do datastorage precisa estar ali, elas tem de ser protegidas"
"Melhor criar uma classe aqui e as proteger"


# ---- 1. seleção de arquivo -------#

def process(sender, app_data, user_data):

    if ds.df_sensores.empty: 
        return
    
    df_trabalho = ds.df_sensores.copy()

# ---- 2. Criaçã0 de botões de ação ----- #
    calib = dpg.get_value("input_calibration")
    df_trabalho = calibration(df_trabalho, calib)
        

    outlier = dpg.get_value("input_outlier")
    df_trabalho = remove_outliers(df_trabalho, window=outlier, thresh=3, verbose=False)

    offset = dpg.get_value('input_offset')
    df_trabalho = adjust_offset(df_trabalho, offset)
     
# ----- 3. Criação das checkbox --------

    dpg.delete_item("eixo_y", children_only=True)

    for col_name in ds.column_view:
        tag_check = ds.checkbox_tags.get(col_name)

        if tag_check and dpg.get_value(tag_check):
            if col_name in df_trabalho.columns:
                value_y = df_trabalho[col_name].tolist()
                dpg.add_line_series(ds.df_timestamp, value_y, parent="eixo_y", label=f"Ext {col_name-5}")

    ds.df_actual_view = df_trabalho.copy()

# ----- 4. Criação do zoom ------ #

def callback_zomm(sender, app_data):
    x_min, x_max = app_data[0], app_data[1]
    y_min, y_max = app_data[2], app_data[3]
    dpg.set_axis_limits("eixo_x", x_min, x_max)
    dpg.set_axis_limits("eixo_y", y_min, y_max)


# ----- 5. Selecionador de arquivos ------- #

def select_archive(sender, app_data):

    file_path = app_data['file_path_name']

    ds.df_timestamp, ds.df_sensores = Load_data(file_path)

    if len(ds.df_timestamp) > 0:
        ds.column_view = ds.df_sensores.columns.tolist()
         # 2. Reconstrói a lista de Checkboxes
        dpg.delete_item("grupo_lista_canais", children_only=True)
        ds.checkbox_tags.clear()
        
        for col in ds.column_view:
            tag_chk = f"chk_{col}"
            ds.checkbox_tags[col] = tag_chk
            estado = True if col in ds.column_view[:3] else False
            dpg.add_checkbox(label=f"Ext {col-5}", tag=tag_chk, default_value=estado, callback=process, parent="grupo_lista_canais")
        
        process(None, None, None)
        dpg.fit_axis_data("eixo_x")
        dpg.fit_axis_data("eixo_y")
        dpg.set_axis_limits("eixo_y",-40, 40)

    

    
    

