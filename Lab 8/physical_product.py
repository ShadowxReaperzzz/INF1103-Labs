# =====================================================
# PHYSICAL PRODUCT
# A Product with a weight (kg) that can be shipped.
# Inherits from Product, realises the CanBeShipped interface.
# =====================================================

import math

from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier

class PhysicalProduct(Product, CanBeShipped):
    TYPE = "physical"

    BASE_SHIPPING_COST = 5.00
    COST_PER_KG = 2.00

    def __init__(
    self,
    product_id: str,
    name: str,
    price: float,
    stock: int,
    supplier: Supplier,
    weight: float
    ):
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight = self.validate_weight(weight)

    @staticmethod
    def validate_weight(weight):
        if not math.isfinite(weight) or weight <= 0:
            raise ValueError(
                "Weight must be a finite number greater than zero."
            )

        return weight

    @property
    def weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f" \n[ Type: Physical | Weight: {self.__weight:.2f} kg ]\n")

    def get_fulfilment_info(self):
        return (
            "Physical product: requires packing and shipping "
            f"(shipping cost ${self.calculate_shipping_cost():.2f})."
        )

    def calculate_shipping_cost(self):
        # Flat base fee plus a charge per kilogram.
        return self.BASE_SHIPPING_COST + self.COST_PER_KG * self.__weight

    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.TYPE
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data: dict, default_id: str):
        supplier_data = data.get(
            "supplier",
            {
                "supplier_id": "SUP000",
                "name": "Unspecified Supplier",
                "contact_email": "not-provided@example.com"
            }
        )

        supplier = Supplier.from_dict(supplier_data)

        return cls(
            data.get("product_id", default_id),
            data["name"],
            data.get("price", 0.0),
            data["stock"],
            supplier,
            data["weight"]
        )
