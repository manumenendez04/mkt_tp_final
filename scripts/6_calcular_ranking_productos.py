import pandas as pd
import os

print("Iniciando el script de cálculo de ranking de productos...")

# Definir rutas relativas a todos los archivos necesarios
ruta_base = os.path.dirname(__file__)
ruta_items = os.path.join(ruta_base, '..', 'RAW', 'sales_order_item.csv')
ruta_pedidos = os.path.join(ruta_base, '..', 'RAW', 'sales_order.csv')
ruta_productos = os.path.join(ruta_base, '..', 'RAW', 'product.csv')
ruta_dw = os.path.join(ruta_base, '..', 'DW', 'ranking_productos_mensual.csv')

try:
    # Cargar los tres DataFrames
    df_items = pd.read_csv(ruta_items)
    df_pedidos = pd.read_csv(ruta_pedidos)
    df_productos = pd.read_csv(ruta_productos)
    print("Archivos CSV cargados correctamente.")

    # 1. Filtrar solo los pedidos que son ventas reales ('PAID', 'FULFILLED')
    # Hacemos esto primero para reducir la cantidad de datos a procesar
    pedidos_validos = df_pedidos[df_pedidos['status'].isin(['PAID', 'FULFILLED'])]

    # 2. Primera unión: Unir los items con los pedidos válidos para obtener la fecha
    df_items_con_fecha = pd.merge(
        left=df_items,
        right=pedidos_validos[['order_id', 'order_date']], # Solo necesitamos estas columnas del df de pedidos
        on='order_id',
        how='inner' # 'inner' join para quedarnos solo con los items de pedidos válidos
    )
    print("Unión de items y pedidos completada.")

    # 3. Segunda unión: Unir con la tabla de productos para obtener el nombre
    df_completo = pd.merge(
        left=df_items_con_fecha,
        right=df_productos[['product_id', 'name']],
        on='product_id',
        how='left'
    )
    print("Unión con productos completada.")

    # 4. Preparar la columna de fecha para agrupar por mes
    df_completo['order_date'] = pd.to_datetime(df_completo['order_date'])
    # Creamos una nueva columna 'mes' en formato 'YYYY-MM'
    df_completo['mes'] = df_completo['order_date'].dt.to_period('M').astype(str)

    # 5. Agrupar por mes y nombre del producto, y sumar el total de la línea
    ranking_mensual = df_completo.groupby(['mes', 'name'])['line_total'].sum().reset_index()
    ranking_mensual.columns = ['mes', 'producto', 'total_ventas'] # Renombrar columnas
    print("Cálculo del ranking mensual finalizado.")

    # 6. Guardar el resultado final en la carpeta DW
    os.makedirs(os.path.dirname(ruta_dw), exist_ok=True)
    ranking_mensual.to_csv(ruta_dw, index=False)

    print(f"Resultado guardado exitosamente en: {ruta_dw}")

except FileNotFoundError as e:
    print(f"Error: No se encontró el archivo. Revisa la ruta: {e.filename}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")