import pandas as pd
from pathlib import Path

# --- RUTAS ---
BASE_DIR = Path(__file__).resolve().parents[1]
DW = BASE_DIR / "DW"

# --- LECTURA DE TABLAS ---
fact = pd.read_csv(DW / "fact_order_item.csv", parse_dates=["order_date"])
dim_customer = pd.read_csv(DW / "dim_customer.csv")
dim_product = pd.read_csv(DW / "dim_product.csv")
dim_channel = pd.read_csv(DW / "dim_channel.csv")
dim_store = pd.read_csv(DW / "dim_store.csv")
dim_address = pd.read_csv(DW / "dim_address.csv")
dim_calendar = pd.read_csv(DW / "dim_calendar.csv", parse_dates=["date"])

# --- JOINS CON DIMENSIONES ---

# Customer
fact = fact.merge(
    dim_customer[["customer_id", "customer_sk"]],
    how="left",
    on="customer_id"
)

# Product
fact = fact.merge(
    dim_product[["product_id", "product_sk"]],
    how="left",
    on="product_id"
)

# Channel
fact = fact.merge(
    dim_channel[["channel_id", "channel_sk"]],
    how="left",
    on="channel_id"
)

# Store
fact = fact.merge(
    dim_store[["store_id", "store_sk"]],
    how="left",
    on="store_id"
)

# Billing Address
fact = fact.merge(
    dim_address[["address_id", "address_sk"]].rename(columns={"address_sk": "billing_address_sk"}),
    how="left",
    left_on="billing_address_id",
    right_on="address_id"
).drop(columns=["address_id"])

# Shipping Address
fact = fact.merge(
    dim_address[["address_id", "address_sk"]].rename(columns={"address_sk": "shipping_address_sk"}),
    how="left",
    left_on="shipping_address_id",
    right_on="address_id"
).drop(columns=["address_id"])

# Fecha (order_date → date_sk)
fact["order_date_norm"] = fact["order_date"].dt.normalize()
fact = fact.merge(
    dim_calendar[["date", "date_sk"]],
    how="left",
    left_on="order_date_norm",
    right_on="date"
)
fact = fact.rename(columns={"date_sk": "order_date_sk"})

# --- REEMPLAZAR NULOS POR 0 (late-arriving dimensions) ---
for col in ["customer_sk", "product_sk", "channel_sk", "store_sk",
            "billing_address_sk", "shipping_address_sk", "order_date_sk"]:
    fact[col] = fact[col].fillna(0).astype(int)

# --- SELECCIÓN FINAL DE COLUMNAS ---
cols = [
    "order_item_sk", "order_item_id", "order_id",
    "order_date_sk",
    "customer_sk", "product_sk", "channel_sk", "store_sk",
    "billing_address_sk", "shipping_address_sk",
    "status", "currency_code",
    "quantity", "unit_price", "discount_amount",
    "gross_amount", "net_amount", "subtotal",
    "tax_amount", "shipping_fee", "total_amount"
]
fact = fact[cols]

# --- EXPORTAR ---
fact.to_csv(DW / "fact_order_item_enriched.csv", index=False)
print("✅ fact_order_item_enriched creada en /DW/fact_order_item_enriched.csv")
