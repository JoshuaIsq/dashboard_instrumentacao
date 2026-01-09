import dearpygui.dearpygui as dpg

class Theme():

    @staticmethod
    def color():
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvPlotCol_PlotBg, (255, 255, 255, 255), category=dpg.mvThemeCat_Plots)
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (100, 149, 237))
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (220, 220, 220))
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (255, 255, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_Button, (220, 220, 220))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0))
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0.3)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
        return theme
        
    @staticmethod
    def font():
        with dpg.font_registry():
            default_font = dpg.add_font("C:\\Windows\\Fonts\\Arial.ttf", 20)
        dpg.bind_font(default_font)