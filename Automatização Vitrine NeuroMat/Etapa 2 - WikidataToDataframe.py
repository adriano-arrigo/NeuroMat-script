# Etapa 2 - Extração de dados altmétricos
# Este script lê o arquivo df_wikidata.csv, que deve estar no mesmo diretório.
# O arquivo de entrada deve conter uma coluna chamada "doi".
# Ao final, será gerado o arquivo df_altmetric.csv com os dados retornados pela API Altmetric.

import requests
import pandas as pd
import time

# ==========================================
# Configurações
# ==========================================

csv_file = "df_wikidata.csv"
output_file = "df_altmetric.csv"
# À partir de 2025, é necessário uma chave para consultar a API.
api_url = "https://api.altmetric.com/v1/doi/"
API_KEY = "chave_da_API"

# ==========================================
# Carregar CSV
# ==========================================

df = pd.read_csv(csv_file, delimiter=",")

if "doi" not in df.columns:
    raise ValueError("A coluna 'doi' não foi encontrada no arquivo CSV.")
dois_list = df["doi"].tolist()

# ==========================================
# Estrutura dos resultados
# ==========================================

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


# ==========================================
# Consulta Altmetric
# ==========================================

for doi in dois_list:


    if pd.isna(doi) or str(doi).strip() == "":

        for key in dados_altmetric:
            dados_altmetric[key].append(0)

        continue


    # Remove somente espaços
    # Mantém capitalização original do DOI
    doi = str(doi).strip()


    try:

        response = requests.get(
            api_url + doi,
            params={"key": API_KEY},
            timeout=30
        )


        # DOI encontrado

        if response.status_code == 200:

            data = response.json()
            print(f"{doi} -> {data.get('score')}")

            score = data.get("score", 0)

            dados_altmetric["doi_score"].append(
                round(float(score), 3) if score is not
              None else 0.0
                
            )

            dados_altmetric["readers_count"].append(
                data.get("readers_count", 0)
            )

            dados_altmetric["cited_by_tweeters_count"].append(
                data.get("cited_by_tweeters_count", 0)
            )

            dados_altmetric["cited_by_accounts_count"].append(
                data.get("cited_by_accounts_count", 0)
            )

            dados_altmetric["cited_by_posts_count"].append(
                data.get("cited_by_posts_count", 0)
            )

            dados_altmetric["cited_by_msm_count"].append(
                data.get("cited_by_msm_count", 0)
            )

            dados_altmetric["cited_by_feeds_count"].append(
                data.get("cited_by_feeds_count", 0)
            )

            dados_altmetric["cited_by_fbwalls_count"].append(
                data.get("cited_by_fbwalls_count", 0)
            )

            dados_altmetric["cited_by_gplus_count"].append(
                data.get("cited_by_gplus_count", 0)
            )

            dados_altmetric["cited_by_videos_count"].append(
                data.get("cited_by_videos_count", 0)
            )

            dados_altmetric["cited_by_rdts"].append(
                data.get("cited_by_rdts", 0)
            )

            dados_altmetric["arxiv_id"].append(
                data.get("arxiv_id", 0)
            )

            dados_altmetric["pmid"].append(
                data.get("pmid", 0)
            )

            dados_altmetric["cited_by_wikipedia_count"].append(
                data.get("cited_by_wikipedia_count", 0)
            )


        # DOI não encontrado na Altmetric

        elif response.status_code == 404:

            print(f"DOI não encontrado na Altmetric: {doi}")

            for key in dados_altmetric:
                dados_altmetric[key].append(0)


        # Outros erros

        else:

            print(
                f"Erro {response.status_code} para DOI: {doi}"
            )

            for key in dados_altmetric:
                dados_altmetric[key].append(None)



    except requests.exceptions.RequestException as e:

        print(
            f"Erro de conexão para DOI {doi}: {e}"
        )

        for key in dados_altmetric:
            dados_altmetric[key].append(None)


    time.sleep(0.2)



# ==========================================
# Conferência
# ==========================================

print("Linhas no CSV:", len(df))
print(
    "Resultados Altmetric:",
    len(dados_altmetric["doi_score"])
)


# ==========================================
# Adicionar resultados ao DataFrame
# ==========================================

for key, values in dados_altmetric.items():
    df[key] = values



# ==========================================
# Salvar CSV final
# ==========================================

df.to_csv(
    output_file,
    index=False,
    sep=";",
    float_format="%.2f"
)


print(f"Arquivo salvo como {output_file}")
df.to_csv(OUTPUT_FILE, index=False, sep=";")

print(f"Arquivo salvo como {OUTPUT_FILE} com delimitador ';'.")
