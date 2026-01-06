import Teste_Model 
import Teste_view


model = Teste_Model.LogImporter()
view = Teste_view.PrimaryView()

class Controller():

    def select_archive(sender, app_data):
        file_path = app_data['file_path_name']
        model.import_file(file_path)
        model.create_timestamp()
        eixo_x, df_sensores = model.join_files()

        if eixo_x is not None:
            view.callback_checkbox(eixo_x, df_sensores)



if __name__ == "__main__":
   
    view.set_callback(Controller.select_archive)
    view.build_window()
    view.run()

