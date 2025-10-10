# Execução dos scripts fora do Flask

Este documento é uma ajuda para rodar os scripts fora do Flask.  
A metodologia proposta nesse repositório está intrinsecamente relacionada ao framework Flask.  
Porém, o passo a passo para executar essa metodologia fora do Flask fica a critério do usuário.  

Sugerimos o uso de ferramentas interativas, como **notebooks baseados em Python**, que permitem a execução sequencial do código e a visualização imediata dos resultados.

É necessário, então, que, pelo menos, as três etapas iniciais sejam executadas nessas ferramentas.

---

## Etapa 1 - Coleta da produção científica

Nesta etapa, ocorre a **coleta da produção científica do NeuroMat a partir do Wikidata**, utilizando consultas **SPARQL**.  
O objetivo é gerar um  arquivo *.csv* com os dados de publicações, autores, instituições e demais metadados disponíveis na Wikidata Query Service.

1. Utilize o script em SPARQL que coleta a produção científica do NeuroMat, alterando as propriedades conforme necessário.

2. Utilize uma biblioteca Python como `requests` ou `SPARQLWrapper` para enviar a query ao [endpoint].
  > Este endpoint é utilizado devido à separação do grafo principal do Wikidata (Wikidata Graph Split), garantindo a disponibilidade de dados científicos.

3. Salve o resultado em formato .csv no diretório da ferramenta.

5. Confirme se o arquivo gerado contém as colunas essenciais (item, title, authorLabel, publicationDate, etc.), pois ele servirá como entrada para a Etapa 2.

## Etapa 2 - Extração altmétrica

Nessa fase, os dados coletados no Wikdiata serão enriquecidos com informações provenientes da API da Altmetric.
1. Execute o script.
  > Após gerar o dataframe da **Etapa 1**, é necessário aplicar o [[Script 2 (extração altmétrica)]] diretamente sobre esse DataFrame.  Esse script já possui todas os comandos necessário, **é necessário somente ter o arquivo df_wikidata.csv no mesmo diretório**.
> Após o script ser executado, será gerado um dataframe chamado **df_altmetric.csv**.

## Etapa 3 - Reconciliação de dados
1. Execute o script para reconciliar os dados do arquivo gerado na etapa anterior.


