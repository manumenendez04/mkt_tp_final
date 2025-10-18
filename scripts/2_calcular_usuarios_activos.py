import pandas as pd
import os

print("Iniciando el script de cálculo de usuarios activos...")

# Definir rutas relativas
ruta_base = os.path.dirname(__file__)
ruta_raw = os.path.join(ruta_base, '..', 'RAW', 'web_session.csv')
ruta_dw = os.path.join(ruta_base, '..', 'DW', 'usuarios_activos_diarios.csv')

try:
    df_sesiones = pd.read_csv(ruta_raw)
    print("Archivo 'web_session.csv' cargado correctamente.")

    # Convertir 'started_at' a formato de fecha
    df_sesiones['started_at'] = pd.to_datetime(df_sesiones['started_at'])

    # Eliminar sesiones sin un customer_id (sesiones anónimas)
    df_sesiones.dropna(subset=['customer_id'], inplace=True)

    # Agrupar por fecha y contar los clientes únicos (COUNT DISTINCT) [cite: 181]
    usuarios_activos = df_sesiones.groupby(df_sesiones['started_at'].dt.date)['customer_id'].nunique().reset_index()
    usuarios_activos.columns = ['fecha', 'usuarios_activos']
    print("Cálculo de usuarios activos diarios finalizado.")

    # Guardar el resultado en la carpeta DW
    os.makedirs(os.path.dirname(ruta_dw), exist_ok=True)
    usuarios_activos.to_csv(ruta_dw, index=False)

    print(f"Resultado guardado exitosamente en: {ruta_dw}")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta '{ruta_raw}'.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")