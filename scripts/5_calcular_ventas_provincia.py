import pandas as pd
import os

print("Iniciando el script de cálculo de ventas por provincia...")

# Definir rutas relativas
ruta_base = os.path.dirname(__file__)
ruta_pedidos = os.path.join(ruta_base, '..', 'RAW', 'sales_order.csv')
ruta_direcciones = os.path.join(ruta_base, '..', 'RAW', 'address.csv')
ruta_provincias = os.path.join(ruta_base, '..', 'RAW', 'province.csv')
ruta_dw = os.path.join(ruta_base, '..', 'DW', 'ventas_por_provincia.csv')

try:
    # Cargar los tres archivos que necesitamos
    df_pedidos = pd.read_csv(ruta_pedidos)
    df_direcciones = pd.read_csv(ruta_direcciones)
    df_provincias = pd.read_csv(ruta_provincias)
    print("Archivos CSV cargados correctamente.")

    # 1. Filtrar solo las ventas reales
    df_ventas = df_pedidos[df_pedidos['status'].isin(['PAID', 'FULFILLED'])].copy()

    # 2. Primera unión (Merge): Unir ventas con direcciones
    # Unimos usando el ID de la dirección de envío
    df_ventas_con_direccion = pd.merge(
        left=df_ventas,
        right=df_direcciones,
        left_on='shipping_address_id',
        right_on='address_id',
        how='left' # Usamos 'left' para mantener todas las ventas aunque alguna no tuviera dirección
    )
    print("Unión de ventas y direcciones completada.")

    # 3. Segunda unión (Merge): Unir el resultado con provincias
    df_completo = pd.merge(
        left=df_ventas_con_direccion,
        right=df_provincias,
        on='province_id',
        how='left'
    )
    print("Unión con provincias completada.")

    # 4. Agrupar por el nombre de la provincia y sumar el total de la venta
    ventas_por_provincia = df_completo.groupby('name')['total_amount'].sum().reset_index()
    ventas_por_provincia.columns = ['provincia', 'total_ventas'] # Renombrar columnas
    print("Cálculo de ventas por provincia finalizado.")

    # 5. Guardar el resultado en la carpeta DW
    os.makedirs(os.path.dirname(ruta_dw), exist_ok=True)
    ventas_por_provincia.to_csv(ruta_dw, index=False)

    print(f"Resultado guardado exitosamente en: {ruta_dw}")

except FileNotFoundError as e:
    print(f"Error: No se encontró el archivo. Revisa la ruta: {e.filename}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")