from datetime import datetime

PRODUCTS = {
    1: {"name": "Milk", "price": 2.50, "stock": 20},
    2: {"name": "Bread", "price": 1.80, "stock": 25},
    3: {"name": "Eggs", "price": 3.20, "stock": 15},
    4: {"name": "Rice", "price": 12.00, "stock": 10},
    5: {"name": "Chicken", "price": 8.50, "stock": 12},
    6: {"name": "Juice", "price": 2.99, "stock": 18},
}

TAX_RATE = 0.08
DISCOUNT_LIMIT = 50
DISCOUNT_RATE = 0.10

cart = {}


def show_products():
    print("\nAvailable Products")
    print("-" * 45)
    print(f"{'ID':<5}{'Product':<15}{'Price':<10}{'Stock'}")
    print("-" * 45)

    for product_id, item in PRODUCTS.items():
        print(f"{product_id:<5}{item['name']:<15}${item['price']:<9.2f}{item['stock']}")

    print("-" * 45)


def get_number(prompt, number_type=int):
    while True:
        try:
            value = number_type(input(prompt))
            if value <= 0:
                print("Please enter a number greater than 0.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def add_to_cart():
    show_products()

    product_id = get_number("Enter product ID: ")

    if product_id not in PRODUCTS:
        print("Product not found.")
        return

    quantity = get_number("Enter quantity: ")

    product = PRODUCTS[product_id]

    if quantity > product["stock"]:
        print(f"Only {product['stock']} items available in stock.")
        return

    cart[product_id] = cart.get(product_id, 0) + quantity
    product["stock"] -= quantity

    print(f"{quantity} x {product['name']} added to cart.")


def view_cart():
    if not cart:
        print("\nYour cart is empty.")
        return

    print("\nYour Cart")
    print("-" * 50)
    print(f"{'Product':<15}{'Price':<10}{'Qty':<8}{'Total'}")
    print("-" * 50)

    for product_id, quantity in cart.items():
        product = PRODUCTS[product_id]
        total = product["price"] * quantity
        print(f"{product['name']:<15}${product['price']:<9.2f}{quantity:<8}${total:.2f}")

    print("-" * 50)


def remove_from_cart():
    if not cart:
        print("\nYour cart is empty.")
        return

    view_cart()
    product_id = get_number("Enter product ID to remove: ")

    if product_id not in cart:
        print("This product is not in your cart.")
        return

    quantity = get_number("Enter quantity to remove: ")

    if quantity >= cart[product_id]:
        PRODUCTS[product_id]["stock"] += cart[product_id]
        del cart[product_id]
        print("Product removed from cart.")
    else:
        cart[product_id] -= quantity
        PRODUCTS[product_id]["stock"] += quantity
        print("Quantity updated.")


def calculate_bill():
    subtotal = sum(PRODUCTS[pid]["price"] * qty for pid, qty in cart.items())
    discount = subtotal * DISCOUNT_RATE if subtotal >= DISCOUNT_LIMIT else 0
    tax = (subtotal - discount) * TAX_RATE
    total = subtotal - discount + tax

    return subtotal, discount, tax, total


def save_receipt(receipt_text):
    filename = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(filename, "w") as file:
        file.write(receipt_text)

    print(f"Receipt saved as {filename}")


def checkout():
    if not cart:
        print("\nYour cart is empty.")
        return

    subtotal, discount, tax, total = calculate_bill()

    receipt = "\nSHOPPING COUNTER RECEIPT\n"
    receipt += "=" * 50 + "\n"
    receipt += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    receipt += "=" * 50 + "\n"
    receipt += f"{'Product':<15}{'Price':<10}{'Qty':<8}{'Total'}\n"
    receipt += "-" * 50 + "\n"

    for product_id, quantity in cart.items():
        product = PRODUCTS[product_id]
        item_total = product["price"] * quantity
        receipt += f"{product['name']:<15}${product['price']:<9.2f}{quantity:<8}${item_total:.2f}\n"

    receipt += "-" * 50 + "\n"
    receipt += f"Subtotal: ${subtotal:.2f}\n"
    receipt += f"Discount: ${discount:.2f}\n"
    receipt += f"Tax:      ${tax:.2f}\n"
    receipt += f"Total:    ${total:.2f}\n"
    receipt += "=" * 50 + "\n"
    receipt += "Thank you for shopping!\n"

    print(receipt)

    choice = input("Save receipt? (y/n): ").lower()
    if choice == "y":
        save_receipt(receipt)

    cart.clear()


def main():
    while True:
        print("\n====== Shopping Counter System ======")
        print("1. View Products")
        print("2. Add to Cart")
        print("3. View Cart")
        print("4. Remove from Cart")
        print("5. Checkout")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            show_products()
        elif choice == "2":
            add_to_cart()
        elif choice == "3":
            view_cart()
        elif choice == "4":
            remove_from_cart()
        elif choice == "5":
            checkout()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


main()