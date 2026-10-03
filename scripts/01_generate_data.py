import numpy as np  # type: ignore
import pandas as pd  # type: ignore

# Setting seed for analytical reproducibility
np.random.seed(42)

# 1. Distribution Centers Dimension (10 CDs)
cds = [
    {
        "cd_id": i,
        "cd_name": f"CD_Region_{i:02d}",
        "area_m2": np.random.randint(5000, 25000),
        "base_operating_cost": np.random.uniform(50000, 150000),
    }
    for i in range(1, 11)
]
df_cd = pd.DataFrame(cds)

# 2. Vehicle Fleet Dimension (100 Proprietary Trucks)
vehicle_types = [
    "Small Truck",
    "Medium Truck",
    "Simple Trailer",
    "Refrigerated Trailer",
]
fleet = []
for i in range(1, 101):
  v_type = np.random.choice(vehicle_types, p=[0.3, 0.4, 0.2, 0.1])
  if v_type == "Small Truck":
    weight_cap, vol_cap = 5000, 30
  elif v_type == "Medium Truck":
    weight_cap, vol_cap = 12000, 60
  elif v_type == "Simple Trailer":
    weight_cap, vol_cap = 25000, 95
  else:  # Refrigerated Trailer
    weight_cap, vol_cap = 22000, 85

  fleet.append({
      "vehicle_id": i,
      "vehicle_type": v_type,
      "max_weight_kg": weight_cap,
      "max_volume_m3": vol_cap,
      "cost_per_km": np.random.uniform(4.5, 9.2),
  })
df_fleet = pd.DataFrame(fleet)

# 3. Products Dimension (Mix of different storage requirements)
storage_categories = ["Standard", "Fragile", "Perishable/Cold", "Hazmat"]
products = []
for i in range(1, 201):
  requirement = np.random.choice(storage_categories, p=[0.5, 0.2, 0.2, 0.1])
  products.append({
      "product_id": i,
      "product_name": f"Product_{i:03d}",
      "storage_category": requirement,
      "cube_factor": np.random.uniform(0.1, 0.5),
  })
df_product = pd.DataFrame(products)

# 4. Deliveries Fact Table (15,000 records simulating operational bottlenecks)
n_rows = 15000
timestamps = pd.date_range(start="2025-01-01", end="2025-12-31", freq="h")

transaction_ids = range(100000, 100000 + n_rows)
sample_dates = np.random.choice(timestamps, n_rows)
sample_cds = np.random.randint(1, 11, n_rows)
sample_vehicles = np.random.randint(1, 101, n_rows)
sample_products = np.random.randint(1, 201, n_rows)

transported_weight = np.random.uniform(1000, 20000, n_rows)
transported_volume = np.random.uniform(10, 80, n_rows)
distance_km = np.random.uniform(50, 1200, n_rows)

# Simulated logic for logistics delays and bottlenecks
delay_hours = np.random.exponential(scale=3, size=n_rows) * (
    distance_km / 500
)
on_time_status = np.where(delay_hours < 4, 1, 0)
in_full_status = np.random.choice([1, 0], size=n_rows, p=[0.88, 0.12])

df_fact = pd.DataFrame({
    "transaction_id": transaction_ids,
    "shipping_date": sample_dates,
    "cd_id": sample_cds,
    "vehicle_id": sample_vehicles,
    "product_id": sample_products,
    "transported_weight_kg": transported_weight,
    "transported_volume_m3": transported_volume,
    "distance_km": distance_km,
    "delay_hours": delay_hours,
    "on_time_status": on_time_status,
    "in_full_status": in_full_status,
    "estimated_freight_cost": distance_km * np.random.uniform(5, 12),
})

# Exporting CSV files to the /data folder
df_cd.to_csv("data/dim_cd.csv", index=False)
df_fleet.to_csv("data/dim_fleet.csv", index=False)
df_product.to_csv("data/dim_product.csv", index=False)
df_fact.to_csv("data/fact_deliveries.csv", index=False)

print("ETL pipeline executed successfully! CSV files generated in /data.")