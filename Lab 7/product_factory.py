# =====================================================
# PRODUCT FACTORY
# Turns saved data ("type": "physical" / "digital") back into the correct Product subclass. 
# Keeps Inventory free of any knowledge about specific product types (SRP / OCP): 
# A new product type only need to be registered here.
# =====================================================

from physical_product import PhysicalProduct
from digital_product import DigitalProduct


PRODUCT_TYPES = {
    cls.TYPE: cls for cls in (PhysicalProduct, DigitalProduct)
}


def product_from_dict(data, default_id):
    product_type = data.get("type")
    product_class = PRODUCT_TYPES.get(product_type)

    if product_class is None:
        raise ValueError(f"Unknown product type: {product_type!r}")

    return product_class.from_dict(data, default_id)
