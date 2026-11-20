# =====================================================
# INVENTORY CLASS
# Keeps the list of products and can add, search, update stock and display them.
# Does not maninpulate product details/data. It asks the Product to do it.
# =====================================================

from product import Product
from product_factory import product_from_dict

class Inventory:
    def __init__(self):
        self.__products = []
        self.__transactions = []
        self.__total_transaction_amount = 0

    def __record_transaction(self, amount):
        self.__transactions.append(amount)
        self.__total_transaction_amount += amount

    def validate_new_product_id(self, product_id):
        product_id = Product.validate_product_id(product_id)

        if self.search_product(product_id) is not None:
            raise ValueError(
                f"Product ID '{product_id}' already exists."
            )

        return product_id

    def add_product(self, product):
        if any(
            p.product_id.casefold() == product.product_id.casefold()
            for p in self.__products
        ):
            raise ValueError(
                f"Product ID '{product.product_id}' already exists."
            )

        self.__products.append(product)
        self.__record_transaction(product.stock)

    def search_product(self, query):
        return next(
            (p for p in self.__products if p.matches(query)),
            None
        )

    def update_stock(self, query, new_quantity):
        product = self.search_product(query)

        if product is None:
            return None

        change = product.update_stock(new_quantity)
        self.__record_transaction(change)

        return product

    def display_all(self):
        print("Current Inventory")
        print("-" * 48)

        if not self.__products:
            print(" " * 14 + "Inventory is empty.")
        else:
            for product in self.__products:
                product.display_information()

        print("-" * 48)

    def to_dict(self):
        return {
            "products": [p.to_dict() for p in self.__products],
            "transactions": list(self.__transactions),
            "total_transaction_amount": self.__total_transaction_amount
        }

    @classmethod
    def from_dict(cls, data):
        inventory = cls()

        for index, item in enumerate(
            data.get("products", []), start=1
        ):
            inventory.__products.append(
                product_from_dict(item, f"P{index:03d}")
            )

        inventory.__transactions = data.get("transactions", [])
        inventory.__total_transaction_amount = data.get(
            "total_transaction_amount", 0
        )

        return inventory