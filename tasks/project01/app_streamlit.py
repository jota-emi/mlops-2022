'''
Autor: João Marcos Viana
Data: Maio 2022
Este projeto tem o objetivo de analisar dois conjuntos
de dados que apresentam os valores mês a mês da cesta básica
de alimentos e também do salário mínimo no Brasil, afim de
criar uma relação entre essas duas variáveis.
Dessa forma, foram gerados alguns gráficos que apresentam
a relação de quantos por cento do salário
mínimo é comprometido somente com o valor da cesta básica.
'''

import logging
from datetime import datetime
import pandas as pd
from matplotlib import style
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path

cesta_basica_csv = Path(__file__).parents[1] / 'cesta_basica.csv'
salario_minimo_csv = Path(__file__).parents[1] / 'salario_minimo.csv'



# configurando o logging
logging.basicConfig(
    filename='./results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')


def read_data(file_path):
    """Read data from csv.

    Args:
        file_path (str): file path to read.

    Return:
        df_file (DataFrame): returns the file read as a dataframe.
    """
    try:
        df_file = pd.read_csv(file_path)
        logging.info("SUCCESS : File %s is read without erros", file_path)
        return df_file
    except FileNotFoundError:
        logging.error("ERROR : There's no such %s", file_path)
        return None


def apply_datetime(df_file, date_column, original_format):
    """Transform the column that contains date
    to datetime format.

    Args:
        df_file (DataFrame): df that will be transformed.
        date_column (str): column name that contains date.
        original_format (str): date format in original dataset
                               this has to be informed to conversion

    Return:
        df_after (DataFrame): returns the new dataframe with the data
                             labels in correctly format.
    """
    try:
        df_after = df_file.copy()
        df_after[date_column] = pd.to_datetime(
            df_after[date_column], format=original_format)

        df_after[date_column] = df_after[date_column].dt.date

        df_after.sort_values(date_column, inplace=True)
        df_after.reset_index(drop=True, inplace=True)
        logging.info("SUCCESS : Datetime conversion is executed without erros")
        return df_after
    except: # pylint: disable=bare-except
        logging.error("ERROR : Datetime conversion not work")
        return None


# Cleaning Datasets
# Salario minimo
salario_minimo = read_data('https://raw.githubusercontent.com/jota-emi/mlops-2022/main/tasks/project01/salario_minimo.csv')
salario_minimo.rename(columns={
    'Salário mínimo vigente - R$ - ' +
    'Ministério da Economia- Outras (Min- Economia/Outras) - MTE12_SALMIN12': 'Salario_minimo',
},
    inplace=True)

salario_minimo = salario_minimo.drop(columns=['Unnamed: 2'])
salario_minimo = apply_datetime(salario_minimo, 'Data', '%Y-%m')

# Cesta básica
cesta_basica = read_data('https://raw.githubusercontent.com/jota-emi/mlops-2022/main/tasks/project01/cesta_basica.csv')
cesta_basica.rename(columns={'Gasto Mensal - Total da Cesta': 'Data',
                             },
                    inplace=True)
cesta_basica = cesta_basica.drop(columns=['Brasília', 'Campo Grande',	'Cuiabá',
                                          'Belo Horizonte', 'Boa Vista', 'Macapá',
                                          'Manaus',	'Palmas', 'Porto Velho', 'Rio Branco',
                                          'Maceió', 'São Luís',	'Teresina',	'Macaé'])
cesta_basica['Media_Brasil'] = (
    cesta_basica.iloc[0:, 1:].mean(axis=1)).round(2)
cesta_basica = apply_datetime(cesta_basica, 'Data', '%m-%Y')

# Merge Datasets
salario_cesta = pd.merge(salario_minimo, cesta_basica, how='outer')
salario_cesta['Data'] = pd.to_datetime(cesta_basica['Data'])
salario_cesta['Salario_Cesta'] = salario_cesta['Media_Brasil'] / \
    salario_cesta['Salario_minimo']

# Analise Exploratoria
plt.plot(salario_cesta['Data'], salario_cesta['Media_Brasil']/salario_cesta['Salario_minimo'])
#plt.savefig('salario_cesta_exploratorio.png', format='png')
# plt.show()

# Analise Explanatória
lula = salario_cesta.copy(
)[salario_cesta['Data'].dt.year < 2011]
dilmatemer = salario_cesta.copy(
)[(salario_cesta['Data'].dt.year >= 2011) & (salario_cesta['Data'].dt.year < 2019)]
bolso = salario_cesta.copy(
)[(salario_cesta['Data'].dt.year >= 2019) & (salario_cesta['Data'].dt.year <= 2022)]

dilma = dilmatemer.copy(
)[dilmatemer['Data'] < datetime.strptime('2016-09-01', '%Y-%m-%d')]
temer = dilmatemer.copy(
)[dilmatemer['Data'] >= datetime.strptime('2016-09-01', '%Y-%m-%d')]

# Adding the FiveThirtyEight style
style.use('fivethirtyeight')

# Adding the subplots
fig = plt.figure(figsize=(12, 8))
ax1 = plt.subplot(2, 3, 1)
ax2 = plt.subplot(2, 3, 2)
ax3 = plt.subplot(2, 3, 3)
ax4 = plt.subplot(2, 1, 2)
axes = [ax1, ax2, ax3, ax4]

# Changes to all the subplots
for ax in axes:
    ax.set_ylim(0.3, 0.9)
    ax.set_yticks([0.4, 0.5, 0.6, 0.8])
    ax.set_yticklabels(['40%', '50%', '60%', '70%'],
                       alpha=0.3)
    ax.grid(alpha=0.5)


### Ax1: Lula
ax1.plot(lula['Data'], lula['Salario_Cesta'],
         color='#CC0000')
ax1.set_xticks([datetime.strptime('2002-07-01', '%Y-%m-%d'),
                datetime.strptime('2003-01-01', '%Y-%m-%d'),
                datetime.strptime('2004-01-01', '%Y-%m-%d'),
                datetime.strptime('2005-01-01', '%Y-%m-%d'),
                datetime.strptime('2006-01-01', '%Y-%m-%d'),
                datetime.strptime('2007-01-01', '%Y-%m-%d'),
                datetime.strptime('2008-01-01', '%Y-%m-%d'),
                datetime.strptime('2009-01-01', '%Y-%m-%d'),
                datetime.strptime('2010-01-01', '%Y-%m-%d'),
                datetime.strptime('2011-01-01', '%Y-%m-%d'), ])
ax1.set_xticklabels(['', '2003', '', '2005', '', '2007', '',
                     '2009', '', '2011'],
                    alpha=0.3)
ax1.text(13080.0, 0.95, 'LULA', fontsize=18, weight='bold',
          color='#CC0000')
ax1.text(12780.0, 0.9, '[2003-2010]', weight='bold',
          alpha=0.3)

### Ax2: Dilma/Temer
ax2.plot(dilma['Data'], dilma['Salario_Cesta'],
         color='#dd8800')
ax2.plot(temer['Data'], temer['Salario_Cesta'],
         color='#006400')
ax2.set_xticks([datetime.strptime('2010-07-01', '%Y-%m-%d'),
                datetime.strptime('2011-01-01', '%Y-%m-%d'),
                datetime.strptime('2012-01-01', '%Y-%m-%d'),
                datetime.strptime('2013-01-01', '%Y-%m-%d'),
                datetime.strptime('2014-01-01', '%Y-%m-%d'),
                datetime.strptime('2015-01-01', '%Y-%m-%d'),
                datetime.strptime('2016-01-01', '%Y-%m-%d'),
                datetime.strptime('2017-01-01', '%Y-%m-%d'),
                datetime.strptime('2018-01-01', '%Y-%m-%d'),
                datetime.strptime('2019-01-01', '%Y-%m-%d'), ])
ax2.set_xticklabels(['', '2011', '', '2013', '', '2015', '',
                     '2017', '', '2019'],
                   alpha=0.3)
ax2.text(14750.0, 0.95, 'DILMA', fontsize=18, weight='bold',
          color='#dd8800')
ax2.text(17100.0, 0.95, 'TEMER', fontsize=18, weight='bold',
         color='#006400')
ax2.text(14500, 0.9, '[2011-2016]', weight='bold',
         alpha=0.3)
ax2.text(16900.0, 0.9, '[2016-2018]', weight='bold',
         alpha=0.3)


### Ax3: Bolsonaro
ax3.plot(bolso['Data'], bolso['Salario_Cesta'],
         color='#0404b6')
ax3.set_xticks([datetime.strptime('2019-01-01', '%Y-%m-%d'),
                datetime.strptime('2019-07-01', '%Y-%m-%d'),
                datetime.strptime('2020-01-01', '%Y-%m-%d'),
                datetime.strptime('2020-07-01', '%Y-%m-%d'),
                datetime.strptime('2021-01-01', '%Y-%m-%d'),
                datetime.strptime('2021-07-01', '%Y-%m-%d'),
                datetime.strptime('2022-01-01', '%Y-%m-%d')])
ax3.set_xticklabels(['2019', '', '2020', '', '2021', '', '2022'],
                    alpha=0.3)
ax3.text(18200.0, 0.95, 'BOLSONARO', fontsize=18, weight='bold',
          color='#0404b6')
ax3.text(18300.0, 0.9, '[2019-2022]', weight='bold',
         alpha=0.3)

### Ax4: Lula-Dilma-Temer-Bolsonaro
ax4.plot(lula['Data'], lula['Salario_Cesta'],
         color='#CC0000')
ax4.plot(dilma['Data'], dilma['Salario_Cesta'],
         color='#dd8800')
ax4.plot(temer['Data'], temer['Salario_Cesta'],
         color='#006400')
ax4.plot(bolso['Data'], bolso['Salario_Cesta'],
         color='#0404b6')
ax4.grid(alpha=0.5)
ax4.set_xticks([])

# Adding a title and a subtitle
ax1.text(11500.0, 1.20, 'Valor da cesta básica no Brasil chega a 56% ' +
          'do salário mínimo pela \nprimeira vez desde 2005',
          fontsize=20, weight='bold')
ax1.text(11500.0, 1.11, 'Histórico mostra os preços da cesta básica em relação ' +
         'aos salários mínimos ao longo dos últimos governos',
         fontsize=14)

# # Adding a signature
ax4.text(11500.0, 0.22, 'Autor: João Marcos Viana' + ' '*115 + 'Fonte: DIESSE',
          color='#f0f0f0', backgroundcolor='#4d4d4d',
          size=14)

#plt.savefig('salario_cesta_governos.png', format='png')
# plt.show()



st.sidebar.title("Menu")
paginaSelecionada = st.sidebar.selectbox("Selecione a página", ['Página Inicial', 'Sobre'])

if paginaSelecionada == 'Página Inicial':
    st.title("Projeto 01 - MLOps")
    st.markdown("## Comparativo dos preços da cesta básica ao longo dos últimos governos")
    st.pyplot(fig)
elif paginaSelecionada == 'Sobre':
    st.title("Projeto 01 - MLOps")
    st.markdown("### Projeto desenvolvido por João Marcos Viana - UFRN")
