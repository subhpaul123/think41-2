import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal
from models.product import Product

df = pd.read_csv("data/products.csv")
session = SessionLocal()

for _, row in df.iterrows():
    product = Product(
        id=row["id"],
        cost=row["cost"],
        category=row["category"],
        name=row["name"],
        brand=row["brand"],
        retail_price=row["retail_price"],
        department=row["department"],
        sku=row["sku"],
        distribution_center_id=row["distribution_center_id"]
    )
    session.merge(product)
session.commit()
session.close()
