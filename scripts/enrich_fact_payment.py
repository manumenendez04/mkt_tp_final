import pandas as pd
from pathlib import Path

# --- RUTAS ---
BASE_DIR = Path(__file__).resolve().parents[1]
DW = BASE_DIR / "DW"

# --- LECTURA DE TABLAS ---
fact_payment = pd.read_csv(DW / "fact_payment.csv", parse_dates=["paid_at"])
fact_order = pd.read_csv(DW / "fact_order_item_enriched.csv")
dim_calendar = pd.read_csv(DW / "dim_calendar.csv", parse_dates=["date"])

# --- NORMALIZAR FECHAS ---
fact_payment["paid_date_norm"] = fact_payment["paid_at"].dt.normalize()

# --- AGREGAR CUSTOMER, CHANNEL, STORE DESDE FACT_ORDER_ITEM ---
# Tomamos columnas únicas por order_id (una sola fila por pedido)
order_lookup = fact_order.drop_duplicates(subset=["order_id"])[
    ["order_id", "customer_sk", "channel_sk", "store_sk"]
]

fact_payment = fact_payment.merge(order_lookup, how="left", on="order_id")

# --- RELACIONAR CON DIM_CALENDAR ---
fact_payment = fact_payment.merge(
    dim_calendar[["date", "date_sk"]],
    how="left",
    left_on="paid_date_norm",
    right_on="date"
)
fact_payment = fact_payment.rename(columns={"date_sk": "paid_date_sk"})

# --- REEMPLAZAR NULOS POR 0 ---
for col in ["customer_sk", "channel_sk", "store_sk", "paid_date_sk"]:
    fact_payment[col] = fact_payment[col].fillna(0).astype(int)

# --- SELECCIÓN FINAL DE COLUMNAS ---
cols = [
    "payment_sk", "payment_id", "order_id",
    "customer_sk", "channel_sk", "store_sk",
    "paid_date_sk", "method", "status", "amount", "transaction_ref"
]
fact_payment = fact_payment[cols]

# --- EXPORTAR ---
fact_payment.to_csv(DW / "fact_payment_enriched.csv", index=False)
print("✅ fact_payment_enriched creada en /DW/fact_payment_enriched.csv")
