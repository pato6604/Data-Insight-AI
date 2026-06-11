import pandas as pd 

# Obtener dimensiones del dataframe
def obtener_dimensiones(df):
    filas = df.shape[0]
    columnas = df.shape[1]

    return filas, columnas

# Obtener tipos de datos
def obtener_tipos_datos(df):
    tipos_datos = df.dtypes

    return tipos_datos


# Obtener valores NaN
def obtener_valores_nulos(df):
    valores_nulos = df.isnull().sum()

    return valores_nulos


# Obtener duplicados
def obtener_duplicados(df):
    duplicados = df.duplicated().sum()

    return duplicados


# Obtener estadisticas basicas
def obtener_estadisticas_numericas(df):
    estadisticas_numericas = df.describe(include='number')

    return estadisticas_numericas


def obtener_estadisticas_categoricas(df):
    estadisticas_categoricas = df.describe(include='object')

    return estadisticas_categoricas