from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from src.student_tasks import (
    build_category_sales_pivot,
    clean_orders_missing_values,
    concat_contact_directory,
    load_raw_datasets,
    merge_customers_orders,
    summarize_customer_sales_by_month,
)


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"


def _load():
    return load_raw_datasets(RAW_DIR)


def test_merge_customers_orders_matches_left_join():
    customers, _, orders, _ = _load()
    result = merge_customers_orders(customers, orders, how="left")
    expected = pd.merge(customers, orders, on="customer_id", how="left")
    expected = expected.sort_values(["customer_id", "order_id"], na_position="last").reset_index(drop=True)
    assert_frame_equal(result, expected, check_dtype=False)


def test_merge_customers_orders_matches_right_join():
    customers, _, orders, _ = _load()
    result = merge_customers_orders(customers, orders, how="right")
    expected = pd.merge(customers, orders, on="customer_id", how="right")
    expected = expected.sort_values(["customer_id", "order_id"], na_position="last").reset_index(drop=True)
    assert_frame_equal(result, expected, check_dtype=False)


def test_concat_contact_directory_matches_expected_result():
    customers, _, _, _ = _load()

    email_contacts = customers[["customer_id", "email"]].copy()
    email_contacts["contact_type"] = "email"
    email_contacts = email_contacts.rename(columns={"email": "contact_value"})
    email_contacts = email_contacts[["customer_id", "contact_type", "contact_value"]]

    city_contacts = customers[["customer_id", "city"]].copy()
    city_contacts["contact_type"] = "city"
    city_contacts = city_contacts.rename(columns={"city": "contact_value"})
    city_contacts = city_contacts[["customer_id", "contact_type", "contact_value"]]

    expected = pd.concat([email_contacts, city_contacts], ignore_index=True)
    result = concat_contact_directory(customers)
    assert_frame_equal(result, expected)


def test_clean_orders_missing_values_matches_expected_cleanup():
    _, _, orders, _ = _load()

    expected = orders.copy()
    expected["order_date"] = pd.to_datetime(expected["order_date"])
    expected = expected.dropna(subset=["customer_id", "order_date"])
    expected["shipping_city"] = expected["shipping_city"].fillna("Unknown")
    expected["total_amount"] = expected["total_amount"].fillna(0)
    expected["notes"] = expected["notes"].fillna("No notes")
    expected["has_coupon"] = expected["coupon_code"].notna()
    expected = expected.drop_duplicates()
    expected = expected.sort_values(["order_date", "order_id"]).reset_index(drop=True)

    result = clean_orders_missing_values(orders)
    assert_frame_equal(result, expected, check_dtype=False)


def test_monthly_customer_summary_matches_expected_groupby():
    customers, _, orders, _ = _load()

    expected_orders = orders.copy()
    expected_orders["order_date"] = pd.to_datetime(expected_orders["order_date"])
    expected_orders = expected_orders[expected_orders["status"] == "Delivered"]
    expected_orders = expected_orders.dropna(subset=["order_date"])

    expected = pd.merge(expected_orders, customers, on="customer_id", how="inner")
    expected["order_month"] = expected["order_date"].values.astype("datetime64[M]")
    expected = (
        expected.groupby(["customer_id", "customer_name", "order_month"], dropna=False)
        .agg(
            total_revenue=("total_amount", "sum"),
            average_order_value=("total_amount", "mean"),
            order_count=("order_id", "count"),
        )
        .reset_index()
        .sort_values(["customer_id", "order_month"])
        .reset_index(drop=True)
    )

    result = summarize_customer_sales_by_month(customers, orders)
    assert_frame_equal(result, expected, check_dtype=False)


def test_category_sales_pivot_matches_expected_pivot():
    _, products, _, order_items = _load()

    expected = pd.merge(order_items, products, on="product_id", how="left")
    expected = pd.pivot_table(
        expected,
        index="category",
        columns="brand",
        values="line_total",
        aggfunc="sum",
        fill_value=0,
    )
    expected = expected.sort_index()

    result = build_category_sales_pivot(order_items, products)
    assert_frame_equal(result, expected, check_dtype=False)
