import sys
import os

# Garante que o python enxergue as pastas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa a função do View
from dashboard_instrumentacao.View import run_interface

if __name__ == "__main__":
    # Aqui sim chamamos a execução!
    run_interface()