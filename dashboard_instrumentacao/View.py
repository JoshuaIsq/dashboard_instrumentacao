import dearpygui.dearpygui as dpg
from sklearn import calibration
from .Theme import Theme
from .Model import Math

class PrimaryView():
    def __init__(self):
        self.callback_archive = None 
        self.data_sensors = None
        self.data_time = None
        self.callback_offset_func = None 
        self.callback_outliers = None 
        self.callback_calibration = None
        self.callback_lowwpass = None
        self.checkbox_tags = {}
        self.callback_tendency = None

        self.TAG_PLOT_TITLE = "graph title"
        self.TAG_PLOT_Y = "axe_y_title"
        self.TAG_PLOT_NEW_TITLE = "Extensômetros superiores"
        self.TAG_PLOT_NEW_Y = "Deslocamento (mm)"

    def set_callback(self, archive, offset, outliers, average, calibration, lowpass, tendency):
        self.callback_archive = archive
        self.callback_offset_func = offset
        self.callback_outliers = outliers
        self.callback_move_average = average
        self.callback_calibration = calibration
        self.callback_lowwpass = lowpass
        self.callback_tendency = tendency

    def run_lowpass_callback(self):
        if self.callback_lowwpass:
            cutoff = dpg.get_value("input_lowpass_cutoff")
            self.callback_lowwpass(cutoff_freq=cutoff, freq_rate=None, order=5)

    def run_calibration_callback(self):
        if self.callback_calibration:
            factors = dpg.get_value("input_calibration_factors")  
            self.callback_calibration(factors)

    def run_move_average_callback(self):
        if self.callback_move_average:
            sesh = dpg.get_value("input_moving_average")
            self.callback_move_average(sesh)            

    def run_offset_callback(self):
        if self.callback_offset_func:
            n_linhas = dpg.get_value("input_offset")
            self.callback_offset_func(n_linhas)
    
    def run_outliers_Callback(self):
        if self.callback_outliers:
            remove_out = dpg.get_value("input_outliers")
            self.callback_outliers(window=remove_out, thresh=3, verbose=False)

    def update_plot(self, time, sensors):
        self.data_sensors = sensors
        self.data_time = time   
        self.update_graph()
            
    def callback_checkbox(self, time, sensors):
        self.data_sensors = sensors
        self.data_time = time
        dpg.delete_item("grupo_lista_canais", children_only=True)
        self.checkbox_tags = {}
        cols = sensors.columns
        for i, col in enumerate(cols):
            is_checked = True if i < 5 else False
            tag = dpg.add_checkbox(label=f"Sensor {col-5}", parent="grupo_lista_canais", 
                                   default_value=is_checked, callback=self.update_graph)
            self.checkbox_tags[col] = tag
        self.update_graph()

    def update_titles(self, sender, app_data, user_data):
        window_tag = user_data
        new_title = dpg.get_value(self.TAG_PLOT_NEW_TITLE)
        new_axeY = dpg.get_value(self.TAG_PLOT_NEW_Y)
        if dpg.does_item_exist(self.TAG_PLOT_TITLE):
            dpg.set_item_label(self.TAG_PLOT_TITLE, new_title)
        if dpg.does_item_exist(self.TAG_PLOT_Y):
            dpg.set_item_label(self.TAG_PLOT_Y, new_axeY)
        if dpg.does_item_exist(window_tag):
            dpg.delete_item(window_tag)

    def update_graph(self, sender=None, app_data=None):
        if self.data_sensors is None:
            return
        if dpg.does_item_exist(self.TAG_PLOT_Y):
            dpg.delete_item(self.TAG_PLOT_Y, children_only=True)
        canais_ordenados = sorted(self.checkbox_tags.items())
        for i, (col_name, tag_id) in enumerate(canais_ordenados):
            if dpg.get_value(tag_id): 
                y_data = self.data_sensors[col_name].tolist()
                x_data = self.data_time
                y_data = [0 if (val != val) else val for val in y_data]
                label_nome = f"Sensor {col_name-5}" 
                line_tag = dpg.add_line_series(
                    x_data, 
                    y_data, 
                    label=label_nome, 
                    parent=self.TAG_PLOT_Y
                )
                tema_da_linha = Theme.get_line_theme(i)
                dpg.bind_item_theme(line_tag, tema_da_linha)

        dpg.fit_axis_data(self.TAG_PLOT_Y)
        dpg.fit_axis_data("eixo_x")

    def _button_config(self, text: str, label:str,tag:str, callbacks, is_float:bool = True, ):
        with dpg.group(horizontal=True):
            with dpg.group(horizontal=False):
                dpg.add_text(text)
                if is_float == True:
                    dpg.add_input_float(default_value=0, width=160, tag=tag, min_value=0, format="%.6f")
                else:
                    dpg.add_input_int(default_value=0, width=160, tag=tag, min_value=0)
                dpg.add_spacer(height=5)
                dpg.add_button(label=label, callback=callbacks) 
    
    def _main_window(self):
        dpg.add_text("Dashboard instrumentação", color=(0, 0, 0),)
        dpg.add_spacer(width=50)
        dpg.add_button(label='Selecionar arquivo', callback=lambda: dpg.show_item('file_dialog_id'))
        dpg.add_separator()

    def tendency_window(self):
        tag_win = 'Tendência'

        if dpg.does_item_exist(tag_win):
            dpg.delete_item(tag_win)

        tendency = self.callback_tendency()
        if tendency is None or tendency.empty:
            return
        
        with dpg.window(label=self.TAG_PLOT_NEW_TITLE, tag=tag_win, width=800, height=600):
            dpg.bind_item_theme(tag_win, Theme.color_tendency())
            dpg.add_text("Regressão Linear - Tendência dos Sensores")

            with dpg.plot(label=self.TAG_PLOT_NEW_TITLE, height=-1, width=-1):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="Data/Hora", time=True)

                with dpg.plot_axis(dpg.mvYAxis, label=self.TAG_PLOT_NEW_Y, tag="tendency_axe_y"):
                    dpg.set_axis_limits("tendency_axe_y",-40,40)
                    for i, col in enumerate(tendency.columns):
                        tag_chk = self.checkbox_tags.get(col)
                        if tag_chk and not dpg.get_value(tag_chk):
                            continue
                        y_data = tendency[col].tolist()
                        x_data = self.data_time
                        label_nome = f"Tendência Sensor {col-5}" 
                        line_tag = dpg.add_line_series(
                            x_data, 
                            y_data, 
                            label=label_nome, 
                            parent="tendency_axe_y"
                        )
                        tema_da_linha = Theme.get_line_theme(i)
                        dpg.bind_item_theme(line_tag, tema_da_linha)

    
    def _button_play(self):
        with dpg.group(horizontal=True):
            self._button_config("Ajuste de offset", "Aplicar offset", \
                                "input_offset",callbacks=self.run_offset_callback, is_float=False)
            dpg.add_spacer(width=20)
            self._button_config("Remoção de outliers", "Remover outliers", \
                                "input_outliers", callbacks=self.run_outliers_Callback, is_float=False)
            dpg.add_spacer(width=20)
            self._button_config("Média Movel", "Aplicar média movel", \
                                "input_moving_average", callbacks=self.run_move_average_callback, is_float=True)
            self._button_config("Fator de Calibração", "Aplicar calibração", \
                                "input_calibration_factors", callbacks=self.run_calibration_callback, is_float=True)
            self._button_config("Filtro passa-baixa (Hz)", "Aplicar filtro", \
                                "input_lowpass_cutoff", callbacks=self.run_lowpass_callback, is_float=True)
            
        dpg.add_spacer(height=10)

        with dpg.group(horizontal=True):
            dpg.add_button(label="Exibir Tendência", callback=self.tendency_window)
            dpg.add_spacer(width=20)

    def _chanel_list(self):
        with dpg.group(horizontal=False):
            with dpg.child_window(width=200, height=-1):
                dpg.add_text('Selecionar canais: ')
                dpg.add_separator()
                dpg.add_group(tag="grupo_lista_canais")
                    
            dpg.add_spacer(width=15)
    
    def _plot_area(self):
        with dpg.group(horizontal=True):
            with dpg.plot(label="Extensômetros superiores", height=-1, width=1250, query=True, tag=self.TAG_PLOT_TITLE):
                dpg.add_plot_legend()
                xaxis = dpg.add_plot_axis(dpg.mvXAxis, label="Data / Hora", tag="eixo_x", time=True)
                yaxis = dpg.add_plot_axis(dpg.mvYAxis, label="Deslocamento (mm)", tag=self.TAG_PLOT_Y)
                dpg.set_axis_limits(self.TAG_PLOT_Y,-40,40)
    
    def _build_sidebar(self):
        with dpg.group(horizontal=False):
            dpg.add_button(label="Configurar títulos", callback=lambda: dpg.show_item("config_window"))
            dpg.add_spacer(height=10)
            dpg.add_separator()
        with dpg.window(label="Editar titulos", tag="config_window", width=300, height=200, show=False, modal=True):
            dpg.add_text("Configurações Visuais:")
            dpg.add_input_text(label="Título", tag=self.TAG_PLOT_NEW_TITLE, default_value="Extensômetros", width=120)
            dpg.add_input_text(label="Nome Eixo Y", tag=self.TAG_PLOT_NEW_Y, default_value="Deslocamento (mm)", width=120)
            dpg.add_spacer(height=5)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Atualizar Títulos", callback=lambda: [self.update_titles(None, None, None), dpg.hide_item("config_window")], user_data="config_window")
                dpg.add_button(label="Cancelar", callback=lambda: dpg.hide_item("janela_titulos"))
                
    def build_window(self):
        dpg.create_context()
        Theme.font()

        #selecionar arquivo
        with dpg.file_dialog(directory_selector=False, show=False, callback=self.callback_archive, \
                             tag="file_dialog_id", width=700, height=400):
            dpg.add_file_extension(".txt", color=(0, 255, 0, 255))
            dpg.add_file_extension(".*")

        #janela principal
        with dpg.window(tag="Primary Window"):
            self._main_window()
            self._button_play()
            self._build_sidebar()
            dpg.add_spacer(height=10)
            with dpg.group(horizontal=True):
                self._chanel_list()
                self._plot_area()


    
    def run(self):
        dpg.bind_item_theme("Primary Window", Theme.color_main())
        dpg.create_viewport(title='Analise Grafica', width=1000, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()
