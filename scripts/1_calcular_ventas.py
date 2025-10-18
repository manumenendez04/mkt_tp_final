# 1. Importar la librería pandas para manipular los datos
import pandas as pd
import os

print("Iniciando el script de cálculo de ventas...")

# 2. Definir las rutas a los archivos de forma relativa
# Esto hace que el script funcione en cualquier computadora
ruta_base = os.path.dirname(__file__) # Obtenemos la ruta de la carpeta 'scripts'
ruta_raw = os.path.join(ruta_base, '..', 'RAW', 'sales_order.csv')
ruta_dw = os.path.join(ruta_base, '..', 'DW', 'ventas_diarias.csv')

# 3. Cargar el archivo CSV en un DataFrame de pandas
try:
    df_pedidos = pd.read_csv(ruta_raw)
    print("Archivo 'sales_order.csv' cargado correctamente.")

    # 4. Realizar las transformaciones de datos
    # [cite_start]Filtrar solo los pedidos pagados o completados, que son las ventas reales [cite: 179, 180]
    df_ventas = df_pedidos[df_pedidos['status'].isin(['PAID', 'FULFILLED'])].copy()
    print(f"Se encontraron {len(df_ventas)} ventas reales.")

    # Convertir la columna 'order_date' a un formato de fecha para poder trabajar con ella
    df_ventas['order_date'] = pd.to_datetime(df_ventas['order_date'])

    # Agrupar por fecha y sumar el total. Esto nos servirá para el gráfico de "serie temporal"
    ventas_por_dia = df_ventas.groupby(df_ventas['order_date'].dt.date)['total_amount'].sum().reset_index()
    ventas_por_dia.columns = ['fecha', 'total_ventas'] # Renombrar columnas para claridad
    print("Cálculo de ventas diarias finalizado.")

    # 5. Guardar el resultado en un nuevo archivo CSV en la carpeta DW
    # Asegurarse de que la carpeta DW exista
    os.makedirs(os.path.dirname(ruta_dw), exist_ok=True)
    ventas_por_dia.to_csv(ruta_dw, index=False)

    print(f"Resultado guardado exitosamente en: {ruta_dw}")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta '{ruta_raw}'. Verifica que el archivo exista.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")