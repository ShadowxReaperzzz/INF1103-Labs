# =====================================================
# DIGITAL PRODUCT
# A Product with a download size (MB). Delivered electronically,
# so it does NOT implement CanBeShipped.
# =====================================================

import math

from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    TYPE = "digital"

    def __init__(
    self,
    product_id: str,
    name: str,
    price: float,
    stock: int,
    supplier: Supplier,
    download_size: float
):
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size = self.validate_download_size(download_size)

    @staticmethod
    def validate_download_size(download_size):
        if not math.isfinite(download_size) or download_size <= 0:
            raise ValueError(
                "Download size must be a finite number greater than zero."
            )

        return download_size

    @property
    def download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(
            f" \n[ Type: Digital | Download size: "
            f"{self.__download_size:.2f} MB ]\n"
        )

    def get_fulfilment_info(self):
        return "Digital product: delivered electronically via download."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.TYPE
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data: dict, default_id: str):
        supplier = Supplier.from_dict(data["supplier"])

        return cls(
            data.get("product_id", default_id),
            data["name"],
            data.get("price", 0.0),
            data["stock"],
            supplier,
            data["download_size"]
        )
