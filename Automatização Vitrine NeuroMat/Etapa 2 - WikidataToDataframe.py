# Etapa 2 - Extração 
# Atenção! É necessário ter um dataframe nesse diretório chamado "df_wikidata.csv" para aplicar o script abaixo
# Ao final deste script, será gerado um novo dataframe (df_altmetric.csv) com os valores escolhidos na metodologia

import requests
import pandas as pd

# Nome do arquivo CSV de entrada
csv_file = "df_wikidata.csv"

# Carregar o CSV
df = pd.read_csv(csv_file, delimiter=",")  # Ajuste para CSV com delimitador ponto e vírgula

# Verificar se a coluna "doi" existe
if "doi" not in df.columns:
    raise ValueError("A coluna 'doi' não foi encontrada no arquivo CSV.")

# Lista de DOIs extraída do CSV
dois_list = df["doi"].dropna().tolist()

# URL base da API Altmetric
api_url = "https://api.altmetric.com/v1/doi/"

# Dicionário para armazenar os resultados
dados_altmetric = {
    "doi_score": [],
    "readers_count": [],
    "cited_by_tweeters_count": [],
    "cited_by_accounts_count": [],
    "cited_by_posts_count": [],
    "cited_by_msm_count": [],
    "cited_by_feeds_count": [],
    "cited_by_fbwalls_count": [],
    "cited_by_gplus_count": [],
    "cited_by_videos_count": [],
    "cited_by_rdts": [],
    "arxiv_id": [],
    "pmid": [],
    "cited_by_wikipedia_count": []
}

for doi in dois_list:
    response = requests.get(api_url + doi)

    if response.status_code == 200:
        data = response.json()
        score = data.get("score")
        dados_altmetric["doi_score"].append(round(score, 2) if isinstance(score, (int, float)) else "Sem score disponível")
        dados_altmetric["readers_count"].append(data.get("readers_count", 0))
        dados_altmetric["cited_by_tweeters_count"].append(data.get("cited_by_tweeters_count",0))
        dados_altmetric["cited_by_accounts_count"].append(data.get("cited_by_accounts_count", 0))
        dados_altmetric["cited_by_posts_count"].append(data.get("cited_by_posts_count", 0))
        dados_altmetric["cited_by_msm_count"].append(data.get("cited_by_msm_count", 0))
        dados_altmetric["cited_by_feeds_count"].append(data.get("cited_by_feeds_count", 0))
        dados_altmetric["cited_by_fbwalls_count"].append(data.get("cited_by_fbwalls_count", 0))
        dados_altmetric["cited_by_gplus_count"].append(data.get("cited_by_gplus_count", 0))
        dados_altmetric["cited_by_videos_count"].append(data.get("cited_by_videos_count", 0))
        dados_altmetric["cited_by_rdts"].append(data.get("cited_by_rdts", 0))
        dados_altmetric["arxiv_id"].append(data.get("arxiv_id", 0))
        dados_altmetric["pmid"].append(data.get("pmid", 0))
        dados_altmetric["cited_by_wikipedia_count"].append(data.get("cited_by_wikipedia_count",0))

    elif response.status_code == 404:
        for key in dados_altmetric:
            dados_altmetric[key].append(0)
    else:
        error_msg = f"Erro {response.status_code}"
        for key in dados_altmetric:
            dados_altmetric[key].append(error_msg)

# Adicionar os resultados ao DataFrame
for key, values in dados_altmetric.items():
    df[key] = values

# Salvar como CSV com delimitador ";"
output_file = "df_altmetric.csv"
df.to_csv(output_file, index=False, sep=";")

print(f"Arquivo salvo como {output_file} com delimitador ';'")
