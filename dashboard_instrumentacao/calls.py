import pandas as pd
import numpy as np
import scipy as sp
from scipy import signal
import dearpygui.dearpygui as dpg
from Import_Calib_filter import DataStorage as ds
from Import_Calib_filter import Load_data, adjust_offset, moving_average, filter_low_pass, filter_high_pass, calibration

# ---- 1. seleção de arquivo -------#

def process(sender, app_data, user_data):

    if ds.df_sensores.empty: 
        return

    df_trabalho = ds.df_sensores.copy()

    calib = dpg.get_value("imput_calibration")
    if calib > 0:
        df_trabalho = calibration(df_trabalho, calib)



    dpg.delete_item("eixo_y", children_only=True)

    for col_name in ds.colum_view:
        tag_check = ds.checkbox_tags.get(col_name)

        if tag_check and dpg.get_value(tag_check):
            if col_name in df_trabalho.columns:
                value_y = df_trabalho[col_name].tolist()
                dpg.add_line_series(ds.df_timestamp, value_y, parent="eixo_y", label=f"Ext {col_name}")

    ds.df_actual_view = df_trabalho.copy()

def callback_zomm(sender, app_data):
    x_min, x_max = app_data[0], app_data[1]
    y_min, y_max = app_data[2], app_data[3]
    dpg.set_axis_limits("eixo_x", x_min, x_max)
    dpg.set_axis_limits("eixo_y", y_min, y_max)




"""def select_archive(sender, app_data):

    file_path = app_data("file_path")

    ds.df_timestamp, ds.df_sensores = Load_data(file_path)

    if len(ds.df_timestamp) > 0:
        ds.colum_view = ds.df_sensores.columns.tolist()
         # 2. Reconstrói a lista de Checkboxes
        dpg.delete_item("grupo_lista_canais", children_only=True)
        ds.checkbox_tags.clear()
        
        for col in ds.colum_view:
            tag_chk = f"chk_{col}"
            ds.checkbox_tags[col] = tag_chk
            # Marca os 3 primeiros por padrão
            estado = True if col in ds.colum_view[:3] else False
            dpg.add_checkbox(label=f"Ext {col}", tag=tag_chk, default_value=estado, callback=processar_e, parent="grupo_lista_canais")
        
        processar_e_plotar(None, None, None)
        dpg.fit_axis_data("eixo_x")
        dpg.fit_axis_data("eixo_y")
        dpg.set_axis_limits("eixo_y",-40, 40)"""
    

    
    

