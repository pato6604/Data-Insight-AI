import pandas as pd


# Creo la funcion para cargar el archivo csv


def load_data(file):
    try:
        df = pd.read_csv(file)
        return df
    
    except Exception as e:
        raise Exception (f'Error al cargart el archivo {e}')
    
    