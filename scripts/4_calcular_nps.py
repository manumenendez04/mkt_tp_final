import pandas as pd
import os

print("Iniciando el script de cálculo de NPS...")

# Definir rutas relativas
ruta_base = os.path.dirname(__file__)
ruta_raw = os.path.join(ruta_base, '..', 'RAW', 'nps_response.csv')
ruta_dw = os.path.join(ruta_base, '..', 'DW', 'nps_calculado.csv')

try:
    df_nps = pd.read_csv(ruta_raw)
    print("Archivo 'nps_response.csv' cargado correctamente.")

    # 1. Definir una función para clasificar cada 'score'
    def clasificar_nps(score):
        if score >= 9:
            return 'Promotor'
        elif score >= 7:
            return 'Pasivo'
        else:
            return 'Detractor'

    # 2. Aplicar la función para crear una nueva columna 'categoria'
    df_nps['categoria'] = df_nps['score'].apply(clasificar_nps)
    print("Clasificación de respuestas NPS completada.")

    # 3. Contar el número de respuestas en cada categoría
    conteo_categorias = df_nps['categoria'].value_counts()
    total_respuestas = len(df_nps)

    # 4. Calcular el porcentaje de cada categoría
    # Usamos .get(key, 0) para evitar errores si una categoría no tiene respuestas
    porc_promotores = (conteo_categorias.get('Promotor', 0) / total_respuestas) * 100
    porc_detractores = (conteo_categorias.get('Detractor', 0) / total_respuestas) * 100

    # 5. Calcular el NPS final
    nps_score = porc_promotores - porc_detractores
    print(f"Cálculo de NPS finalizado. Puntuación: {nps_score:.2f}")

    # 6. Guardar el resultado en la carpeta DW
    # Creamos un DataFrame para guardarlo en un formato ordenado
    resultado_nps = pd.DataFrame({'nps_score': [nps_score]})

    os.makedirs(os.path.dirname(ruta_dw), exist_ok=True)
    resultado_nps.to_csv(ruta_dw, index=False)

    print(f"Resultado guardado exitosamente en: {ruta_dw}")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta '{ruta_raw}'.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")