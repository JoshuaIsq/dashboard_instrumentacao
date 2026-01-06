import Teste_Model 
import Teste_view
import dearpygui.dearpygui as dpg

model = Teste_Model.LogImporter()
view = Teste_view.PrimaryView()

class Controller():
    def select_archive(sender, app_data):

        file_path = app_data['file_path_name']
        model.import_file(file_path)
        model.create_timestamp()
        eixo_x, df_sensores = model.join_files()

        if eixo_x is not None:
            view.graph_plot(eixo_x, df_sensores)


if __name__ == "__main__":
    # 2. Injeção de dependência: Passar a função do controller para a view
    view.set_callback(Controller.select_archive)
    
    # 3. Construir e rodar
    view.build_window()
    view.run()

