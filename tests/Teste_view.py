import dearpygui.dearpygui as dpg
import pandas as pd
import Teste_Model 

acesso = Teste_Model.LogImporter()


class PrimaryView():

    def __init__(self):
        self.callback_archive = None 
        self.data_sensors = None
        self.data_time = None


    def set_callback(self, func):
        self.callback_archive = func

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

    def update_graph(self, sender=None, app_data=None):
        if self.data_sensors is None:
            return
        dpg.delete_item("eixo_y", children_only=True)
        for col_name, tag_id in self.checkbox_tags.items():
            if dpg.get_value(tag_id): 
                axe_y = self.data_sensors[col_name].tolist()
                dpg.add_line_series(self.data_time, axe_y, label=str(col_name-5), parent="eixo_y")

        dpg.fit_axis_data("eixo_y")
        dpg.fit_axis_data("eixo_x")

            
    def _select_source(self):
        with dpg.font_registry():
            default_font = dpg.add_font("C:\\Windows\\Fonts\\Times.ttf", 20)
        dpg.bind_font(default_font)


    def colors(self):
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvPlotCol_PlotBg, (255, 255, 255, 255), category=dpg.mvThemeCat_Plots)
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 0, 0, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (128, 128, 128, 255))
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (255, 255, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_Button, (200, 200, 200, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0))
        return theme
    
    
    def build_window(self):
        dpg.create_context()
        self._select_source()

        #selecionar arquivo
        with dpg.file_dialog(directory_selector=False, show=False, callback=self.callback_archive, tag="file_dialog_id", width=700, height=400):
            dpg.add_file_extension(".txt", color=(0, 255, 0, 255))
            dpg.add_file_extension(".*")

        #janela principal
        with dpg.window(tag="Primary Window"):
            dpg.add_text("Vizualizador de dados de instrumentação", color=(0, 0, 0),)
            dpg.add_spacer(width=50)
            dpg.add_button(label='Selecionar arquivo', callback=lambda: dpg.show_item('file_dialog_id'))

            with dpg.group(horizontal=True):
                dpg.add_separator()
                
                #seletor de canais
                with dpg.child_window(width=200, height=-1):
                    dpg.add_text('Selecionar canais: ')
                    dpg.add_separator()
                    dpg.add_group(tag="grupo_lista_canais")
                       
                #gráfico plotado
                with dpg.group(horizontal=True):
                        with dpg.plot(label="Extensômetros superiores", height=-1, width=-1, query=True,):
                            dpg.add_plot_legend()
                            xaxis = dpg.add_plot_axis(dpg.mvXAxis, label="Data / Hora", tag="eixo_x", time=True)
                            yaxis = dpg.add_plot_axis(dpg.mvYAxis, label="Deslocamento (mm)", tag="eixo_y")

    
    def run(self):
        dpg.bind_item_theme("Primary Window", self.colors())
        dpg.create_viewport(title='Analise Grafica', width=1000, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Primary Window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()
