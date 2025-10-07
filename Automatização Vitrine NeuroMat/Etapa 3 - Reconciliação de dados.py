# Atenção! Para aplicar esse script, é necessário ter o arquivo df_altmetric.csv gerado na etapa 2 

import requests
import pandas as pd

# Nome do arquivo CSV de entrada com cada produção cientifica já com os valores altmetricos
csv_file = "df_altmetric.csv"

# Carregar o CSV, especificando o delimitador como ';'
df = pd.read_csv(csv_file, delimiter=';', on_bad_lines='skip')  # Added delimiter and error handling


doi_score = df['doi_score']
readers = df['readers_count']
tweeters = df['cited_by_tweeters_count']
rdts = df['cited_by_rdts']
news_count = df['cited_by_msm_count']
feeds = df['cited_by_feeds_count']
accounts = df['cited_by_accounts_count']
fbwalls = df['cited_by_fbwalls_count']
gplus = df['cited_by_gplus_count']
videos = df['cited_by_videos_count']
wikipedia = df['cited_by_wikipedia_count']

# Converter as colunas para o tipo numérico


for ind in readers.index:
    if len(str(doi_score[ind])) > 20:
        doi_score.iloc[ind] = 0.0
    if len(str(readers[ind])) > 20:
        readers.iloc[ind] = 0.0
    if len(str(tweeters[ind])) > 20:
        tweeters.iloc[ind] = 0.0
    if len(str(rdts[ind])) > 20:
        rdts.iloc[ind] = 0.0
    if len(str(news_count[ind])) > 20:
        news_count.iloc[ind] = 0.0
    if len(str(feeds[ind])) > 20:
        feeds.iloc[ind] = 0.0
    if len(str(accounts[ind])) > 20:
        accounts.iloc[ind] = 0.0
    if len(str(fbwalls[ind])) > 20:
        fbwalls.iloc[ind] = 0.0
    if len(str(gplus[ind])) > 20:
        gplus.iloc[ind] = 0.0
    if len(str(videos[ind])) > 20:
        videos.iloc[ind] = 0.0
    if len(str(wikipedia[ind])) > 20:
        wikipedia.iloc[ind] = 0.0

doi_score = doi_score.fillna(0.0)
doi_score = doi_score.astype(float)

readers = readers.fillna(0.0)
readers = readers.astype(float)

tweeters = tweeters.fillna(0.0)
tweeters = tweeters.astype(float)

rdts = rdts.fillna(0.0)
rdts = rdts.astype(float)

news_count = news_count.fillna(0.0)
news_count = news_count.astype(float)

feeds = feeds.fillna(0.0)
feeds = feeds.astype(float)

accounts = accounts.fillna(0.0)
accounts = accounts.astype(float)

fbwalls = fbwalls.fillna(0.0)
fbwalls = fbwalls.astype(float)

gplus = gplus.fillna(0.0)
gplus = gplus.astype(float)

videos = videos.fillna(0.0)
videos = videos.astype(float)

wikipedia = wikipedia.fillna(0.0)
wikipedia = wikipedia.astype(float)
