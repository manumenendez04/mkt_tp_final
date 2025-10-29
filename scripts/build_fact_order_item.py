import pandas as pd
from pathlib import Path

# --- RUTAS ---
BASE_DIR = Path(__file__).resolve().parents[1]
RAW = BASE_DIR / "RAW"
DW = BASE_DIR / "DW"
DW.mkdir(exist_ok=True)

# --- LECTURA DE TABLAS ---
orders = pd.read_csv(RAW / "sales_order.csv", parse_dates=["order_date"])
items = pd.read_csv(RAW / "sales_order_item.csv")

# --- LIMPIEZA BÁSICA ---
for df in [orders, items]:
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

# --- UNIÓN ENTRE ORDEN E ÍTEM ---
fact = items.merge(orders, on="order_id", how="left", suffixes=("_item", "_order"))

# --- CÁLCULOS DE MÉTRICAS ---
fact["gross_amount"] = fact["quantity"] * fact["unit_price"]
fact["net_amount"] = fact["gross_amount"] - fact["discount_amount"]

# --- CLAVE SURROGATE (opcional, para DW) ---
fact.insert(0, "order_item_sk", range(1, len(fact) + 1))

# --- SELECCIÓN Y ORDEN DE COLUMNAS ---
cols = [
    "order_item_sk",
    "order_item_id", "order_id", "order_date",
    "customer_id", "product_id", "channel_id", "store_id",
    "billing_address_id", "shipping_address_id",
    "status", "currency_code",
    "quantity", "unit_price", "discount_amount", "gross_amount", "net_amount",
    "subtotal", "tax_amount", "shipping_fee", "total_amount"
]
fact = fact[cols]

# --- EXPORTAR ---
fact.to_csv(DW / "fact_order_item.csv", index=False)
print("✅ fact_order_item creada en /DW/fact_order_item.csv (unifica sales_order + sales_order_item)")
