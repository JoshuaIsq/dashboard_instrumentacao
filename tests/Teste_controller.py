import Teste_Model 
import Teste_view


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
        math_tool = Teste_Model.Math(self.eixo_x, self.df_sensores.copy())
        df_com_offset = math_tool.adjust_offset(n_linhas)
        self.df_sensores = df_com_offset
        self.view.callback_checkbox(self.eixo_x, df_com_offset)


    
if __name__ == "__main__":
    model = Teste_Model.LogImporter()
    view = Teste_view.PrimaryView()
    controller = Controller(model, view)
    
    view.set_callback(controller.select_archive)
    view.set_offset_callback(controller.apply_offset)

    view.build_window()
    view.run()

