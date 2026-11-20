# =====================================================
# PRODUCT FACTORY
# Turns saved data ("type": "physical" / "digital") back into the correct Product subclass. 
# Keeps Inventory free of any knowledge about specific product types (SRP / OCP): 
# A new product type only need to be registered here.
# =====================================================


from physical_product import PhysicalProduct
from digital_product import DigitalProduct

class ProductFactory:

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier,
        weight=None,
        download_size=None
    ):
        if product_type == "physical":
            return PhysicalProduct(
                product_id, name, price, stock, supplier, weight
            )

        elif product_type == "digital":
            return DigitalProduct(
                product_id, name, price, stock, supplier, download_size
            )

        else:
            raise ValueError(
                f"Unknown product type: {product_type}"
            )


def product_from_dict(data, default_id):
    product_type = data.get("type")

    if product_type == "physical":
        return PhysicalProduct.from_dict(data, default_id)

    elif product_type == "digital":
        return DigitalProduct.from_dict(data, default_id)

    else:
        raise ValueError(
            f"Unknown product type: {product_type!r}"
        )