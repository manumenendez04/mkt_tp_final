import pandas as pd
import os

print("Iniciando el script de cálculo de ticket promedio...")

# Definir rutas relativas
ruta_base = os.path.dirname(__file__)
ruta_raw = os.path.join(ruta_base, '..', 'RAW', 'sales_order.csv')
ruta_dw = os.path.join(ruta_base, '..', 'DW', 'ticket_promedio_diario.csv')

try:
    df_pedidos = pd.read_csv(ruta_raw)
    print("Archivo 'sales_order.csv' cargado correctamente.")

    # 1. Filtrar solo las ventas reales, igual que antes
    df_ventas = df_pedidos[df_pedidos['status'].isin(['PAID', 'FULFILLED'])].copy()
    print(f"Se encontraron {len(df_ventas)} ventas para el cálculo.")

    # 2. Convertir 'order_date' a formato de fecha
    df_ventas['order_date'] = pd.to_datetime(df_ventas['order_date'])

    # 3. Agrupar por día y realizar dos cálculos a la vez: sumar el total y contar los pedidos
    calculo_diario = df_ventas.groupby(df_ventas['order_date'].dt.date).agg(
        total_ventas=('total_amount', 'sum'),
        numero_pedidos=('order_id', 'count')
    ).reset_index()

    # 4. Calcular la nueva columna 'ticket_promedio'
    calculo_diario['ticket_promedio'] = calculo_diario['total_ventas'] / calculo_diario['numero_pedidos']
    print("Cálculo de ticket promedio diario finalizado.")

    # 5. Seleccionar solo las columnas que nos interesan para el archivo final
    resultado_final = calculo_diario[['order_date', 'ticket_promedio']]
    resultado_final.columns = ['fecha', 'ticket_promedio'] # Renombrar para claridad

    # 6. Guardar el resultado en la carpeta DW
    os.makedirs(os.path.dirname(ruta_dw), exist_ok=True)
    resultado_final.to_csv(ruta_dw, index=False)

    print(f"Resultado guardado exitosamente en: {ruta_dw}")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta '{ruta_raw}'.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")