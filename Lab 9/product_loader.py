import csv
from product_factory import ProductFactory


def load_products(path, inventory, supplier):
    loaded = 0

    try:
        file = open(path, newline="")

    except FileNotFoundError:
        print(f"Products file not found: {path}")

    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                try:
                    product_type = row[0]
                    product_id = row[1]
                    name = row[2]
                    price = float(row[3])
                    stock = int(row[4])

                    product = ProductFactory.create(
                        product_type,
                        product_id,
                        name,
                        price,
                        stock,
                        supplier,
                        weight=2.0 if product_type == "physical" else None,
                        download_size=50.0 if product_type == "digital" else None
                    )

                    inventory.add_product(product)
                    loaded += 1

                except ValueError as error:
                    print(f"Invalid product row {row}: {error}")

        print(f"{loaded} products loaded.")

    finally:
        print("Load attempt finished.")
