import dearpygui.dearpygui as dpg
import Teste_controller


dpg.create_context()

with dpg.font_registry():
    default_font = dpg.add_font("C:\\Windows\\Fonts\\Times.ttf", 20)

dpg.bind_font(default_font)


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

with dpg.file_dialog(directory_selector=False, show=False, callback=Teste_controller.select_archive, tag="file_dialog_id", width=700, height=400):
    dpg.add_file_extension(".txt", color=(0, 255, 0, 255))
    dpg.add_file_extension(".*")

with dpg.window(tag="Primary Window"):
    dpg.add_text("Vizualizador de dados de instrumentação", color=(0, 0, 0),)
    dpg.add_spacer(width=50)
    dpg.add_button(label='Selecionar arquivo', callback=lambda: dpg.show_item('file_dialog_id'))

    with dpg.group(horizontal=True):
            with dpg.plot(label="Extensômetros superiores", height=-1, width=-1, query=True,):
                dpg.add_plot_legend()
                xaxis = dpg.add_plot_axis(dpg.mvXAxis, label="Data / Hora", tag="eixo_x", time=True)
                yaxis = dpg.add_plot_axis(dpg.mvYAxis, label="Deslocamento (mm)", tag="eixo_y")



dpg.bind_item_theme("Primary Window", theme)
dpg.create_viewport(title='Analise Grafica', width=1000, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
