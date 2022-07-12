# Construindo um pipeline para ETL, checagem e segregação de dados

Neste projeto, o objetivo é aplicar as habilidades adquiridas durante a semana 8 do curso de [MLOps](https://github.com/ivanovitchm/mlops) ministrado pelo professor Ivanovitch Medeiros na Universidade Federal do Rio Grande do Norte, visando desenvolver as primeiras três etapas da produção de um modelo de regressão para previsão do preço de alugueis do Airbnb na cidade do Rio de Janeiro. Dados disponibilizados pelo professor publicamente através deste [link](https://drive.google.com/file/d/16zF4MHEP_bBxAEWpQgVocPupTjRRAgfP/view?usp=sharing).

## Principais ferramentas utilizadas
- Pandas
- Weights&Biases
- Dataprep
- MLFlow
- Conda
- Pytest

## Pipeline
A construção do pipeline de dados foi feita através da utilização de diversas ferramentas que auxiliam no gerenciamento do fluxo de dados. Dentre as ferramentas, destacam-se o MLFlow e o Weights&Biases (Wandb). O MLFlow é uma plataforma para otimizar todo o processo de desenvolvimento de modelos de aprendizado de máquina, gerenciando de ponta a ponta o fluxo, incluindo rastreamento de experimentos, empacotamento de código em execuções reproduzíveis, compartilhamento e implantação de modelos. Enquanto isso, o Wandb é o responsável pelo rastreamento dos experimentos, além de realizar o controle de versionamento de conjuntos de dados.

Para cada etapa do pipeline teremos alguns arquivos de configuração, são eles "enviroment.yml" que lista as dependencias necessárias para a execução daquela tarefa e o ambiente conda consegue ser montado a partir dele. Existem também os arquivos "MLproject", que são responsáveis pela configuração da execução do MLFlow, nele onde são definidos o nome do projeto que será criado no Wandb para cada artefato, os parâmetros necessários e também o comando que será rodado para executar.

O modelo idealizado de arquitetura do pipeline pode ser visualizado na imagem abaixo, disponibilizado também pelo professor no [repositório](https://github.com/ivanovitchm/mlops).

[<img src="https://github.com/jota-emi/mlops-2022/blob/main/tasks/project/images/pipeline.PNG?raw=true">](http://google.com.au/)

Através de sua interface web, o Wandb possui também uma forma de visualização e organização que nos permite visualizar a linearidade obtida durante todo o fluxo dos dados. Nos proporcionando assim uma visão geral de como ficou o pipeline ao final das etapas. Podemos ver o resultado final obtido na imagem abaixo.

[<img src="https://github.com/jota-emi/mlops-2022/blob/main/tasks/project/images/wandb.PNG?raw=true">](http://google.com.au/)

## Passo 1 - ETL/EDA
### Download raw_data.csv
Durante a primeira etapa devemos disponibilizar o dado bruto no Wandb, que é a ferramenta capaz de rastrear rapidamente os experimentos, controlar o versionamento e iterações em conjuntos de dados. Com isso, iremos gerar assim o primeiro artefato.

Juntamente com os arquivos de configuração "enviroment.yml" e "MLproject", foi criado o arquivo python em si, capaz de realizar a leitura do arquivo .csv original e criar a conexão com Wandb, gerando o artefato chamado "raw_data.csv", que simplesmente contém os dados brutos do dataset do Airbnb.
OBS: Como foi aproveitado esse primeiro momento para já fazer também uma análise exploratória dos dados, o arquivo .py foi substituído por um .ipynb. 

### Preprocessamento
Na sequência, ainda dentro do escopo do ETL, foram realizadas diversas transformações nos dados iniciais. Tais transformações se fazem necessárias devido a atributos e características do dataset. Seja retirando colunas/dados que não são importantes para o objetivo em questão, que é prever o preço do aluguel de casas, ou mesmo ajustando os tipos de determinado dado, realizando limpezas, tratando dados faltantes, entre outras transformações.
Toda a configuração necessária para esse passo foi também realizada pelos arquivos de configuração e do arquivo .py, onde as transformações foram feitas efetivamente através da biblioteca pandas. Ao final, também foi gerado um novo artefato que continha agora um dataset mais limpo, a princípio pronto para o uso. Este novo artefato foi chamado de clean_data.csv.

### EDA
Tanto antes quanto após a etapa de preprocessamento do dataset, foram realizadas análises em todos os aspectos do dataset, com o objetivo de proporcionar ao desenvolvedor um panorama dos dados e do problema em questão. Nesta etapa foi utilizada a ferramenta Dataprep, uma biblioteca que visa automatizar a geração de gráficos, dados estatísticos e qualquer análise de caráter exploratório na base de dados. Com a ajuda desta ferramenta que foi facilitado o entendimento de quais colunas provavelmente serão mais ou menos importantes dentro do contexto de predição de preços, por exemplo. Assim, as necessidades de transformações foram identificadas e aplicadas na etapa de preprocessamento.

## Passo 2 - Checagem dos dados
Nessa etapa, realizamos algumas verificações nos dados, que podem ser de caráter deterministico ou não, e que servem para assegurar que seus tipos estejam corretos, que os valores estejam condizentes com o esperado, entre outras possibilidades. Isso foi feito através de duas funções python no arquivo teste_data.py.

Além dos arquivos padrões de configuração, nesta etapa fez-se necessária também a criação de um arquivo "conftest.py", responsável por iniciar o projeto no Wandb e criar uma fixture que define qual o dado que será passado como parâmetro nas funções de teste. Utilizou-se a biblioteca pytest para realizar os testes.

## Passo 3 - Segregação
Após garantirmos que os dados estão prontos para serem utilizados em produção, é hora de realizar a divisão dos dados em dados de treinamento e dados de teste. Para isso, foi utilizada a função train_test_split da biblioteca do sklearn. A proporção desta divisão, assim como outros parâmetros são determinados pelo usuário no momento da chamada do mlflow.
Ao final desta etapa, dois novos artefatos serão gerados no Wandb, eles foram chamados de "test_data.csv" e "train_data.csv".

### Link do vídeo explicativo
[Video]()