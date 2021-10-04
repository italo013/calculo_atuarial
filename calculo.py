#Importando Bibliotecas
import pandas as pd
import numpy as np
import os
from pathlib import Path

#---------------------------------------------------------------------------------------------------------------------------------------------------------#

#Selecionando as Variáveis
tabua_mortalidade = 'AMERICAN EXPERIENCE'
tabua_mortalidade_inv = 'RRB-44'
tabua_entrada_inv = 'ALVARO VINDAS'
tabua_morbidez = 'Atuários Ingleses'
tx_juros = 0.06
cres_sal = 0.01
cres_benef = 0.01

#---------------------------------------------------------------------------------------------------------------------------------------------------------#

#Importando as tábuas com os qx
qx_morta = pd.read_csv(str(Path(os.getcwd())) + '\\Tábuas\\tb_mortalidade.csv', encoding='UTF-8', sep=';', usecols=[tabua_mortalidade])
qx_morta_inv = pd.read_csv(str(Path(os.getcwd())) + '\\Tábuas\\tb_mortalidade_inv.csv', encoding='UTF-8', sep=';', usecols=[tabua_mortalidade_inv])
qx_entrada_inv = pd.read_csv(str(Path(os.getcwd())) + '\\Tábuas\\tb_entrada_inv.csv', encoding='UTF-8', sep=';', usecols=[tabua_entrada_inv])
qx_morbidez = pd.read_csv(str(Path(os.getcwd())) + '\\Tábuas\\tb_morbidez.csv', encoding='UTF-8', sep=';', usecols=[tabua_morbidez])

#Calculando os px
px_morta = (1 - qx_morta)
px_morta_inv = (1 - qx_morta_inv)
px_entrada_inv = (1 - qx_entrada_inv)
px_morbidez = (1 - qx_morbidez)

#Calculando os dx e lx
dx_morta = pd.DataFrame(columns=px_morta.columns)
dx_morta_inv = pd.DataFrame(columns=px_morta_inv.columns)
dx_entrada_inv = pd.DataFrame(columns=px_entrada_inv.columns)
dx_morbidez = pd.DataFrame(columns=px_morbidez.columns)

lx_morta = pd.DataFrame(columns=px_morta.columns)
lx_morta_inv = pd.DataFrame(columns=px_morta_inv.columns)
lx_entrada_inv = pd.DataFrame(columns=px_entrada_inv.columns)
lx_morbidez = pd.DataFrame(columns=px_morbidez.columns)

for c in range(127):
    if c >= 1:
        lx_morta.loc[c] = lx_morta.loc[c-1] - dx_morta.loc[c-1]
        lx_morta_inv.loc[c] = lx_morta_inv.loc[c-1] - dx_morta_inv.loc[c-1]
        lx_entrada_inv.loc[c] = lx_entrada_inv.loc[c-1] - dx_entrada_inv.loc[c-1]
        lx_morbidez.loc[c] = lx_morbidez.loc[c-1] - dx_morbidez.loc[c-1]

        dx_morta.loc[c] = lx_morta.loc[c] * qx_morta.loc[c]
        dx_morta_inv.loc[c] = lx_morta_inv.loc[c] * qx_morta_inv.loc[c]
        dx_entrada_inv.loc[c] = lx_entrada_inv.loc[c] * qx_entrada_inv.loc[c]
        dx_morbidez.loc[c] = lx_morbidez.loc[c] * qx_morbidez.loc[c]

    else:
        lx_morta.loc[c] = 100000
        lx_morta_inv.loc[c] = 100000
        lx_entrada_inv.loc[c] = 100000
        lx_morbidez.loc[c] = 100000

        dx_morta.loc[c] = lx_morta.loc[c] * qx_morta.loc[c]
        dx_morta_inv.loc[c] = lx_morta_inv.loc[c] * qx_morta_inv.loc[c]
        dx_entrada_inv.loc[c] = lx_entrada_inv.loc[c] * qx_entrada_inv.loc[c]
        dx_morbidez.loc[c] = lx_morbidez.loc[c] * qx_morbidez.loc[c]

#Calculando as Comutação do Dx
Dx_morta = pd.DataFrame(columns=px_morta.columns)

for c in range(127):
    Dx_morta.loc[c] = lx_morta.loc[c]/(1+tx_juros)**c

#Calculando a Comutação do Nx
Nx_morta = pd.DataFrame(columns=px_morta.columns)

for c in range(127):
    Nx_morta.loc[c] = Dx_morta.loc[c:].sum()

#---------------------------------------------------------------------------------------------------------------------------------------------------------#
 
#Calculando as ANUIDADES
#Selecionando as Variáveis
x = 25 #Idade
n = 20 #Temporariedade
k = 20 #Diferimento

#äx = Nx/Dx
ax_ant = Nx_morta.loc[x]/Dx_morta.loc[x]

print(ax_ant)
print('FINALIZADO!!!')
