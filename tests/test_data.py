
from pathlib import Path
import pandas as pd

from pathlib import Path
import pandas as pd

# Lê o arquivo na mesma pasta do script e já imprime direto
caminho = r"C:\Users\joshua.marinho\Documents\dashboard_instrumentacao\tests\LOG_1.txt"
print(pd.read_csv(caminho, sep="\t", header=None))