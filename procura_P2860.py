import pandas as pd
import requests
import time
import re

# === CONFIGURAÇÕES ===
csv_input = "itens.csv"              # arquivo CSV de entrada
csv_output = "resultado_p2860.csv"   # arquivo CSV de saída
endpoint = "https://query-scholarly.wikidata.org/sparql"  # ou "https://query.wikidata.org/sparql"
batch_size = 20                      # tamanho do lote (use 20 para o Scholarly)
delay = 2                            # segundos entre requisições

# === FUNÇÃO PARA RODAR A QUERY ===
def run_query(endpoint, query):
    headers = {
        "User-Agent": "NeuroMatDataBot/0.1 (https://neuromat.numec.prp.usp.usp.br)",
        "Accept": "application/sparql-results+json",
        "Content-Type": "application/sparql-query"
    }
    response = requests.post(endpoint, data=query.encode('utf-8'), headers=headers)
    response.raise_for_status()
    return response.json()

# === CARREGAR E LIMPAR CSV ===
df = pd.read_csv(csv_input)
df.columns = df.columns.str.strip().str.upper()

if "QID" not in df.columns:
    raise ValueError("O arquivo CSV precisa ter uma coluna chamada 'QID'.")

# Limpa QIDs e remove valores inválidos
qids = df["QID"].dropna().astype(str).str.strip().unique().tolist()
qids = [qid for qid in qids if re.match(r"^Q\d+$", qid)]

print(f"Total de itens a verificar: {len(qids)}")

# === CONSULTAR EM LOTES ===
results = []
for i in range(0, len(qids), batch_size):
    batch = qids[i:i+batch_size]
    print(f" Consultando lote {i//batch_size + 1} ({len(batch)} itens)...")

    values_str = " ".join(f"wd:{qid}" for qid in batch)
    query = f"""
    SELECT ?item ?itemLabel (COUNT(?citation) AS ?numCitations)
    WHERE {{
      VALUES ?item {{ {values_str} }}
      OPTIONAL {{ ?item wdt:P2860 ?citation. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    GROUP BY ?item ?itemLabel
    """

    try:
        data = run_query(endpoint, query)
        for b in data["results"]["bindings"]:
            results.append({
                "QID": b["item"]["value"].split("/")[-1],
                "Label": b.get("itemLabel", {}).get("value", ""),
                "numCitations": int(b.get("numCitations", {}).get("value", 0))
            })
    except Exception as e:
        print(f" Erro no lote {i//batch_size + 1}: {e}")

    time.sleep(delay)

# === JUNTAR RESULTADOS ===
results_df = pd.DataFrame(results)
results_df.rename(columns={"item": "QID"}, inplace=True)

merged = df.merge(results_df, on="QID", how="left")
merged["numCitations"] = merged["numCitations"].fillna(0).astype(int)

merged.to_csv(csv_output, index=False)
print(f"Resultados salvos em: {csv_output}")
