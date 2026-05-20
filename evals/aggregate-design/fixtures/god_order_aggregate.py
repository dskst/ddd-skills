"""God Aggregate のサンプル。エンティティ数が多く、トランザクション境界も曖昧。"""


class Order:
    def __init__(self, order_id, customer, items, payments, shipments,
                 reviews, refunds, coupons, points, inventory_locks,
                 notifications, audit_logs):
        self.order_id = order_id
        self.customer = customer
        self.items = items
        self.payments = payments
        self.shipments = shipments
        self.reviews = reviews
        self.refunds = refunds
        self.coupons = coupons
        self.points = points
        self.inventory_locks = inventory_locks
        self.notifications = notifications
        self.audit_logs = audit_logs

    def place(self):
        for item in self.items:
            item.stock -= item.quantity
        for payment in self.payments:
            payment.charge()
        for shipment in self.shipments:
            shipment.dispatch()
        for notification in self.notifications:
            notification.send()
        self.audit_logs.append("placed")

    def add_review(self, review):
        self.reviews.append(review)

    def apply_coupon(self, coupon):
        self.coupons.append(coupon)

    def grant_points(self, points):
        self.points += points
