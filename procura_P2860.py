# Este script gera um arquivo CSV com a contagem total de referências bibliográficas (propriedade P2860)
# para um conjunto de itens listados (lote) em um arquivo itens.csv. 
# Para cada QID, o script consulta simultaneamente os endpoints Scholarly e Main do WDQS,
# pois, devido ao split do grafo, algumas referências podem aparecer apenas em um dos endpoints.
# O resultado final mostra o total de P2860 e indica em qual endpoint esse total foi maior.
# Não é mostrado o título de cada referência bibliográfica, apenas um número total resultado da soma referência bibliográfica do item analisado.

import pandas as pd
import requests
import time
import re

# ---------------------------
# CONFIGURAÇÕES
# ---------------------------
CSV_INPUT = "itens.csv"
CSV_OUTPUT = "resultado_p2860.csv"

ENDPOINT_SCHOLARLY = "https://query-scholarly.wikidata.org/sparql"
ENDPOINT_MAIN = "https://query.wikidata.org/sparql"

BATCH_SIZE = 40     # ajuste conforme necessidade (20-50 razoável)
DELAY = 1.0         # segundos entre requisições para evitar rate limits
TIMEOUT = 60        # timeout em segundos para requests

USER_AGENT = "VitrineNeuroMatDataBot/0.1 (contato: arrigo.adriano@gmail.com)"  # personalizável

# ---------------------------
# FUNÇÕES AUXILIARES
# ---------------------------
def run_sparql_post(endpoint, query):
    """
    Executa uma consulta SPARQL via POST e retorna JSON (ou lança exception).
    Uso de POST evita problemas com URLs muito longas (especialmente no Scholarly).
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/sparql-results+json",
        "Content-Type": "application/sparql-query; charset=utf-8"
    }
    resp = requests.post(endpoint, data=query.encode("utf-8"), headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()

def consultar_p2860_completa(endpoint, qids):
    """
    Consulta counts e labels para um lote de QIDs num dado endpoint.
    Retorna dicionário:
      { 'Q123': {'count': int, 'label': '...', 'endpoint': 'scholarly'|'main'} , ... }
    """
    if not qids:
        return {}

    values = " ".join(f"wd:{qid}" for qid in qids)
    # Query: conta P2860 por item e traz label (se houver)
    query = f"""
    SELECT ?item ?itemLabel (COUNT(?citation) AS ?numCitations)
    WHERE {{
      VALUES ?item {{ {values} }}
      OPTIONAL {{ ?item wdt:P2860 ?citation. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    GROUP BY ?item ?itemLabel
    """

    data = run_sparql_post(endpoint, query)
    out = {}
    for b in data.get("results", {}).get("bindings", []):
        qid = b["item"]["value"].split("/")[-1]
        label = b.get("itemLabel", {}).get("value", "")
        count = int(b.get("numCitations", {}).get("value", 0))
        out[qid] = {"count": count, "label": label}
    # Para QIDs que não aparecem no resultado, retornaremos 0 e label vazio (fora da função)
    return out

# ---------------------------
# FLUXO PRINCIPAL
# ---------------------------
def main():
    # 1) carregar CSV
    df = pd.read_csv(CSV_INPUT)
    df.columns = df.columns.str.strip().str.upper()
    if "QID" not in df.columns:
        raise ValueError("O arquivo CSV precisa ter coluna 'QID' (exatamente).")

    # limpar QIDs
    qids_raw = df["QID"].dropna().astype(str).str.strip().unique().tolist()
    qids = [q for q in qids_raw if re.match(r"^Q\d+$", q)]
    print(f"Total QIDs válidos: {len(qids)}")

    # 2) Preparar estrutura para resultados
    registros = []

    # 3) Percorrer em lotes e consultar ambos endpoints
    for start in range(0, len(qids), BATCH_SIZE):
        lote = qids[start:start + BATCH_SIZE]
        print(f"Processando lote {start//BATCH_SIZE + 1}: {len(lote)} itens...")

        # 3a) consultar Scholarly (POST)
        scholarly_data = {}
        try:
            scholarly_data = consultar_p2860_completa(ENDPOINT_SCHOLARLY, lote)
        except Exception as e:
            print(f"  Erro ao consultar Scholarly no lote {start//BATCH_SIZE + 1}: {e}")

        time.sleep(DELAY)

        # 3b) consultar Main (POST)
        main_data = {}
        try:
            main_data = consultar_p2860_completa(ENDPOINT_MAIN, lote)
        except Exception as e:
            print(f"  Erro ao consultar Main no lote {start//BATCH_SIZE + 1}: {e}")

        time.sleep(DELAY)

        # 3c) compilar resultados por item
        for q in lote:
            schol = scholarly_data.get(q, {"count": 0, "label": ""})
            m = main_data.get(q, {"count": 0, "label": ""})

            count_schol = schol["count"]
            count_main = m["count"]
            label_schol = schol["label"]
            label_main = m["label"]

            # decidir final: maior valor; se iguais e >0 -> both; se ambos 0 -> none
            if count_schol > count_main:
                final_count = count_schol
                endpoint_maior = "scholarly"
            elif count_main > count_schol:
                final_count = count_main
                endpoint_maior = "main"
            else:  # iguais
                final_count = count_schol  # (ambos iguais)
                if final_count == 0:
                    endpoint_maior = "none"
                else:
                    endpoint_maior = "both"

            registros.append({
                "QID": q,
                "Label_Scholarly": label_schol,
                "P2860_Scholarly": count_schol,
                "Label_Main": label_main,
                "P2860_Main": count_main,
                "P2860_Final": final_count,
                "Endpoint_Maior": endpoint_maior
            })

    # 4) salvar resultado completo em CSV
    df_out = pd.DataFrame(registros)
    df_out = df.merge(df_out, on="QID", how="right")
    df_out.to_csv(CSV_OUTPUT, index=False)
    print(f" Salvo: {CSV_OUTPUT}")

if __name__ == "__main__":
    main()
