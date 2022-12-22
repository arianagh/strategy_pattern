from abc import ABC, abstractmethod
from collections.abc import Sequence
from decimal import Decimal
from typing import NamedTuple, Optional


class Customer(NamedTuple):
    name: str
    fidelity: int


class LineItem(NamedTuple):

    product: str
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.quantity * self.price


class Order(NamedTuple):
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional['Promotion'] = None

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
            return discount
        discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due(fee): {self.due():.2f}>'


class Promotion(ABC):
    """Return discount as a positive dollar amount"""

    @abstractmethod
    def discount(self, order: Order) -> Decimal:
        pass


class FidelityPromotion(Promotion):
    """5% discount for customers with 1000 or more fidelity points"""

    def discount(self, order: Order) -> Decimal:
        rate = Decimal('0.05')
        if order.customer.fidelity >= 1000:
            return order.total() * rate
        return Decimal(0)


class BulkItemPromotion(Promotion):
    """10% discount for each LineItem with 20 or more units"""

    def discount(self, order: Order) -> Decimal:
        rate = Decimal('0.1')
        total_discount = Decimal(0)
        for item in order.cart:
            if item.quantity >= 20:
                total_discount += item.total() * rate
        return total_discount


class LargeOrderPromotion(Promotion):
    """7% discount for orders with 10 or more distinct items"""

    def discount(self, order: Order) -> Decimal:
        rate = Decimal('0.07')
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * rate
        return Decimal(0)


clark = Customer('Clark Scot', 0)
emily = Customer('Emily Taho', 1100)
cart = (LineItem('lemon', 4, Decimal('.5')),
        LineItem('grape', 10, Decimal('1.5')),
        LineItem('melon', 5, Decimal(5))
        )
print(Order(clark, cart, FidelityPromotion()))
print(Order(emily, cart, FidelityPromotion()))
