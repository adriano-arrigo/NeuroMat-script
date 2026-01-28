 # __________ EM CONSTRUÇÃO __________

# Execução dos scripts fora do Flask

Este documento é um documento para executar os scripts do projeto fora do Flask, embora a metodologia proposta nesse repositório está intrinsecamente relacionada ao framework Flask, embora seja possível executar este passo a passo fora do ambiente Flask.  

## Pré-requisitos
Sugerimos o uso de ferramentas interativas, como **notebooks baseados em Python** (Google Colab ou Jupyter Notebook), que permitem a execução sequencial do código e a visualização dos resultados.

A partir disso, é necessário, então, que, pelo menos, as três etapas iniciais sejam executadas nessas ferramentas.

---

## Etapa 1 - Coleta da produção científica

Nesta etapa, ocorre a **coleta da produção científica de uma base dados no Wikidata**, (no caso aqui, a base do Cepid NeuroMat) utilizando consultas **SPARQL** concentradasso script 1.
O objetivo é gerar um  arquivo *.csv* com os dados de publicações, autores, instituições e demais metadados disponíveis na Wikidata Query Service.

### 1. [Script 1 - Coleta de dados](https://github.com/adriano-arrigo/NeuroMat-script/blob/dd54ced850233d9874ae6bf5f0c496d5c8bafc76/Automatiza%C3%A7%C3%A3o%20Vitrine%20NeuroMat/Etapa%201%20-%20Coletar%20a%20produ%C3%A7%C3%A3o%20cient%C3%ADfica%20do%20NeuroMat%20do%20Wikidata.rq)
* Script em SPARQL responsável pela coleta a produção científica do NeuroMat, alterando as propriedades conforme necessário.
* Esse script utiliza biblioteca Python como `requests` ou `SPARQLWrapper` para enviar a requisão de dados ao endpoint Scholary[^1] do Wikidata.

[^1]: Este endpoint é utilizado devido à separação do grafo principal do Wikidata (Wikidata Graph Split), garantindo a disponibilidade de dados científicos.

3. Salve o resultado em formato *.csv* no diretório da ferramenta.

5. Confirme se o arquivo gerado contém as colunas essenciais (item, title, authorLabel, publicationDate, etc.), pois ele servirá como entrada para a Etapa 2.

## Etapa 2 - Extração altmétrica

Nessa fase, os dados coletados no Wikdiata serão enriquecidos com informações provenientes da API da Altmetric.
1. Execute o script.
  > Esse script já possui todas os comandos necessários, **é necessário somente ter o arquivo df_wikidata.csv no mesmo diretório**.
> Após o script ser executado, será gerado um dataframe chamado **df_altmetric.csv**.

## Etapa 3 - Reconciliação de dados
1. Execute o script para reconciliar os dados do arquivo gerado na etapa anterior.


