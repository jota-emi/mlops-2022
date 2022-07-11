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


## Passo 1 - ETL/EDA
### Download raw_data.csv
Durante a primeira etapa devemos disponibilizar o dado bruto no Wandb, que é a ferramenta capaz de rastrear rapidamente os experimentos, controlar o versionamento e iterações em conjuntos de dados. Com isso, iremos gerar assim o primeiro artefato.

Para conseguir realizar esta etapa foi feita a configuração do arquivo [MLproject](https://github.com/jota-emi/mlops-2022/blob/main/tasks/project/etl_eda/MLproject), responsáve

### Preprocessamento
### EDA

## Passo 2 - Checagem dos dados
## Passo 3 - Segregação

## Conclusão