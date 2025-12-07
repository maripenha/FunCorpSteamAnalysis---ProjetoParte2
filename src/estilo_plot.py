#estilo padronizado dos gráficos

import matplotlib.pyplot as plt
PALETA = ['#4C78A8','#F58518','#E45756','#72B7B2','#54A24B','#EECA3B']

def aplicar_estilo():
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({
        'figure.figsize': (8, 5),
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'lines.linewidth': 2,
        'axes.grid': True,
        'grid.alpha': 0.3
    })
