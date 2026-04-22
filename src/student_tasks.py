from pathlib import Path

import pandas as pd


def create_store_reference() -> pd.DataFrame:
    """
    Build a DataFrame from scratch with these exact values and index labels.

    Index name: store_id
    Index labels: S001, S002, S003

    Columns:
    - store_name
    - city
    - region
    - store_count

    Rows:
    - S001, Centro, Monterrey, North, 1
    - S002, Plaza, Guadalajara, West, 2
    - S003, Alameda, Merida, South, 1
    """
    # TODO: Replace the placeholder implementation.

    store_reference = pd.DataFrame(
        {
            "store_name": ["Centro", "Plaza", "Alameda"],
            "city": ["Monterrey", "Guadalajara", "Merida"],
            "region": ["North", "West", "South"],
            "store_count": [1, 2, 1],
        },
        index=["S001", "S002", "S003"],
    )
    store_reference.index.name = "store_id"
    return store_reference



def load_raw_datasets(data_dir: str | Path = "data/raw") -> tuple[pd.DataFrame, ...]:
    """
    Load the four raw CSV files using pd.read_csv only.

    Return them in this exact order:
    customers, products, orders, order_items
    """
    # TODO: Replace the placeholder implementation.
    data_dir = Path(data_dir)

    customers = pd.read_csv(data_dir / "customers.csv")
    products = pd.read_csv(data_dir / "products.csv")
    orders = pd.read_csv(data_dir / "orders.csv")
    order_items = pd.read_csv(data_dir / "order_items.csv")

    return customers, products, orders, order_items


def filter_high_value_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """
    Return orders that match all of these conditions:

    - total_amount is at least 200
    - status is either Delivered or Shipped
    - payment_method is not Cash

    Return only these columns in this order:
    order_id, customer_id, status, payment_method, total_amount

    Sort by total_amount descending, then order_id ascending.
    Reset the index before returning.
    """
    # TODO: Replace the placeholder implementation.
    raise NotImplementedError("Implement filter_high_value_orders")


def create_order_features(orders: pd.DataFrame) -> pd.DataFrame:
    """
    Return a transformed copy of orders with the following steps:

    1. Convert order_date to datetime.
    2. Rename total_amount to order_total.
    3. Create order_month as a YYYY-MM string.
    4. Create is_high_value where order_total >= 250.
    5. Create discount_rate using any clear logic you prefer:
       - SAVE10 -> 0.10
       - WELCOME5 -> 0.05
       - any other coupon or missing coupon -> 0.00
    6. Create discounted_total = order_total * (1 - discount_rate), rounded to 2 decimals.
    7. Drop the notes column.

    Keep the remaining columns.
    """
    # TODO: Replace the placeholder implementation.
    raise NotImplementedError("Implement create_order_features")


def merge_customers_orders(
    customers: pd.DataFrame, orders: pd.DataFrame, how: str = "left"
) -> pd.DataFrame:
    """
    Merge customers with orders on customer_id using pd.merge.

    Parameters:
    - customers: the left DataFrame
    - orders: the right DataFrame
    - how: left, inner, or right

    Return the merged DataFrame sorted by customer_id and order_id, with the index reset.
    """
    # TODO: Replace the placeholder implementation.
    raise NotImplementedError("Implement merge_customers_orders")


def concat_contact_directory(customers: pd.DataFrame) -> pd.DataFrame:
    """
    Build two small DataFrames and concatenate them with pd.concat:

    1. email_contacts with columns:
       customer_id, contact_type, contact_value
       where contact_type is 'email' and contact_value comes from email

    2. city_contacts with columns:
       customer_id, contact_type, contact_value
       where contact_type is 'city' and contact_value comes from city

    Concatenate them in that order, reset the index, and return the result.
    """
    # TODO: Replace the placeholder implementation.
    raise NotImplementedError("Implement concat_contact_directory")


def clean_orders_missing_values(orders: pd.DataFrame) -> pd.DataFrame:
    """
    Return a cleaned copy of orders with these rules:

    1. Convert order_date to datetime.
    2. Drop rows missing customer_id or order_date.
    3. Fill missing shipping_city with 'Unknown'.
    4. Fill missing total_amount with 0.
    5. Fill missing notes with 'No notes'.
    6. Create has_coupon using notna on coupon_code.
    7. Drop exact duplicate rows.
    8. Sort by order_date, then order_id, and reset the index.
    """
    # TODO: Replace the placeholder implementation.
    raise NotImplementedError("Implement clean_orders_missing_values")


def summarize_customer_sales_by_month(
    customers: pd.DataFrame, orders: pd.DataFrame
) -> pd.DataFrame:
    """
    Build a monthly customer summary for delivered orders only.

    Steps:
    - convert order_date to datetime
    - keep rows where status == 'Delivered'
    - merge orders with customers using an inner join on customer_id
    - create order_month as the month start timestamp
    - group by customer_id, customer_name, and order_month
    - aggregate:
      total_revenue = sum of total_amount
      average_order_value = mean of total_amount
      order_count = count of order_id

    Sort by customer_id and order_month, then reset the index.
    """
    # TODO: Replace the placeholder implementation.
    raise NotImplementedError("Implement summarize_customer_sales_by_month")


def build_category_sales_pivot(
    order_items: pd.DataFrame, products: pd.DataFrame
) -> pd.DataFrame:
    """
    Create a pivot table after merging order_items with products on product_id.

    Requirements:
    - use a left merge
    - index should be category
    - columns should be brand
    - values should be line_total
    - aggfunc should be sum
    - fill missing values with 0

    Sort the index before returning.
    """
    # TODO: Replace the placeholder implementation.
    raise NotImplementedError("Implement build_category_sales_pivot")
