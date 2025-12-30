from dashboard_instrumentacao.controller import process, callback_zomm, select_archive
from dashboard_instrumentacao.Model import DataStorage as ds
import dearpygui.dearpygui as dpg

#----- 1. criação contexto front ------ #

dpg.create_context()

with dpg.font_registry():
    default_font = dpg.add_font("C:\\Windows\\Fonts\\Times.ttf", 20)

dpg.bind_font(default_font)

#------- 1. Definição da janela principal e seu design -------#

with dpg.theme() as tema_claro:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvPlotCol_PlotBg, (255, 255, 255, 255), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 0, 0, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (128, 128, 128, 255))
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (255, 255, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (200, 200, 200, 255))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0))

# ------- 2. janela para selecionar o arquivo a ser analisado -----#
with dpg.file_dialog(directory_selector=False, show=False, callback=select_archive, tag="file_dialog_id", width=700, height=400):
    dpg.add_file_extension(".txt", color=(0, 255, 0, 255))
    dpg.add_file_extension(".*")

#-------- 2 . Janela principal onde vemos tudo acontecer ----- #

with dpg.window(tag="Primary Window"):
    dpg.add_text("Vizualizador de dados de instrumentação", color=(0, 0, 0),)
    dpg.add_spacer(width=50)
    dpg.add_button(label='Selecionar arquivo', callback=lambda: dpg.show_item('file_dialog_id'))
    
    # ----- 2.1 grupo de janelas superior, onde ficam botões de ação ------- #
    with dpg.group(horizontal=True):
        dpg.add_separator()

        #----- 2.1.1 criação de botões --------
        class Button():
            def __init__(self, text: str, tag: str, label: str, is_float: bool = True):
                with dpg.group(horizontal=True):
                    with dpg.group(horizontal=False):
                        dpg.add_text(text)
                        if is_float == True:
                            dpg.add_input_float(default_value=0, width=120, tag=tag)
                        else:
                            dpg.add_input_int(default_value=0, width=120, tag=tag)
                        dpg.add_spacer(height=5)
                        dpg.add_button(label=label, callback=process)

                dpg.add_spacer(width=20)
        
        Button('Calibração:', 'input_calibration', 'Realizar calibração', is_float=True)
        Button('Remoção de Outliers:', 'input_outlier', 'Remover Outliers', is_float=False)
        Button('Ajuste de offset:', 'input_offset', 'Ajustar offset', is_float=False)


        dpg.add_spacer(width=10)
        dpg.add_separator()

    # ------ 2.2 grupo de janelas inferior, onde fica o grafico e seletor de canais -----
    with dpg.group(horizontal=True):
        
        # ---- 2.2.1 Cria a Caixa da Esquerda (Lista de Canais)
        with dpg.child_window(width=200, height=-1):
            dpg.add_text("Canais Disponíveis:")
            def toggle_all(sender, app_data):
                for col in ds.column_view:
                    dpg.set_value(ds.checkbox_tags[col], True)
                process(None, None, None)
            dpg.add_button(label="Marcar Todos", callback=toggle_all)
            dpg.add_separator()
            with dpg.group(tag="grupo_lista_canais"):
            # Cria os Checkboxes
                for col in ds.column_view:
                    tag_chk = f"chk_{col}"
                    ds.checkbox_tags[col] = tag_chk
                    comeca_marcado = True if col in ds.column_view[:3] else False
                    dpg.add_checkbox(label=f"Canal {col}", tag=tag_chk, default_value=comeca_marcado, callback=process)

        # ---- 2.2.2 Cria o gráfico como a janela principal da parte inferior ---- #
        with dpg.group(horizontal=True):
            with dpg.plot(label="Extensômetros superiores", height=-1, width=-1, query=True, callback=callback_zomm):
                dpg.add_plot_legend()
                xaxis = dpg.add_plot_axis(dpg.mvXAxis, label="Data / Hora", tag="eixo_x", time=True)
                yaxis = dpg.add_plot_axis(dpg.mvYAxis, label="Deslocamento (mm)", tag="eixo_y")

dpg.bind_item_theme("Primary Window", tema_claro)
dpg.create_viewport(title='Analise Grafica', width=1000, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
