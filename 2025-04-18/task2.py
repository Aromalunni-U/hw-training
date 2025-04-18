

inventory = {
"apple":30.0,
"orange": 40.5,
"milk":20.5,
"eggs":50.0
}

cart = ["apple","orange","milk"]

print("Inventory :",type(inventory))
print("One price value :",type(list(inventory.values())[0]))
print("Cart :",type(cart))

total_bill = 0
for item in cart:
    if item in inventory:
        n = inventory[item]
        total_bill += n
    else:
        print(item,"Not available")


print("Total bill :",total_bill)

cart = set(cart)

categories = ("fruits", "dairy", "bakery")
print("Product Categories :", categories)
print("Type of category :",type(categories))

inventory["banana"] = None
print(type(inventory["banana"]))

is_discount_applied = False
if total_bill > 100:
    is_discount_applied = True
