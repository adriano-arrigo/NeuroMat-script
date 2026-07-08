#Etapa 3 - Reconciliação dos dados
# Atenção! Para aplicar esse script, é necessário ter o arquivo df_altmetric.csv gerado na etapa 2 
# Após esse script, o dataframe está normalizado para ser usado

import pandas as pd
import re

arquivo_entrada = "df_altmetric.csv"
arquivo_saida = "df_altmetric_normalizado.csv"

df = pd.read_csv(arquivo_entrada, sep=";", on_bad_lines="skip")


def normalizar_doi_score(valor):
    if pd.isna(valor):
        return 0.0

    valor = str(valor).strip()

    if valor == "":
        return 0.0

    # Remove espaços e quebras invisíveis
    valor = valor.replace("\n", "").replace("\r", "").strip()

    # Caso: 2,715E+15, 1,285E+16 etc.
    if "E+" in valor.upper():
        mantissa = valor.upper().split("E+")[0]
        mantissa = mantissa.replace(",", "").replace(".", "")
        return float(mantissa) / 100

    # Remove todos os pontos e recoloca decimal nas duas últimas casas
    if valor.count(".") > 1:
        apenas_digitos = re.sub(r"\D", "", valor)
        if apenas_digitos == "":
            return 0.0
        return float(apenas_digitos[:4]) / 100 if len(apenas_digitos) > 10 else float(apenas_digitos) / 100

    # Caso com vírgula decimal: 2,55
    if "," in valor:
        valor = valor.replace(",", ".")
        return float(valor)

    # Caso já correto: 338.25
    if "." in valor:
        return float(valor)

    # Caso inteiro que perdeu decimal: 655 → 6.55
    if valor.isdigit():
        return float(valor) / 100

    return 0.0


df["doi_score"] = df["doi_score"].apply(normalizar_doi_score)

df.to_csv(arquivo_saida, sep=";", index=False)

print(f"Arquivo salvo como {arquivo_saida}")
print("Soma normalizada:", df["doi_score"].sum())
print(df["doi_score"].describe())
