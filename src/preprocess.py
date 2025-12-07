#funções para carregar e limpar dadoscd caminho/para/projeto-jogos

import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    # CSV com separador ponto-e-vírgula. Adiciona encoding para lidar com acentos.
    return pd.read_csv(path, sep=";", encoding='latin-1')

def _split_multi(val):
    if pd.isna(val): return []
    
    return [s.strip() for s in str(val).replace('|',';').split(';') if s.strip()]

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Datas e ano
    df['Release date'] = pd.to_datetime(df['Release date'], errors='coerce')
    df['year'] = df['Release date'].dt.year

    num_cols = [
        'Price','DLC count','Metacritic score','Positive','Negative',
        'Screenshots','Movies','User score','Achievements','Recommendations',
        'Average playtime forever','Average playtime two weeks',
        'Median playtime forever','Median playtime two weeks','Score rank'
    ]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Pago/gratuito
    df['Price'] = df['Price'].fillna(0)
    df['is_free'] = df['Price'] == 0
    df['is_paid'] = ~df['is_free']

    # Listas categóricas
    df['genres_list'] = df['Genres'].apply(_split_multi) if 'Genres' in df.columns else [[]]*len(df)
    df['categories_list'] = df['Categories'].apply(_split_multi) if 'Categories' in df.columns else [[]]*len(df)
    df['tags_list'] = df['Tags'].apply(_split_multi) if 'Tags' in df.columns else [[]]*len(df)

    # Suporte a sistemas operacionais 
    df['has_windows'] = df['Windows'].astype(bool) if 'Windows' in df.columns else False
    df['has_mac'] = df['Mac'].astype(bool) if 'Mac' in df.columns else False
    df['has_linux'] = df['Linux'].astype(bool) if 'Linux' in df.columns else False

    # Single-player a partir de Categories
    df['is_singleplayer'] = df['categories_list'].apply(lambda cats: any('Single-player' in c for c in cats))

    # Mídia de demonstração
    df['Screenshots'] = df['Screenshots'].fillna(0)
    df['Movies'] = df['Movies'].fillna(0)
    df['demo_media'] = df['Screenshots'] + df['Movies']

    # Título
    if 'Name' in df.columns:
        df = df.dropna(subset=['Name'])

    return df
