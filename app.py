import streamlit as st
from src.data_loader import load_data
from src.EDA import (
    obtener_dimensiones,
    obtener_tipos_datos,
    obtener_valores_nulos,
    obtener_duplicados,
    obtener_estadisticas_numericas,
    obtener_estadisticas_categoricas
)

from src.charts import (
    obtener_columnas_numericas,
    crear_histograma,
    crear_boxplot,
    crear_matriz_correlacion
)
from src.insights import (
    detectar_correlaciones,
    detectar_outliers_iqr,
    generar_texto_correlaciones,
    generar_texto_outliers
)
from src.llm import (
    cargar_api_key_openai,
    generar_contexto_dataset,
    responder_pregunta_dataset
)




#Titulo del proyecto 
st.title("AI Data Insight")



# Carga del archivo por parte del usuario 
archivo = st.file_uploader(
    "Subí un CSV",
    type=["csv"]
)



# Validacion de la carga 
if archivo is None:
    st.info("Subi un archivo CSV para comenzar el analisis.")
    st.stop()

df = load_data(archivo)

st.success("Archivo cargado")

st.write(df.head())
    



# Dimensiones en pantalla
filas, columnas = obtener_dimensiones(df)

st.subheader("Dimensiones")
st.write("Filas:", filas)
st.write("Columnas:", columnas)


# Tipos de datos en pantalla
st.subheader('Tipos de datos')
st.dataframe(obtener_tipos_datos(df))


# Valores nulos en pantalla 
st.subheader("Valores nulos")
st.dataframe(obtener_valores_nulos(df))


# Valores duplicados en pantalla 
st.subheader("Duplicados")
st.write(obtener_duplicados(df))



# Estadisticas basicas 

st.subheader("Estadísticas numéricas")
st.dataframe(obtener_estadisticas_numericas(df))

st.subheader("Estadísticas categóricas")
st.dataframe(obtener_estadisticas_categoricas(df))


# Graficos
st.subheader("Graficos")

columnas_numericas = obtener_columnas_numericas(df)

if not columnas_numericas:
    st.warning("No hay columnas numericas para graficar.")
else:
    columna_grafico = st.selectbox(
        "Selecciona una columna numerica",
        columnas_numericas
    )

    st.write("Histograma")
    st.pyplot(crear_histograma(df, columna_grafico))

    st.write("Box plot")
    st.pyplot(crear_boxplot(df, columna_grafico))

    st.write("Matriz de correlacion")
    matriz_correlacion = crear_matriz_correlacion(df)

    if matriz_correlacion is None:
        st.info("Se necesitan al menos dos columnas numericas para calcular la correlacion.")
    else:
        st.pyplot(matriz_correlacion)


# Insights automaticos
st.subheader("Insights automaticos")

correlaciones_fuertes = detectar_correlaciones(df)
outliers_por_columna = detectar_outliers_iqr(df)

st.write("Correlaciones fuertes")
st.text(generar_texto_correlaciones(correlaciones_fuertes))

st.write("Valores atipicos")
st.text(generar_texto_outliers(outliers_por_columna))


# Preguntas con OpenAI
st.subheader("Preguntas sobre el dataset")

api_key = cargar_api_key_openai()

pregunta_dataset = st.text_area(
    "Escribi una pregunta sobre el dataset cargado"
)

if st.button("Responder pregunta"):
    if not api_key:
        st.warning("No se encontro OPENAI_API_KEY en el archivo .env.")
    elif not pregunta_dataset.strip():
        st.warning("Escribi una pregunta antes de consultar.")
    else:
        contexto_dataset = generar_contexto_dataset(df)

        with st.spinner("Consultando OpenAI..."):
            try:
                respuesta = responder_pregunta_dataset(
                    pregunta_dataset,
                    contexto_dataset,
                    api_key=api_key
                )
                st.write(respuesta)
            except Exception as error:
                st.error(f"No se pudo obtener una respuesta: {error}")
