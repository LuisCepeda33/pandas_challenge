from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from src.student_tasks import create_store_reference, load_raw_datasets


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"


def test_create_store_reference_matches_expected_table():
    expected = pd.DataFrame(
        {
            "store_name": ["Centro", "Plaza", "Alameda"],
            "city": ["Monterrey", "Guadalajara", "Merida"],
            "region": ["North", "West", "South"],
            "store_count": [1, 2, 1],
        },
        index=["S001", "S002", "S003"],
    )
    expected.index.name = "store_id"

    result = create_store_reference()
    assert_frame_equal(result, expected)


def test_load_raw_datasets_uses_expected_csv_content():
    customers, products, orders, order_items = load_raw_datasets(RAW_DIR)

    expected_customers = pd.read_csv(RAW_DIR / "customers.csv")
    expected_products = pd.read_csv(RAW_DIR / "products.csv")
    expected_orders = pd.read_csv(RAW_DIR / "orders.csv")
    expected_order_items = pd.read_csv(RAW_DIR / "order_items.csv")

    assert_frame_equal(customers, expected_customers)
    assert_frame_equal(products, expected_products)
    assert_frame_equal(orders, expected_orders)
    assert_frame_equal(order_items, expected_order_items)
