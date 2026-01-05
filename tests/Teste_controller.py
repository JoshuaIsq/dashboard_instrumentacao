import Teste_Model_POO
import dearpygui.dearpygui as dpg

model = Teste_Model_POO.LogImporter()

def select_archive(sender, app_data):

    file_path = app_data['file_path_name']
    model.import_file(file_path)
    model.create_timestamp()
    # Pegamos os dados prontos
    eixo_x, df_sensores = model.join_files()

    # 3. Mandar desenhar na View (O momento da mágica)
    if eixo_x is not None:
        plotar_graficos(eixo_x, df_sensores)

def plotar_graficos(eixo_x, df_sensores):
    """
    Função separada só para lidar com a parte visual do DPG
    """
    # LIMPEZA: Antes de desenhar, limpamos as linhas antigas
    # Precisamos deletar os filhos do eixo Y (onde as linhas ficam penduradas)
    # Supondo que na View você deu a tag="eixo_y" para o eixo Y
    dpg.delete_item("eixo_y", children_only=True)

    # LOOP DE DESENHO
    # Para cada coluna (sensor) no seu DataFrame...
    for nome_sensor in df_sensores.columns:
        
        # Pegamos os dados da coluna e transformamos em lista (o DPG exige lista)
        eixo_y = df_sensores[nome_sensor].tolist()
        
        # Criamos a linha no gráfico
        # parent="eixo_y" -> Diz que essa linha pertence ao eixo Y criado na View
        dpg.add_line_series(eixo_x, eixo_y, label=nome_sensor, parent="eixo_y")
        
    # Ajusta o zoom para caber tudo
    dpg.fit_axis_data("eixo_y")
    dpg.fit_axis_data("eixo_x") # Supondo que você deu tag="eixo_x" no eixo X