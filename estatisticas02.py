#Importando Bibliotecas
import pandas as pd
import numpy as np
import os
import datetime
from datetime import timedelta
from pathlib import Path

#Selecionando as Variáveis
ano_dt_base = 2020
tx_juros = 0.06
cres_sal = 0.01
cres_benef = 0.01

#Importando as bases
bd_ativos = pd.read_csv(str(Path(os.getcwd())) + '\\1.SERVIDORES.csv', encoding='UTF-8', sep=';')#, thousands=',')

#Convertendo os dados para float
bd_ativos['DT_NASC_SERVIDOR'] = pd.to_datetime(bd_ativos['DT_NASC_SERVIDOR'], yearfirst=True, format='%d/%m/%Y')
bd_ativos['DT_ING_ENTE'] = pd.to_datetime(bd_ativos['DT_ING_ENTE'], yearfirst=True, format='%d/%m/%Y')
bd_ativos['DT_ING_CARGO'] = pd.to_datetime(bd_ativos['DT_ING_ENTE'], yearfirst=True, format='%d/%m/%Y')
bd_ativos['VL_BASE_CALCULO'] = bd_ativos['VL_BASE_CALCULO'].str.replace(',', '.').astype(float)
bd_ativos['DT_NASC_CONJUGE'] = pd.to_datetime(bd_ativos['DT_NASC_CONJUGE'], yearfirst=True, format='%d/%m/%Y')
bd_ativos['DT_NASC_NOVO'] = pd.to_datetime(bd_ativos['DT_NASC_NOVO'], yearfirst=True, format='%d/%m/%Y')

print(bd_ativos)