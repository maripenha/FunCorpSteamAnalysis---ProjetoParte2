#funções que geram gráficos

import matplotlib.pyplot as plt
import pandas as pd
import estilo_plot
from estilo_plot import aplicar_estilo, PALETA

# Gráfico 1: Percentual de jogos que possuem suporte a cada SO (um voto por SO suportado)
def grafico_percentual_por_sistema(df: pd.DataFrame):
    aplicar_estilo()
    votos = []
    for _, row in df.iterrows():
        if row.get('has_windows'): votos.append('Windows')
        if row.get('has_mac'): votos.append('Mac')
        if row.get('has_linux'): votos.append('Linux')
    s = pd.Series(votos).value_counts()
    pct = (s / s.sum()) * 100
    ax = pct.sort_values(ascending=False).plot(kind='bar', color=PALETA[:len(pct)])
    ax.set_title('Percentual de suporte por sistema operacional')
    ax.set_ylabel('Percentual (%)')
    ax.set_xlabel('Sistema operacional')
    for i, v in enumerate(pct.sort_values(ascending=False).values):
        ax.text(i, v + 0.5, f'{v:.1f}%', ha='center', fontsize=9)
    plt.tight_layout()
    return ax

# Gráfico 2: Número total de jogos single-player (Indie e Strategy) por ano (2010–2020)
def grafico_singleplayer_indie_estrategia(df: pd.DataFrame):
    aplicar_estilo()
    sub = df[df['is_singleplayer'] & df['year'].between(2010, 2020)]
    def tem_genero(g, alvo):
        alvo = alvo.lower()
        return any(alvo == s.strip().lower() for s in g)
    indie = sub[sub['genres_list'].apply(lambda g: tem_genero(g, 'indie'))]
    strategy = sub[sub['genres_list'].apply(lambda g: tem_genero(g, 'strategy'))]
    g1 = indie.groupby('year').size().rename('Indie')
    g2 = strategy.groupby('year').size().rename('Strategy')
    anos = sorted(set(sub['year'].dropna()))
    df_plot = pd.DataFrame({'Indie': g1, 'Strategy': g2}).reindex(anos).fillna(0)
    ax = df_plot.plot(kind='line', marker='o', color=PALETA[:2])
    ax.set_title('Single-player: Indie vs Strategy (2010–2020)')
    ax.set_ylabel('Número de jogos')
    ax.set_xlabel('Ano')
    ax.legend(title='Gênero')
    plt.tight_layout()
    return ax

# Gráfico extra: média de avaliações positivas pago vs gratuito por ano (por gênero)
def grafico_paid_free_por_ano(df: pd.DataFrame, genero='indie'):
    aplicar_estilo()
    sub = df[df['year'].between(2010, 2022)].copy()
    sub['genero_principal'] = sub['genres_list'].apply(lambda g: g[0].lower() if g else 'unknown')
    foco = sub[sub['genero_principal'] == genero.lower()]
    g = foco.groupby(['year','is_paid'])['Positive'].mean().unstack(fill_value=0)
    cols = list(g.columns)
    
    # Ordena cores por colunas [False, True] = [Gratuito, Pago]
    color_map = [PALETA[0], PALETA[2]] if len(cols) == 2 else PALETA[:len(cols)]
    ax = g.plot(kind='line', marker='o', color=color_map)
    ax.set_title(f'Média de avaliações positivas: pago vs gratuito ({genero.capitalize()}, 2010–2022)')
    ax.set_ylabel('Média de avaliações positivas')
    ax.set_xlabel('Ano')
    ax.legend(title='Categoria', labels=['Gratuito','Pago'] if set(cols)=={False,True} else [str(c) for c in cols])
    plt.tight_layout()
    return ax
