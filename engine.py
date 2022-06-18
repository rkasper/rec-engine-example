import pandas as pd
from tabulate import tabulate


# When a customer puts item #id in their shopping cart,
# which other products should we recommend to them?
def get_recommendations(id):
    print("--- Customer added product #" + str(id) + " to their cart. ---")

    # Our DB of all previous customer orders and products
    products = pd.read_csv("data/Product.csv")
    print("--- Our catalog of products ---")
    print(tabulate(products, headers='keys', tablefmt='psql'))
    orders = pd.read_csv("data/OrderProduct.csv")
    print("--- Our database of all previous customer orders ---")
    print(tabulate(orders, headers='keys', tablefmt='psql'))

    # Previous orders that include the product
    orders_for_product = orders[orders.product_id == id].order_id.unique();
    relevant_orders = orders[orders.order_id.isin(orders_for_product)]
    print("--- Historic orders that include product #" + str(id) + " ---")
    print(tabulate(relevant_orders, headers='keys', tablefmt='psql'))

    # Frequency of other items purchased with this product
    accompanying_products_by_order = relevant_orders[relevant_orders.product_id != id]
    num_instance_by_accompanying_product = accompanying_products_by_order.groupby("product_id")["product_id"].count().reset_index(name="instances")
    print("--- Products that other people bought, and how many times those products were purchased simultaneously with the current product ---")
    print(tabulate(num_instance_by_accompanying_product, headers='keys', tablefmt='psql'))

    # How frequently was each accompanying item purchased?
    num_orders_for_product = orders_for_product.size
    product_instances = pd.DataFrame(num_instance_by_accompanying_product)
    product_instances["frequency"] = product_instances["instances"]/num_orders_for_product
    print("--- How frequently was each accompanying item purchased? ---")
    print(tabulate(num_instance_by_accompanying_product, headers='keys', tablefmt='psql'))

    # Top 3 co-purchased items
    recommended_products = pd.DataFrame(product_instances.sort_values("frequency", ascending=False).head(3))
    print("--- Top 3 co-purchased items ---")
    print(tabulate(recommended_products, headers='keys', tablefmt='psql'))

    # Append more product info
    recommended_products = pd.merge(recommended_products, products, on="product_id")
    print("--- Top 3 co-purchased items, with more product information ---")
    print(tabulate(recommended_products, headers='keys', tablefmt='psql'))

    print("--- A version of this table that is easy for other code to use ---")
    return recommended_products.to_json(orient="table")
    