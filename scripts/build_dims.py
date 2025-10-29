import pandas as pd
from dateutil.relativedelta import relativedelta
from etl_utils import read_csv, write_parquet, make_surrogate_keys

# 1) Cargar tablas necesarias
customers  = read_csv("customer.csv", parse_dates=["created_at"], dtype={"customer_id":"int64"})
products   = read_csv("product.csv",  parse_dates=["created_at"], dtype={"product_id":"int64","category_id":"Int64"})
stores     = read_csv("store.csv",    dtype={"store_id":"int64","address_id":"Int64"})
channels   = read_csv("channel.csv",  dtype={"channel_id":"int64"})
addresses  = read_csv("address.csv",  parse_dates=["created_at"], dtype={"address_id":"int64","province_id":"Int64"})
provinces  = read_csv("province.csv", dtype={"province_id":"int64"})

orders     = read_csv("sales_order.csv",
                      parse_dates=["order_date","created_at"],
                      dtype={"order_id":"int64","customer_id":"Int64","store_id":"Int64","channel_id":"Int64"})

shipments  = read_csv("shipment.csv", parse_dates=["shipped_at","delivered_at"], dtype={"shipment_id":"int64","order_id":"int64"})
payments   = read_csv("payment.csv",  parse_dates=["paid_at"], dtype={"payment_id":"int64","order_id":"int64"})
nps        = read_csv("nps_response.csv", parse_dates=["responded_at"], dtype={"nps_id":"int64","customer_id":"Int64"})

# 2) dim_date (a partir de TODAS las fechas)
date_cols = []
for df, cols in [(orders,["order_date","created_at"]),
                 (shipments,["shipped_at","delivered_at"]),
                 (payments,["paid_at"]),
                 (customers,["created_at"]),
                 (addresses,["created_at"]),
                 (nps,["responded_at"])]:
    for c in cols:
        if c in df.columns:
            date_cols.append(df[c])

dates = pd.concat(date_cols, ignore_index=True).dropna().dt.normalize().drop_duplicates().to_frame(name="date")
if dates.empty:
    dates = pd.DataFrame({"date": pd.date_range("2019-01-01","2025-12-31", freq="D")})

dim_date = dates.copy()
dim_date["date_sk"]     = (dim_date["date"].view("int64") // 10**9 // 86400).astype("int64")  # o usa rango 1..n si preferís
dim_date["year"]        = dim_date["date"].dt.year
dim_date["month"]       = dim_date["date"].dt.month
dim_date["day"]         = dim_date["date"].dt.day
dim_date["year_month"]  = dim_date["date"].dt.strftime("%Y-%m")
dim_date["quarter"]     = "Q" + ((dim_date["month"]-1)//3 + 1).astype(str)
dim_date["dow"]         = dim_date["date"].dt.weekday + 1  # 1..7
dim_date["is_weekend"]  = dim_date["dow"].isin([6,7]).astype("int8")

write_parquet(dim_date, "dim_date")

# 3) dim_product
prod_cols = ["product_id","sku","name","category_id","status","created_at"]
dim_product = products[prod_cols].drop_duplicates().copy()
prod_map = make_surrogate_keys(dim_product, "product_id", "product_sk")
dim_product = dim_product.merge(prod_map, on="product_id")
write_parquet(dim_product[["product_sk"]+prod_cols], "dim_product")
prod_map.to_parquet("DW/map_product.parquet", index=False)

# 4) dim_customer
cust_cols = ["customer_id","email","first_name","last_name","status","created_at"]
dim_customer = customers[cust_cols].drop_duplicates().copy()
cust_map = make_surrogate_keys(dim_customer, "customer_id", "customer_sk")
dim_customer = dim_customer.merge(cust_map, on="customer_id")
write_parquet(dim_customer[["customer_sk"]+cust_cols], "dim_customer")
cust_map.to_parquet("DW/map_customer.parquet", index=False)

# 5) dim_store
store_cols = ["store_id","name","address_id"]
dim_store = stores[store_cols].drop_duplicates().copy()
store_map = make_surrogate_keys(dim_store, "store_id", "store_sk")
dim_store = dim_store.merge(store_map, on="store_id")
write_parquet(dim_store[["store_sk"]+store_cols], "dim_store")
store_map.to_parquet("DW/map_store.parquet", index=False)

# 6) dim_channel
chan_cols = ["channel_id","code","name"]
dim_channel = channels[chan_cols].drop_duplicates().copy()
chan_map = make_surrogate_keys(dim_channel, "channel_id", "channel_sk")
dim_channel = dim_channel.merge(chan_map, on="channel_id")
write_parquet(dim_channel[["channel_sk"]+chan_cols], "dim_channel")
chan_map.to_parquet("DW/map_channel.parquet", index=False)

# 7) (opcional) dim_province + dim_address
prov_map = None
if not provinces.empty:
    prov = provinces[["province_id","name","code"]].drop_duplicates().copy()
    prov_map = make_surrogate_keys(prov, "province_id", "province_sk")
    prov = prov.merge(prov_map, on="province_id")
    write_parquet(prov[["province_sk","province_id","name","code"]], "dim_province")
    prov_map.to_parquet("DW/map_province.parquet", index=False)

addr_cols = ["address_id","line1","city","province_id","postal_code","country_code","created_at"]
dim_address = addresses[addr_cols].drop_duplicates().copy()
addr_map = make_surrogate_keys(dim_address, "address_id", "address_sk")
dim_address = dim_address.merge(addr_map, on="address_id")
if prov_map is not None:
    dim_address = dim_address.merge(prov_map, on="province_id", how="left")
write_parquet(dim_address[["address_sk"]+addr_cols+["province_sk"]], "dim_address")
addr_map.to_parquet("DW/map_address.parquet", index=False)
