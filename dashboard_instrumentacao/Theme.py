import dearpygui.dearpygui as dpg

class Theme():

    LINE_COLORS = [
        (255, 0, 0),        # 0. Vermelho
        (0, 0, 255),        # 1. Azul
        (0, 200, 0),        # 2. Verde Escuro
        (255, 165, 0),      # 3. Laranja
        (128, 0, 128),      # 4. Roxo
        (0, 255, 255),      # 5. Ciano
        (255, 0, 255),      # 6. Magenta
        (165, 42, 42),      # 7. Marrom
        (0, 128, 128),      # 8. Teal (Verde-azulado)
        (255, 192, 203),    # 9. Rosa
        (128, 128, 0),      # 10. Oliva
        (75, 0, 130),       # 11. Indigo
        (255, 215, 0),      # 12. Dourado
        (128, 128, 128),    # 13. Cinza
        (0, 0, 0),          # 14. Preto
        (50, 205, 50),      # 15. Verde Lima
        (250, 128, 114),    # 16. Salmão
        (70, 130, 180)      # 17. Azul Aço
    ]

    @staticmethod
    def get_line_theme(index):
    
        # Garante que não vai dar erro se vier o índice 19, 20... ele recicla as cores
        safe_index = index % len(Theme.LINE_COLORS)
        color = Theme.LINE_COLORS[safe_index]

        with dpg.theme() as theme:
            # mvLineSeries é o componente específico para linhas de plot
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(dpg.mvPlotCol_Line, color, category=dpg.mvThemeCat_Plots)
                # Opcional: Definir espessura ou estilo do marcador aqui também
                # dpg.add_theme_style(dpg.mvStyleVar_Marker, dpg.mvMarker_Circle) 
        
        return theme
    
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