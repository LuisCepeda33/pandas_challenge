from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from src.student_tasks import create_order_features, filter_high_value_orders, load_raw_datasets


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"


def _expected_filter(orders: pd.DataFrame) -> pd.DataFrame:
    expected = orders[
        (orders["total_amount"] >= 200)
        & (orders["status"].isin(["Delivered", "Shipped"]))
        & (orders["payment_method"] != "Cash")
    ][["order_id", "customer_id", "status", "payment_method", "total_amount"]]
    expected = expected.sort_values(["total_amount", "order_id"], ascending=[False, True])
    return expected.reset_index(drop=True)


def _expected_features(orders: pd.DataFrame) -> pd.DataFrame:
    expected = orders.copy()
    expected["order_date"] = pd.to_datetime(expected["order_date"])
    expected = expected.rename(columns={"total_amount": "order_total"})
    expected["order_month"] = expected["order_date"].dt.strftime("%Y-%m")
    expected["is_high_value"] = expected["order_total"] >= 250
    discount_map = {"SAVE10": 0.10, "WELCOME5": 0.05, "FREESHIP": 0.00}
    expected["discount_rate"] = expected["coupon_code"].map(discount_map).fillna(0.00)
    expected["discounted_total"] = (expected["order_total"] * (1 - expected["discount_rate"])).round(2)
    expected = expected.drop(columns=["notes"])
    return expected


def test_filter_high_value_orders_matches_expected_rows():
    _, _, orders, _ = load_raw_datasets(RAW_DIR)
    result = filter_high_value_orders(orders)
    expected = _expected_filter(orders)
    assert_frame_equal(result, expected)


def test_create_order_features_matches_expected_transformations():
    _, _, orders, _ = load_raw_datasets(RAW_DIR)
    result = create_order_features(orders)
    expected = _expected_features(orders)
    assert_frame_equal(result, expected, check_dtype=False)
