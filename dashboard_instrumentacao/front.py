from calls import process
from Import_Calib_filter import DataStorage
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

with dpg.window(tag="Primary Window"):
    dpg.add_text("VISUALIZADOR DE EXTENSOMETRIA", color=(0, 0, 0),)
    dpg.add_spacer(width=50)

    
dpg.create_viewport(title='Analise Grafica', width=1000, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()