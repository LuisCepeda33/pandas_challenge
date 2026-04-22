from pathlib import Path

import numpy as np
import pandas as pd


SEED = 20260415


def _build_customers(rng: np.random.Generator) -> pd.DataFrame:
    names = [
        ("Ana Lopez", "Monterrey", "Nuevo Leon"),
        ("Diego Ruiz", "Guadalajara", "Jalisco"),
        ("Sofia Martinez", "Mexico City", "CDMX"),
        ("Carlos Vega", "Puebla", "Puebla"),
        ("Elena Torres", "Merida", "Yucatan"),
        ("Luis Herrera", "Queretaro", "Queretaro"),
        ("Valeria Diaz", "Tijuana", "Baja California"),
        ("Jorge Campos", "Saltillo", "Coahuila"),
        ("Mariana Silva", "Aguascalientes", "Aguascalientes"),
        ("Ricardo Nunez", "Leon", "Guanajuato"),
        ("Fernanda Cruz", "Toluca", "Estado de Mexico"),
        ("Pablo Reyes", "Chihuahua", "Chihuahua"),
        ("Natalia Mora", "San Luis Potosi", "San Luis Potosi"),
        ("Ivan Castillo", "Cancun", "Quintana Roo"),
        ("Camila Ortega", "Culiacan", "Sinaloa"),
        ("Mateo Flores", "Veracruz", "Veracruz"),
        ("Daniela Ramos", "Oaxaca", "Oaxaca"),
        ("Hugo Medina", "Hermosillo", "Sonora"),
    ]

    signup_dates = pd.date_range("2023-01-05", periods=len(names), freq="17D")
    segments = ["Consumer", "Small Business", "Corporate"]
    loyalty_tiers = ["Bronze", "Silver", "Gold"]

    rows = []
    for index, (customer_name, city, state) in enumerate(names, start=1):
        customer_id = f"C{index:03d}"
        email_name = customer_name.lower().replace(" ", ".")
        rows.append(
            {
                "customer_id": customer_id,
                "customer_name": customer_name,
                "city": city,
                "state": state,
                "signup_date": signup_dates[index - 1].strftime("%Y-%m-%d"),
                "email": f"{email_name}@example.com",
                "segment": segments[(index - 1) % len(segments)],
                "loyalty_tier": loyalty_tiers[rng.integers(0, len(loyalty_tiers))],
                "is_active": bool(rng.integers(0, 2)),
            }
        )

    customers = pd.DataFrame(rows)
    customers.loc[[2, 8], "email"] = np.nan
    customers.loc[[4, 11], "loyalty_tier"] = np.nan
    customers.loc[15, "segment"] = np.nan
    return customers


def _build_products(rng: np.random.Generator) -> pd.DataFrame:
    base_rows = [
        ("P001", "Electronics", "Wireless Mouse", "NovaTech", 24.90),
        ("P002", "Electronics", "USB-C Hub", "NovaTech", 39.90),
        ("P003", "Home", "Desk Lamp", "CasaPlus", 32.50),
        ("P004", "Home", "Storage Basket", "CasaPlus", 18.00),
        ("P005", "Fitness", "Yoga Mat", "MoveWell", 27.50),
        ("P006", "Fitness", "Water Bottle", "MoveWell", 14.00),
        ("P007", "Office", "Notebook Set", "PaperTrail", 12.50),
        ("P008", "Office", "Gel Pens", "PaperTrail", 9.75),
        ("P009", "Kitchen", "Coffee Grinder", "BrewLab", 49.90),
        ("P010", "Kitchen", "Travel Mug", "BrewLab", 21.00),
    ]

    products = pd.DataFrame(
        base_rows,
        columns=["product_id", "category", "product_name", "brand", "unit_price"],
    )
    products["is_active"] = rng.choice([True, True, True, False], size=len(products))
    return products


def _build_orders(rng: np.random.Generator, customers: pd.DataFrame) -> pd.DataFrame:
    statuses = ["Delivered", "Shipped", "Pending", "Cancelled"]
    channels = ["Online", "Mobile App", "Store"]
    payment_methods = ["Card", "Transfer", "Cash"]
    coupon_codes = [None, None, None, "SAVE10", "WELCOME5", "FREESHIP"]
    notes = [None, None, "Gift order", "Call before delivery", "Fragile"]

    start = pd.Timestamp("2024-01-01")
    rows = []

    for index in range(1, 61):
        order_date = start + pd.Timedelta(days=int(rng.integers(0, 120)))
        customer_id = customers.loc[rng.integers(0, len(customers)), "customer_id"]
        total_amount = float(np.round(rng.uniform(35, 420), 2))
        rows.append(
            {
                "order_id": f"O{index:04d}",
                "customer_id": customer_id,
                "order_date": order_date.strftime("%Y-%m-%d"),
                "status": rng.choice(statuses, p=[0.48, 0.22, 0.22, 0.08]),
                "sales_channel": rng.choice(channels, p=[0.58, 0.24, 0.18]),
                "payment_method": rng.choice(payment_methods, p=[0.67, 0.20, 0.13]),
                "shipping_city": rng.choice(customers["city"]),
                "coupon_code": rng.choice(coupon_codes),
                "notes": rng.choice(notes),
                "total_amount": total_amount,
            }
        )

    orders = pd.DataFrame(rows)
    orders.loc[[5, 17, 41], "shipping_city"] = np.nan
    orders.loc[[7, 21], "total_amount"] = np.nan
    orders.loc[12, "order_date"] = np.nan
    orders.loc[18, "customer_id"] = "C999"
    duplicate_row = orders.iloc[[10]].copy()
    orders = pd.concat([orders, duplicate_row], ignore_index=True)
    return orders


def _build_order_items(
    rng: np.random.Generator, orders: pd.DataFrame, products: pd.DataFrame
) -> pd.DataFrame:
    rows = []
    usable_orders = orders.drop_duplicates(subset=["order_id"])

    for order_id in usable_orders["order_id"]:
        line_count = int(rng.integers(1, 4))
        selected_products = rng.choice(products["product_id"], size=line_count, replace=False)
        for product_id in selected_products:
            product_row = products.loc[products["product_id"] == product_id].iloc[0]
            quantity = int(rng.integers(1, 5))
            discount_rate = rng.choice([0.0, 0.0, 0.05, 0.10, np.nan])
            line_total = quantity * product_row["unit_price"]
            if pd.notna(discount_rate):
                line_total *= 1 - discount_rate
            rows.append(
                {
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": float(product_row["unit_price"]),
                    "discount_rate": discount_rate,
                    "line_total": float(np.round(line_total, 2)),
                }
            )

    order_items = pd.DataFrame(rows)
    order_items.loc[[3, 15], "line_total"] = np.nan
    duplicate_row = order_items.iloc[[2]].copy()
    order_items = pd.concat([order_items, duplicate_row], ignore_index=True)
    return order_items


def generate_all_datasets(output_dir: Path | str | None = None) -> dict[str, Path]:
    rng = np.random.default_rng(SEED)

    if output_dir is None:
        output_path = Path(__file__).resolve().parents[1] / "data" / "raw"
    else:
        output_path = Path(output_dir)

    output_path.mkdir(parents=True, exist_ok=True)

    customers = _build_customers(rng)
    products = _build_products(rng)
    orders = _build_orders(rng, customers)
    order_items = _build_order_items(rng, orders, products)

    datasets = {
        "customers.csv": customers,
        "products.csv": products,
        "orders.csv": orders,
        "order_items.csv": order_items,
    }

    saved_paths: dict[str, Path] = {}
    for filename, dataframe in datasets.items():
        destination = output_path / filename
        dataframe.to_csv(destination, index=False)
        saved_paths[filename] = destination

    return saved_paths
