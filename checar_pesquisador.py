#Esse script necessita de um arquivo .txt com os nomes dos pesquisadores a serem checados

import requests
import time

def verificar_nome_wikidata(nome):
    """Consulta a API do Wikidata para verificar se um nome existe."""
    url = "https://www.wikidata.org/w/api.php"
    
    headers = {
        'User-Agent': 'VerificadorNomesBot/1.0 (arrigo.adriano@gmail.com) python-requests'
    }
    
    # Parâmetros para a busca na API do MediaWiki do Wikidata
    parametros = {
        "action": "wbsearchentities",
        "search": nome,
        "language": "pt",  
        "format": "json"
    }
    
    try:
        # Passando o headers junto com a requisição
        resposta = requests.get(url, params=parametros, headers=headers)
        resposta.raise_for_status() 
        dados = resposta.json()
        
        resultados = dados.get('search', [])
        
        if resultados:
            primeiro_resultado = resultados[0]
            id_wikidata = primeiro_resultado.get('id')
            descricao = primeiro_resultado.get('description', 'Sem descrição')
            return True, id_wikidata, descricao
        else:
            return False, None, None
            
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao buscar '{nome}': {e}")
        return None, None, None

def main():
    arquivo_entrada = "check.txt"
    
    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            nomes = [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{arquivo_entrada}' não foi encontrado no mesmo diretório.")
        return

    print(f"Iniciando a verificação de {len(nomes)} nome(s) no Wikidata...\n")
    print("-" * 60)
    
    for nome in nomes:
        existe, id_wd, descricao = verificar_nome_wikidata(nome)
        
        if existe is True:
            print(f"[ ✓ ] ENCONTRADO: {nome}")
            print(f"      -> ID: {id_wd} | Descrição: {descricao}")
        elif existe is False:
            print(f"[ X ] NÃO ENCONTRADO: {nome}")
        else:
            print(f"[ ! ] ERRO: Não foi possível verificar '{nome}'")
            
        print("-" * 60)
        
        time.sleep(1)

if __name__ == "__main__":
    main()
