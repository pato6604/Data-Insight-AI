import matplotlib.pyplot as plt

# Graficos columnas numericas
def obtener_columnas_numericas(df):
    return df.select_dtypes(include="number").columns.tolist()



# Histograma
def crear_histograma(df, columna):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df[columna].dropna(), bins=20, edgecolor="black")
    ax.set_title(f"Histograma de {columna}")
    ax.set_xlabel(columna)
    ax.set_ylabel("Frecuencia")
    fig.tight_layout()

    return fig

# Boxplot
def crear_boxplot(df, columna):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.boxplot(df[columna].dropna(), vert=False)
    ax.set_title(f"Box plot de {columna}")
    ax.set_xlabel(columna)
    fig.tight_layout()

    return fig




# Matriz de correlacion
def crear_matriz_correlacion(df):
    datos_numericos = df.select_dtypes(include="number")

    if datos_numericos.shape[1] < 2:
        return None

    correlacion = datos_numericos.corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    imagen = ax.imshow(correlacion, cmap="coolwarm", vmin=-1, vmax=1)

    ax.set_title("Matriz de correlacion")
    ax.set_xticks(range(len(correlacion.columns)))
    ax.set_yticks(range(len(correlacion.columns)))
    ax.set_xticklabels(correlacion.columns, rotation=45, ha="right")
    ax.set_yticklabels(correlacion.columns)

    for fila in range(len(correlacion.columns)):
        for columna in range(len(correlacion.columns)):
            valor = correlacion.iloc[fila, columna]
            ax.text(columna, fila, f"{valor:.2f}", ha="center", va="center")

    fig.colorbar(imagen, ax=ax)
    fig.tight_layout()

    return fig

