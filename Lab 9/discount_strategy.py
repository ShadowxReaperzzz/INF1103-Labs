
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Abstract base class for order discount strategies."""

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    """Returns the original total without a discount."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Applies a percentage discount to the order total."""

    def __init__(self, percentage: float):
        if not 0 <= percentage <= 100:
            raise ValueError(
                "Discount percentage must be between 0 and 100."
            )

        self.percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)


class BulkDiscount(DiscountStrategy):
    """Applies a fixed discount when the total reaches a threshold."""

    def __init__(self, threshold: float, amount: float):
        if threshold < 0:
            raise ValueError("Threshold cannot be negative.")

        if amount < 0:
            raise ValueError("Discount amount cannot be negative.")

        self.threshold = threshold
        self.amount = amount

    def apply(self, total: float) -> float:
        if total >= self.threshold:
            return max(0, total - self.amount)

        return total


class StudentDiscount(DiscountStrategy):
    """Applies a 5% student discount."""

    def apply(self, total: float) -> float:
        return total * 0.95
