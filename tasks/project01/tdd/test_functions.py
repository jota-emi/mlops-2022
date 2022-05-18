'''
Autor: João Marcos Viana
Data: Maio 2022
Arquivo de teste para usar o pytest.
'''
# importando bibliotecas
import pandas as pd
import datetime
from cesta_salario_functions import read_data, apply_datetime

def test_read_data():
    file = read_data("../cesta_basica.csv")
    assert type(file) == pd.core.frame.DataFrame

def test_apply_datetime():
    salario_minimo = read_data('../salario_minimo.csv')
    salario_minimo = apply_datetime(salario_minimo, 'Data', '%Y-%m')
    assert type(salario_minimo['Data'][0]) == datetime.date