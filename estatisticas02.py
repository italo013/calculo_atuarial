#Importando Bibliotecas
import pandas as pd
import numpy as np
import os
import datetime
from datetime import timedelta
from pathlib import Path

########################################################################################################################################################################################################################################################
###############################################################################################################Selecionando as Variáveis################################################################################################################
########################################################################################################################################################################################################################################################

#Selecionando as Variáveis
ano_dt_base = 2020
tx_juros = 0.06
cres_sal = 0.01
cres_benef = 0.01

########################################################################################################################################################################################################################################################
########################################################################################################################################################################################################################################################

#Importando as bases
bd_ativos = pd.read_csv(str(Path(os.getcwd())) + '\\1.SERVIDORES.csv', encoding='UTF-8', sep=';')#, thousands=',')

#Convertendo os dados para float
bd_ativos['DT_NASC_SERVIDOR'] = pd.to_datetime(bd_ativos['DT_NASC_SERVIDOR'], yearfirst=True, format='%d/%m/%Y')
bd_ativos['DT_ING_ENTE'] = pd.to_datetime(bd_ativos['DT_ING_ENTE'], yearfirst=True, format='%d/%m/%Y')
bd_ativos['DT_ING_CARGO'] = pd.to_datetime(bd_ativos['DT_ING_ENTE'], yearfirst=True, format='%d/%m/%Y')
bd_ativos['VL_BASE_CALCULO'] = bd_ativos['VL_BASE_CALCULO'].str.replace(',', '.').astype(float)
bd_ativos['DT_NASC_CONJUGE'] = pd.to_datetime(bd_ativos['DT_NASC_CONJUGE'], yearfirst=True, format='%d/%m/%Y')
bd_ativos['DT_NASC_NOVO'] = pd.to_datetime(bd_ativos['DT_NASC_NOVO'], yearfirst=True, format='%d/%m/%Y')
bd_ativos['DT_NASC_INV'] = pd.to_datetime(bd_ativos['DT_NASC_INV'], yearfirst=True, format='%d/%m/%Y')

bd_ativos['DT_BASE'] = '31/12/2020'
bd_ativos['DT_BASE'] = pd.to_datetime(bd_ativos.DT_BASE, yearfirst=True, format='%d/%m/%Y')

########################################################################################################################################################################################################################################################
########################################################################################################################################################################################################################################################

#Calculando as Estatísticas dos Ativos
statis_ativos = pd.DataFrame()

statis_ativos['IDADE_SERVIDOR'] = round((bd_ativos.DT_BASE - bd_ativos.DT_NASC_SERVIDOR) / timedelta(days=365.25) - 0.5).astype(int) #Data-Base - Data de Nascimento do Servidor
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
statis_ativos['IDADE_ADM'] = round((bd_ativos.DT_ING_ENTE - bd_ativos.DT_NASC_SERVIDOR) / timedelta(days=365.25) - 0.5).astype(int) #Data de Ingresso no Ente - Data de Nascimento do Servidor
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
statis_ativos['IDADE_CONJUGE'] = bd_ativos.DT_NASC_CONJUGE.mask(bd_ativos.DT_NASC_CONJUGE.isnull(), '1800-01-01', axis=0)#, inplace=True) #Preenchendo as linhas vazias com alguma data
statis_ativos.IDADE_CONJUGE = round((bd_ativos.DT_BASE - statis_ativos.IDADE_CONJUGE) / timedelta(days=365.25) - 0.5).astype(int) #Calculando as Idades dos Cônjuges | Data-Base - Data de Nascimento do Cônjuge
statis_ativos.loc[(bd_ativos.CO_EST_CIVIL_SERVIDOR == 1) | (bd_ativos.CO_EST_CIVIL_SERVIDOR == 3) | (bd_ativos.CO_EST_CIVIL_SERVIDOR == 4) | (bd_ativos.CO_EST_CIVIL_SERVIDOR == 5) | (statis_ativos.IDADE_CONJUGE > 127), 'IDADE_CONJUGE'] = None #Removendo as datas inseridas
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
statis_ativos['IDADE_EMT'] = round(statis_ativos.IDADE_ADM - (bd_ativos['NU_TEMPO_RGPS']/365.25)) #Calculando a Idade de Entrada no Mercado de Trabalho | Idade de Admissão - (TSANT/365.25)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
statis_ativos['DIF_ETARIA'] = statis_ativos.IDADE_CONJUGE - statis_ativos.IDADE_SERVIDOR #Calculando a Diferença Etária do Cônjuge | Idade do Cônjuge - Idade do Servidor
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
statis_ativos['IDADE_NOVO'] = bd_ativos.DT_NASC_NOVO.mask(bd_ativos.DT_NASC_NOVO.isnull(), '1800-01-01', axis=0)#, inplace=True) #Preenchendo as linhas vazias com alguma data
statis_ativos.IDADE_NOVO = round((bd_ativos.DT_BASE - statis_ativos.IDADE_NOVO) / timedelta(days=365.25) - 0.5).astype(int) #Calculando as Idades do Filho Mais Novo | Data-Base - Data de Nascimento do Filho Mais Novo
statis_ativos.loc[statis_ativos.IDADE_NOVO > 21, 'IDADE_NOVO'] = None #Removendo as datas inseridas
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
statis_ativos['IDADE_INV'] = bd_ativos.DT_NASC_INV.mask(bd_ativos.DT_NASC_INV.isnull(), '1800-01-01', axis=0)#, inplace=True) #Preenchendo as linhas vazias com alguma data
statis_ativos.IDADE_INV = round((bd_ativos.DT_BASE - statis_ativos.IDADE_INV) / timedelta(days=365.25) - 0.5).astype(int) #Calculando as Idades do Filho Inválido | Data-Base - Data de Nascimento do Filho Inválido
statis_ativos.loc[statis_ativos.IDADE_INV > 127, 'IDADE_INV'] = None #Removendo as datas inseridas
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
statis_ativos['TP_PREFEITURA'] = statis_ativos.IDADE_SERVIDOR - statis_ativos.IDADE_ADM #Calculando o Tempo de Prefeitura | Idade do Servidor - Idade de Admissão
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
statis_ativos['DIFERIMENTO'] = bd_ativos.DT_PROV_APOSENT - statis_ativos.IDADE_SERVIDOR #Calculando o Diferimento até a Aposentadoria | Idade Provável de Aposentadoria - Idade do Servidor
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
statis_ativos['BENEF_PROJ'] = round(bd_ativos.VL_BASE_CALCULO * (1 + cres_sal)**statis_ativos.DIFERIMENTO, 2)

#Projeção do Crescimento Salarial (Benefício de Aposentadoria Projetado)
proj_cres_sal = []
for l in range(len(bd_ativos)):
    linha = []
    for c in range(statis_ativos.DIFERIMENTO[l]+1):
        benef_proj = round(bd_ativos.VL_BASE_CALCULO.loc[l] * ((1 + cres_sal)**c), 2)
        linha.append(benef_proj)
    proj_cres_sal.append(linha)

df_benef_proj = pd.DataFrame(data=proj_cres_sal, index=bd_ativos.ID_SERVIDOR_MATRICULA)