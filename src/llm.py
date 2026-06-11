import os

from openai import OpenAI
from dotenv import load_dotenv


def cargar_api_key_openai():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")


def generar_contexto_dataset(df, max_filas=5, max_caracteres=6000):
    columnas = []

    for columna, tipo in df.dtypes.items():
        columnas.append(f"- {columna}: {tipo}")

    partes_contexto = [
        "Resumen del dataset:",
        f"- Filas: {df.shape[0]}",
        f"- Columnas: {df.shape[1]}",
        "",
        "Columnas y tipos de datos:",
        "\n".join(columnas),
        "",
        "Valores nulos por columna:",
        df.isnull().sum().to_string(),
        "",
        f"Primeras {max_filas} filas:",
        df.head(max_filas).to_string(index=False),
    ]

    datos_numericos = df.select_dtypes(include="number")
    if not datos_numericos.empty:
        partes_contexto.extend([
            "",
            "Estadisticas de columnas numericas:",
            datos_numericos.describe().to_string()
        ])

    datos_categoricos = df.select_dtypes(include=["object", "category", "bool"])
    if not datos_categoricos.empty:
        partes_contexto.extend([
            "",
            "Estadisticas de columnas categoricas:",
            datos_categoricos.describe().to_string()
        ])

    contexto = "\n".join(partes_contexto)

    if len(contexto) > max_caracteres:
        contexto = contexto[:max_caracteres] + "\n\n[Contexto truncado por longitud]"

    return contexto


def responder_pregunta_dataset(
    pregunta,
    contexto_dataset,
    api_key=None,
    modelo="gpt-4.1-mini"
):
    if api_key is None:
        api_key = cargar_api_key_openai()

    client = OpenAI(api_key=api_key) if api_key else OpenAI()

    respuesta = client.responses.create(
        model=modelo,
        input=[
            {
                "role": "system",
                "content": (
                    "Sos un asistente de analisis de datos. "
                    "Responde solo usando el contexto del dataset provisto. "
                    "Si no hay informacion suficiente, decilo claramente."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Contexto del dataset:\n{contexto_dataset}\n\n"
                    f"Pregunta del usuario:\n{pregunta}"
                )
            }
        ]
    )

    return respuesta.output_text
