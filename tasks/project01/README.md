## Projeto 01 - Storytelling Data Visualization

Este projeto foi inspirado pelo projeto guiado "Storytelling Data Visualization on Exchange Rates" do curso de Data Scientist in Python na plataforma Dataquest.io.

O objetivo do trabalho foi explorar as habilidades adquiridas ao longo de toda a Unidade 01 da disciplina de MLOps na UFRN, lecionada pelo professor Ivanovitch Medeiros, como código limpo, documentação, refatoração, uso de ferramentas de análise de qualidade do código, testes, logging, captura e manipulação de erros. Tudo isso dentro do contexto de Ciência de Dados.

Com isso, foi desenvolvida a análise da evolução dos preços da cesta básica de alimentos no Brasil, em comparação ao preço do salário-mínimo vigente. As bases de dados utilizadas foram disponibilizadas pelo DIEESE (Departamento Intersindical de Estatística e Estudos Socioeconômicos).
Tratando-se de duas bases de dados diferentes, uma com os valores mês a mês da cesta básica e outro com os valores mensais do salário-mínimo vigente, foi necessária também a utilização de algumas técnicas de limpeza tratamento de dados para que fosse possível extrair apenas os valores de interesse do escopo do trabalho.

O resultado da análise pode ser visualizado através do gráfico desenvolvido, contendo o comparativo da relação de preços cesta básica / salário-mínimo ao longo dos últimos governos brasileiros. O gráfico está disponível no seguinte [dashboard] (https://share.streamlit.io/jota-emi/mlops-2022/main/tasks/project01/app_streamlit.py), assim como na imagem abaixo:

### Ferramentas Utilizadas
- pandas
- matplotlib
- streamlit
- logging
- pytest
- pylint
- autopep8