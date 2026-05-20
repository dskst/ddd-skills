"""注文ドメインの簡易サンプル。汎用例外を投げているためドメイン例外設計が必要。"""


class Order:
    def __init__(self, order_id: str, status: str, total: int):
        self.order_id = order_id
        self.status = status
        self.total = total

    def cancel(self):
        if self.status == "cancelled":
            raise Exception("error")
        if self.status == "shipped":
            raise Exception("cannot cancel")
        self.status = "cancelled"


class Inventory:
    def __init__(self, stock: int):
        self.stock = stock

    def reserve(self, quantity: int):
        if quantity > self.stock:
            raise ValueError("stock not enough")
        self.stock -= quantity


def find_customer(customer_id: str, customers: dict):
    if customer_id not in customers:
        raise Exception("not found")
    return customers[customer_id]
