import pandas as pd
import numpy as np

import sys
import os

# Obtém o caminho da pasta atual (tests)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Obtém o caminho da pasta pai (dashboard_instrumentacao raiz)
parent_dir = os.path.dirname(current_dir)
# Adiciona a pasta pai ao caminho de busca do Python
sys.path.append(parent_dir)

# Certifique-se que sua classe Math está no arquivo Model.py
from dashboard_instrumentacao import Model
# 1. CRIAR DADOS DE TESTE (Senoide com ruído)
pontos = 100
x = np.linspace(0, 10, pontos)
data = {
    'Sensor_1': np.sin(x),
    'Sensor_2': np.cos(x)
}
df_teste = pd.DataFrame(data)

# 2. INSERIR OUTLIERS (Erros propositais)
print("--- Dados Originais (com erro inserido) ---")
df_teste.iloc[10, 0] = 50.0  # Erro gigante no sensor 1
df_teste.iloc[50, 1] = -50.0 # Erro gigante no sensor 2
print(df_teste.iloc[[10, 50]]) # Mostra os pontos errados

# 3. INSTANCIAR A CLASSE MATH
math_tool = Model.Math(x, df_teste)

# 4. RODAR REMOÇÃO DE OUTLIERS
print("\n--- Processando... ---")
# Janela de 5 pontos, limiar de 2 desvios padrão
df_limpo = math_tool.remove_outliers(window=50, thresh=2, verbose=True)

# 5. VERIFICAR RESULTADO
print("\n--- Dados Limpos ---")
print(df_limpo.iloc[[10, 50]])

# Verificação lógica
valor_corrigido_1 = df_limpo.iloc[10, 0]
valor_corrigido_2 = df_limpo.iloc[50, 1]

if abs(valor_corrigido_1) < 2 and abs(valor_corrigido_2) < 2:
    print("\nSUCESSO: Os valores gigantes foram removidos e interpolados!")
else:
    print("\nFALHA: Os valores ainda estão altos demais.")