# =====================================================
# PRODUCT CLASS (Abstract)
# Common details every product has (ID, name, price, stock)
# =====================================================

import math
from abc import ABC, abstractmethod
from supplier import Supplier
    
class Product(ABC):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier
    ):
        self.__product_id = self.validate_product_id(product_id)
        self.__name = self.validate_name(name)
        self.__price = self.validate_price(price)
        self.__stock = 0
        self.supplier: Supplier = supplier
        self.update_stock(stock)

    @staticmethod
    def validate_product_id(product_id):
        product_id = product_id.strip().upper()

        if not product_id:
            raise ValueError("Product ID cannot be empty.")

        if (
            not product_id.isalnum()
            or not any(c.isalpha() for c in product_id)
            or not any(c.isdigit() for c in product_id)
        ):
            raise ValueError(
                "Product ID must contain only letters and numbers, "
                "including at least one of each."
            )

        return product_id

    @staticmethod
    def validate_name(name):
        name = name.strip()

        if not name:
            raise ValueError("Product name cannot be empty.")

        return name

    @staticmethod
    def validate_price(price):
        if not math.isfinite(price) or price < 0:
            raise ValueError(
                "Price must be a finite, non-negative number."
            )

        return price

    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    def update_stock(self, quantity):
        # Replace current stock with quantity.
        # Returns the change in stock.
        
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

        change = quantity - self.__stock
        self.__stock = quantity

        return change

    def matches(self, query):
        query = query.strip().casefold()

        return query in (
            self.__product_id.casefold(),
            self.__name.casefold()
        )

    def display_information(self):
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}",
            end=""
        )
        print(f"\nSupplier ID: {self.supplier.supplier_id}")
        print(f"Supplier Name: {self.supplier.name}")
        print(f"Supplier Email: {self.supplier.contact_email}")

    def to_dict(self) -> dict:
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.supplier.to_dict()
        }

    @abstractmethod
    def get_fulfilment_info(self):
        # Describe how this product reaches the customer.
        pass
        
