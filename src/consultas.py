#funções que respondem às perguntas

import pandas as pd

# P1: Top 10 Metacritic (empates resolvidos por data mais antiga)
def top10_metacritic(df: pd.DataFrame) -> pd.DataFrame:
    base = df.dropna(subset=['Metacritic score'])
    out = base.sort_values(by=['Metacritic score','Release date'], ascending=[False, True])
    return out[['Name','Metacritic score','Release date']].head(10)

# P2: RPG: média e máximo de DLCs, positivas, negativas e materiais de demo
def rpg_stats(df: pd.DataFrame) -> pd.Series:
    # Filtrar se algum gênero contém 'RPG' ou 'Role-Playing'
    is_rpg = df['genres_list'].apply(lambda g: any(('rpg' in s.lower()) or ('role' in s.lower()) for s in g))
    sub = df[is_rpg]
    return pd.Series({
        'dlc_mean': sub['DLC count'].mean(),
        'dlc_max': sub['DLC count'].max(),
        'pos_mean': sub['Positive'].mean(),
        'pos_max': sub['Positive'].max(),
        'neg_mean': sub['Negative'].mean(),
        'neg_max': sub['Negative'].max(),
        'demo_mean': sub['demo_media'].mean(),
        'demo_max': sub['demo_media'].max(),
        'n_jogos': int(sub.shape[0])
    })

# P3: Top 5 publishers que mais publicam jogos pagos + médias e medianas de positivas
def top5_publishers_paid(df: pd.DataFrame) -> pd.DataFrame:
    paid = df[df['is_paid'] & df['Publishers'].notna()]
    # Publishers podem ter múltiplos nomes separados; vamos considerar o primeiro como principal
    paid = paid.copy()
    paid['publisher_main'] = paid['Publishers'].apply(lambda s: str(s).split(';')[0].split('|')[0].strip())
    pubs_top = paid.groupby('publisher_main').size().sort_values(ascending=False).head(5).index
    sub = paid[paid['publisher_main'].isin(pubs_top)]
    res = sub.groupby('publisher_main')['Positive'].agg(['count','mean','median']).sort_values('count', ascending=False)
    return res.rename(columns={'count':'jogos_pagos','mean':'pos_mean','median':'pos_median'})

# P4: Crescimento de jogos com suporte Linux entre 2018 e 2022
def linux_growth_2018_2022(df: pd.DataFrame) -> pd.DataFrame:
    sub = df[df['year'].between(2018, 2022) & df['has_linux']]
    res = sub.groupby('year').size().rename('qtd_linux').reset_index()
    idx = pd.DataFrame({'year': list(range(2018, 2023))})
    return idx.merge(res, on='year', how='left').fillna({'qtd_linux': 0}).astype({'qtd_linux': int})

# Extra: pagos vs gratuitos por ano e gênero principal (2010–2022)
def paid_vs_free_reviews(df: pd.DataFrame) -> pd.DataFrame:
    sub = df[df['year'].between(2010, 2022)].copy()
    sub['genero_principal'] = sub['genres_list'].apply(lambda g: g[0].lower() if g else 'unknown')
    return sub.groupby(['year','genero_principal','is_paid'])['Positive'].mean().reset_index()
