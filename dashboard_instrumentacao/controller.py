from .Model import LogImporter
from .Model import Math
from .View import PrimaryView

class Controller():

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.df_sensores = None
        self.eixo_x = None
    
    
    def select_archive(self, sender, app_data):
        file_path = app_data['file_path_name']
        self.model.import_file(file_path)
        self.model.create_timestamp()
        self.eixo_x, self.df_sensores = self.model.join_files()

        if self.eixo_x is not None:
            self.view.callback_checkbox(self.eixo_x, self.df_sensores)
    
    
    def apply_offset(self, n_linhas):
        if self.df_sensores is None:
            print("Nenhum arquivo carregado para aplicar offset.")
            return
        print(f"Aplicando offset")
        math_tool = Math(self.eixo_x, self.df_sensores.copy())
        df_com_offset = math_tool.adjust_offset(n_linhas)
        self.df_sensores = df_com_offset
        self.view.callback_checkbox(self.eixo_x, df_com_offset)

