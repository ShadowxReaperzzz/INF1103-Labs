# Lab 7 checks. Run with:  python test_lab7.py
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from inventory_storage import load_inventory, save_inventory
from physical_product import PhysicalProduct
from product import Product


def output_of(func):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        func()
    return buffer.getvalue()


class Lab7Tests(unittest.TestCase):
    def setUp(self):
        self.guitar = PhysicalProduct("G001", "Guitar", 499.0, 5, 3.5)
        self.os = DigitalProduct("OS001", "Linux Pro", 99.0, 100, 4096.0)

    def test_physical_stores_and_displays_weight(self):
        self.assertEqual(self.guitar.weight, 3.5)
        text = output_of(self.guitar.display_information)
        self.assertIn("Guitar", text)        # from parent
        self.assertIn("3.50 kg", text)       # from child

    def test_digital_stores_and_displays_download_size(self):
        self.assertEqual(self.os.download_size, 4096.0)
        text = output_of(self.os.display_information)
        self.assertIn("Linux Pro", text)
        self.assertIn("4096.00 MB", text)

    def test_fulfilment_info(self):
        self.assertIn("shipping", self.guitar.get_fulfilment_info())
        self.assertIn("electronically", self.os.get_fulfilment_info())

    def test_product_is_abstract(self):
        with self.assertRaises(TypeError):
            Product("X1", "Nope", 1.0, 1)

    def test_interface_is_abstract(self):
        with self.assertRaises(TypeError):
            CanBeShipped()

    def test_shipping_cost(self):
        light = PhysicalProduct("L1", "Light", 1.0, 1, 1.0)
        heavy = PhysicalProduct("H1", "Heavy", 1.0, 1, 10.0)
        self.assertAlmostEqual(light.calculate_shipping_cost(), 7.0)
        self.assertAlmostEqual(heavy.calculate_shipping_cost(), 25.0)

    def test_digital_cannot_be_shipped(self):
        self.assertIsInstance(self.guitar, CanBeShipped)
        self.assertNotIsInstance(self.os, CanBeShipped)
        self.assertFalse(hasattr(self.os, "calculate_shipping_cost"))

    def test_validation(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("A1", "Bad", 1.0, 1, 0)
        with self.assertRaises(ValueError):
            DigitalProduct("A1", "Bad", 1.0, 1, -5)

    def test_inventory_operations(self):
        inv = Inventory()
        inv.add_product(self.guitar)
        inv.add_product(self.os)
        with self.assertRaises(ValueError):
            inv.add_product(PhysicalProduct("g001", "Dup", 1.0, 1, 1.0))
        self.assertIs(inv.search_product("guitar"), self.guitar)
        inv.update_stock("OS001", 50)
        self.assertEqual(self.os.stock, 50)
        self.assertIn("Linux Pro", output_of(inv.display_all))

    def test_json_round_trip_preserves_types(self):
        inv = Inventory()
        inv.add_product(self.guitar)
        inv.add_product(self.os)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "inventory.json"
            save_inventory(inv, path)
            loaded = load_inventory(path)
        g = loaded.search_product("G001")
        d = loaded.search_product("OS001")
        self.assertIsInstance(g, PhysicalProduct)
        self.assertIsInstance(d, DigitalProduct)
        self.assertEqual(g.weight, 3.5)
        self.assertEqual(d.download_size, 4096.0)
        self.assertEqual(g.stock, 5)

    def test_unknown_type_rejected(self):
        with self.assertRaises(ValueError):
            Inventory.from_dict(
                {"products": [{"type": "alien", "name": "x", "stock": 1}]}
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
