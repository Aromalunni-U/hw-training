
products = [
    {"name": "Laptop", "price": 10000},
    {"name": "Phone", "price": None},
    {"name": "Speaker", "price": 5000},
    {"name": "Monitor", "price": None},
    {"name": "Keyboard", "price": 300}
]

product_name = [product["name"] for product in products]
print(product_name)


valid_products = [product["name"] for product in products if product["price"] is not None]
print(valid_products)