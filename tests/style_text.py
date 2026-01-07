import Teste_Model 
import Teste_view

class Controller():

    def __init__(self, model, view):
        self.model = model
        self.view = view
        # Variáveis para guardar os dados atuais na memória do Controller
        self.df_sensores_atual = None
        self.eixo_x_atual = None
    
    def select_archive(self, sender, app_data):
        # 1. Proteção simples
        if 'file_path_name' not in app_data: return
        file_path = app_data['file_path_name']
        
        # 2. Usa o self.model (que recebemos no __init__)
        self.model.import_file(file_path)
        self.model.create_timestamp()
        
        # 3. CRUCIAL: Salva os dados no SELF para usar no offset depois
        self.eixo_x_atual, self.df_sensores_atual = self.model.join_files()

        if self.eixo_x_atual is not None:
            # Chama a view para plotar (se sua view usar update_data_and_checkboxes, use ela)
            # Se for callback_checkbox, mantenha:
            self.view.callback_checkbox(self.eixo_x_atual, self.df_sensores_atual)

    def apply_offset(self, n_linhas):
        # Verifica se tem dados carregados
        if self.df_sensores_atual is None:
            print("Carregue um arquivo primeiro!")
            return

        print(f"Calculando offset com {n_linhas} linhas...")

        # 4. Instancia a classe Math AQUI, passando os dados atuais
        # Nota: Teste_Model.Math (NomeDoArquivo.NomeDaClasse)
        math_tool = Teste_Model.Math(self.eixo_x_atual, self.df_sensores_atual.copy())
        
        # Calcula
        df_com_offset = math_tool.adjust_offset(n_linhas)

        # Atualiza os dados atuais e manda a view redesenhar
        self.df_sensores_atual = df_com_offset
        self.view.callback_checkbox(self.eixo_x_atual, df_com_offset)
        

if __name__ == "__main__":
    # --- AQUI ESTÁ A ADIÇÃO NO MAIN QUE VOCÊ PEDIU ---
    
    # 1. Instanciar as peças
    model = Teste_Model.LogImporter()
    view = Teste_view.PrimaryView()
    
    # 2. Instanciar o Controller (Juntando as peças)
    controller = Controller(model, view)
    
    # 3. Conectar botão de Arquivo
    view.set_callback(controller.select_archive)
    
    # 4. Conectar botão de Offset (ESSA É A PARTE NOVA)
    # Certifique-se que você criou o método set_offset_callback na View como te mostrei antes
    view.set_offset_callback(controller.apply_offset) 
    
    #rodar
    view.build_window()
    view.run()