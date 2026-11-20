# =====================================================
# CanBeShipped INTERFACE (abstract base class)
# A contract: anything that can be shipped must be able to
# calculate its shipping cost. No attributes, no implementation.
# =====================================================

from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        # Return the cost of shipping this object
        pass
