import dearpygui.dearpygui as dpg

class Theme():

    LINE_COLORS = [
        (255, 0, 0, 255),        # 0. Vermelho
        (0, 0, 255, 255),        # 1. Azul
        (0, 200, 0, 255),        # 2. Verde Escuro
        (255, 165, 0, 255),      # 3. Laranja
        (128, 0, 128, 255),      # 4. Roxo
        (0, 255, 255, 255),      # 5. Ciano
        (255, 0, 255, 255),      # 6. Magenta
        (165, 42, 42, 255),      # 7. Marrom
        (0, 128, 128, 255),      # 8. Teal (Verde-azulado)
        (255, 192, 203, 255),    # 9. Rosa
        (128, 128, 0, 255),      # 10. Oliva
        (75, 0, 130, 255),       # 11. Indigo
        (255, 215, 0, 255),      # 12. Dourado
        (128, 128, 128, 255),    # 13. Cinza
        (0, 0, 0, 255),          # 14. Preto
        (50, 205, 50, 255),      # 15. Verde Lima
        (250, 128, 114, 255),    # 16. Salmão
        (70, 130, 180, 255)      # 17. Azul Aço
    ]

    @staticmethod
    def get_line_theme(index):
    
        safe_index = index % len(Theme.LINE_COLORS)
        color = Theme.LINE_COLORS[safe_index]

        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvLineSeries):
                dpg.add_theme_color(dpg.mvPlotCol_Line, color, category=dpg.mvThemeCat_Plots)
        
        return theme
    
    @staticmethod
    def color_main():
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvPlotCol_PlotBg, (255, 255, 255, 255), category=dpg.mvThemeCat_Plots)
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (178, 34, 34))
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

    def color_tendency():
        with dpg.theme() as theme:
            with dpg.theme_component(dpg.mvAll):
                # Fundo Branco (Usando Core, que é compatível com todas as versões)
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
                # Texto e Bordas Pretos
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
        return theme
    
    
    @staticmethod
    def init_logo(image_path, tag_name="texture_logo"):
        
        try:
            width, height, channels, data = dpg.load_image("C:/Users/joshua.marinho/Desktop/ISQ-Logo-big.png")
        except TypeError:
            print(f"Erro: Não foi possível carregar a imagem em {'C:/Users/joshua.marinho/Desktop/ISQ-Logo-big.png'}")
            return 0, 0

        
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width=width, height=height, default_value=data, tag=tag_name)
            
        return width, height