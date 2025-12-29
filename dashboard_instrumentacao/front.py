from calls import process, callback_zomm, select_archive
from Import_Calib_filter import DataStorage as ds
import dearpygui.dearpygui as dpg

#----- 1. criação contexto front ------ #

dpg.create_context()

with dpg.font_registry():
    default_font = dpg.add_font("C:\\Windows\\Fonts\\Times.ttf", 20)

dpg.bind_font(default_font)

#------- 1. Definição da janela principal e seu design -------#

with dpg.theme() as tema_claro:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 255, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255, 255, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (255, 255, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (240, 240, 240))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Border, (255, 255, 255))

with dpg.file_dialog(directory_selector=False, show=False, callback=select_archive, tag="file_dialog_id", width=700, height=400):
    dpg.add_file_extension(".txt", color=(0, 255, 0, 255))
    dpg.add_file_extension(".*")

with dpg.window(tag="Primary Window"):
    dpg.add_text("VISUALIZADOR DE EXTENSOMETRIA", color=(0, 0, 0),)
    dpg.add_spacer(width=50)
    dpg.add_button(label='Selecionar arquivo', callback=lambda: dpg.show_item('file_dialog_id'))

    with dpg.group(horizontal=True):
        with dpg.group(horizontal=True):
            with dpg.group(horizontal=False):
                dpg.add_text("Calibração:")
                dpg.add_input_float(default_value=0, width=90, tag="input_calibration")
                dpg.add_spacer(height=20)
                dpg.add_button(label="Aplicar calibração", callback=process)

    with dpg.group(horizontal=True):
        
        # ---- 4.3.2 Cria a Caixa da Esquerda (Lista de Canais)
        with dpg.child_window(width=200, height=-1):
            dpg.add_text("Canais Disponíveis:")
            
            # Botão Auxiliar
            def toggle_all(sender, app_data):
                for col in ds.colum_view:
                    dpg.set_value(ds.checkbox_tags[col], True)
                process(None, None, None)
            
            dpg.add_button(label="Marcar Todos", callback=toggle_all)
            dpg.add_separator()

            with dpg.group(tag="grupo_lista_canais"):

            # Cria os Checkboxes
                for col in ds.colum_view:
                    tag_chk = f"chk_{col}"
                    ds.checkbox_tags[col] = tag_chk
                    
                    # Marcano os 3 primeiros canais
                    comeca_marcado = True if col in ds.colum_view[:3] else False
                    
                    # Cria o checkbox e avisa que se clicar, chama o 'processar_e_plotar'
                    dpg.add_checkbox(label=f"Canal {col}", tag=tag_chk, default_value=comeca_marcado, callback=process)

        with dpg.group(horizontal=True):
            with dpg.plot(label="Extensômetros superiores", height=-1, width=-1, query=True, callback=callback_zomm):
                dpg.add_plot_legend()
                
                xaxis = dpg.add_plot_axis(dpg.mvXAxis, label="Data / Hora", tag="eixo_x", time=True)
                yaxis = dpg.add_plot_axis(dpg.mvYAxis, label="Deslocamento (mm)", tag="eixo_y")


dpg.create_viewport(title='Analise Grafica', width=1000, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()