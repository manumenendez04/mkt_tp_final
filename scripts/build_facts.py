import pandas as pd
from etl_utils import read_csv, write_parquet
import numpy as np

# Mappings
prod_map  = pd.read_parquet("DW/map_product.parquet")
cust_map  = pd.read_parquet("DW/map_customer.parquet")
store_map = pd.read_parquet("DW/map_store.parquet")
chan_map  = pd.read_parquet("DW/map_channel.parquet")
addr_map  = pd.read_parquet("DW/map_address.parquet")
dim_date  = pd.read_parquet("DW/dim_date.parquet")[["date","date_sk"]]

# RAW necesarios
items  = read_csv("sales_order_item.csv",
                  dtype={"order_item_id":"int64","order_id":"int64","product_id":"Int64","qty":"Int64"},
                  parse_dates=None)
orders = read_csv("sales_order.csv",
                  dtype={"order_id":"int64","customer_id":"Int64","store_id":"Int64","channel_id":"Int64","billing_address_id":"Int64","shipping_address_id":"Int64"},
                  parse_dates=["order_date"])

# Join items + orders
fact = items.merge(orders[["order_id","customer_id","store_id","channel_id","order_date"]], on="order_id", how="left")

# Date surrogate
fact = fact.merge(dim_date.rename(columns={"date":"order_date"}), how="left", on="order_date").rename(columns={"date_sk":"order_date_sk"})

# Mapear surrogate keys
fact = fact.merge(prod_map,  how="left", on="product_id").rename(columns={"product_sk":"product_sk"})
fact = fact.merge(cust_map,  how="left", on="customer_id").rename(columns={"customer_sk":"customer_sk"})
fact = fact.merge(store_map, how="left", on="store_id").rename(columns={"store_sk":"store_sk"})
fact = fact.merge(chan_map,  how="left", on="channel_id").rename(columns={"channel_sk":"channel_sk"})

# Métricas (ajusta nombres a tus columnas reales)
# Supongo que en sales_order_item hay unit_price y disc_total; si no, reemplazá por las correctas.
for col in ["unit_price","disc_total"]:
    if col not in fact.columns:
        fact[col] = 0.0

fact["gross_amount"] = fact["qty"].fillna(0).astype("float64") * fact["unit_price"].astype("float64")
fact["net_amount"]   = fact["gross_amount"] - fact["disc_total"].astype("float64")

# Completar SK faltantes con 0
for col in ["product_sk","customer_sk","store_sk","channel_sk","order_date_sk"]:
    fact[col] = fact[col].fillna(0).astype("int64")

# Selección final de columnas
fact_cols = [
    "order_item_id","order_id",
    "product_sk","customer_sk","store_sk","channel_sk","order_date_sk",
    "qty","unit_price","disc_total","gross_amount","net_amount"
]
write_parquet(fact[fact_cols], "fact_order_item")
