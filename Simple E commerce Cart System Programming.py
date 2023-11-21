from abc import ABC, abstractmethod
from copy import deepcopy

# Strategy Pattern for Discount
class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, price, quantity):
        pass

class PercentageOffDiscount(DiscountStrategy):
    def __init__(self, percentage):
        self.percentage = percentage

    def apply_discount(self, price, quantity):
        return price * quantity * (1 - self.percentage / 100)

class BuyOneGetOneFreeDiscount(DiscountStrategy):
    def apply_discount(self, price, quantity):
        return (quantity // 2) * price + (quantity % 2) * price

# Prototype Pattern for Product
class ProductPrototype(ABC):
    @abstractmethod
    def clone(self):
        pass

class Product(ProductPrototype):
    def __init__(self, name, price, available=True):
        self.name = name
        self.price = price
        self.available = available

    def clone(self):
        return deepcopy(self)

# Cart Item
class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

# Shopping Cart
class ShoppingCart:
    def __init__(self, discount_strategy):
        self.items = []
        self.discount_strategy = discount_strategy

    def add_item(self, product, quantity):
        cart_item = CartItem(product.clone(), quantity)
        self.items.append(cart_item)

    def update_quantity(self, product_name, quantity):
        for item in self.items:
            if item.product.name == product_name:
                item.quantity = quantity
                return
        print(f"{product_name} not found in the cart.")

    def remove_item(self, product_name):
        self.items = [item for item in self.items if item.product.name != product_name]

    def calculate_total_bill(self):
        total_bill = sum(self.discount_strategy.apply_discount(item.product.price, item.quantity) for item in self.items)
        return total_bill

    def display_cart(self):
        item_descriptions = [f"{item.quantity} {item.product.name}" for item in self.items]
        print(f"You have {', '.join(item_descriptions)} in your cart.")

# Example Usage with User Input for Products
if __name__ == "__main__":
    discount_strategy = PercentageOffDiscount(5)  # 5% off discount strategy
    cart = ShoppingCart(discount_strategy)

    products = []
    while True:
        product_name = input("Enter product name (or 'done' to finish): ")
        if product_name.lower() == 'done':
            break

        price = float(input("Enter product price: "))
        available = input("Is the product available? (yes/no): ").lower() == 'yes'

        product = Product(product_name, price, available)
        products.append(product)

    for product in products:
        print(f"Product added: {product.name} - Price: ${product.price} - Available: {product.available}")

    while True:
        print("\nMenu:")
        print("1. Add Product to Cart")
        print("2. Update Quantity")
        print("3. Remove Product from Cart")
        print("4. View Cart")
        print("5. Calculate Total Bill")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            product_name = input("Enter product name: ")
            quantity = int(input("Enter quantity: "))

            selected_product = next((product for product in products if product.name == product_name), None)
            if selected_product:
                cart.add_item(selected_product, quantity)
                print("Product added to the cart.")
            else:
                print(f"{product_name} not found in the available products.")

        elif choice == "2":
            product_name = input("Enter product name to update quantity: ")
            quantity = int(input("Enter new quantity: "))
            cart.update_quantity(product_name, quantity)

        elif choice == "3":
            product_name = input("Enter product name to remove from the cart: ")
            cart.remove_item(product_name)

        elif choice == "4":
            cart.display_cart()

        elif choice == "5":
            total_bill = cart.calculate_total_bill()
            print(f"Your total bill is ${total_bill}.")

        elif choice == "6":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
