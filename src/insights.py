def detectar_correlaciones(df, umbral=0.8):
    datos_numericos = df.select_dtypes(include="number")

    if datos_numericos.shape[1] < 2:
        return []

    matriz_correlacion = datos_numericos.corr()
    correlaciones_fuertes = []

    for indice, columna_1 in enumerate(matriz_correlacion.columns):
        for columna_2 in matriz_correlacion.columns[indice + 1:]:
            valor = matriz_correlacion.loc[columna_1, columna_2]

            if abs(valor) >= umbral:
                correlaciones_fuertes.append({
                    "columna_1": columna_1,
                    "columna_2": columna_2,
                    "correlacion": float(valor)
                })

    return correlaciones_fuertes


def detectar_outliers_iqr(df):
    datos_numericos = df.select_dtypes(include="number")
    outliers_por_columna = {}

    for columna in datos_numericos.columns:
        serie = datos_numericos[columna].dropna()

        q1 = serie.quantile(0.25)
        q3 = serie.quantile(0.75)
        iqr = q3 - q1

        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr

        outliers = serie[
            (serie < limite_inferior) |
            (serie > limite_superior)
        ]

        outliers_por_columna[columna] = len(outliers)

    return outliers_por_columna


def generar_texto_correlaciones(correlaciones):
    if not correlaciones:
        return "No se detectaron correlaciones fuertes entre columnas numericas."

    textos = ["Se detectaron correlaciones fuertes entre estas columnas:"]

    for correlacion in correlaciones:
        columna_1 = correlacion["columna_1"]
        columna_2 = correlacion["columna_2"]
        valor = correlacion["correlacion"]

        textos.append(
            f"- {columna_1} y {columna_2}: correlacion de {valor:.2f}"
        )

    return "\n".join(textos)


def generar_texto_outliers(outliers_por_columna):
    if not outliers_por_columna:
        return "No hay columnas numericas para analizar valores atipicos."

    textos = ["Cantidad de valores atipicos detectados por columna:"]

    for columna, cantidad in outliers_por_columna.items():
        textos.append(f"- {columna}: {cantidad} valores atipicos")

    return "\n".join(textos)
