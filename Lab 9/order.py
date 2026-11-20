from product import Product
from discount_strategy import DiscountStrategy, NoDiscount


class OrderLine:
    """Represents one product and its ordered quantity."""

    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        self.product = product
        self.quantity = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity


class Order:
    """Stores order lines and calculates the discounted total."""

    def __init__(
        self,
        discount: DiscountStrategy = None
    ):
        self.order_lines = []
        self.discount = (
            discount if discount is not None else NoDiscount()
        )

    def add_order_line(self, order_line: OrderLine) -> None:
        self.order_lines.append(order_line)

    def set_discount(self, discount: DiscountStrategy) -> None:
        if not isinstance(discount, DiscountStrategy):
            raise TypeError(
                "Discount must be a DiscountStrategy."
            )

        self.discount = discount

    def calculate_total(self) -> float:
        total = sum(
            line.calculate_subtotal()
            for line in self.order_lines
        )

        return self.discount.apply(total)
