import Teste_Model 
import Teste_view


model_import = Teste_Model.LogImporter()
view = Teste_view.PrimaryView()

class Controller():

    def select_archive(sender, app_data):
        file_path = app_data['file_path_name']
        model_import.import_file(file_path)
        model_import.create_timestamp()
        eixo_x, df_sensores = model_import.join_files()

        if eixo_x is not None:
            view.callback_checkbox(eixo_x, df_sensores)
    
        

if __name__ == "__main__":
   
    view.set_callback(Controller.select_archive)
    view.build_window()
    view.run()

