from typing import Optional, Callable
from decimal import Decimal


Promotion: Optional[Callable] = None

promotions: list[Promotion] = []


def promotion(func: Promotion) -> Promotion:
    """ decorator function """
    promotions.append(func)
    return func


def best_promo(order) -> Decimal:
    return max(item(order) for item in promotions)
