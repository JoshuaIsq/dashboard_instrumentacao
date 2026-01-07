import Model
import View

class Controller():

    def __init__(self, model, view):

        self.model = model
        self.view = view

    def select_archive(self, sender, app_data):
        file_path = app_data['file_path_name']
        self.model.import_file(file_path)
        self.model.create_timestamp()
        eixo_x, df_sensores = self.model.join_files()

        if eixo_x is not None:
            self.view.callback_checkbox(eixo_x, df_sensores)


