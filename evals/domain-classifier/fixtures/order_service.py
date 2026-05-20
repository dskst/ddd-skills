"""層の責務が混在したサンプル。本来は分離すべき。"""

import smtplib
import sqlite3


class Order:
    """ドメイン層のはずだが、外部 IO・トランザクション制御まで持っている。"""

    def __init__(self, order_id, items):
        self.order_id = order_id
        self.items = items

    def total(self):
        return sum(item.price * item.quantity for item in self.items)

    def can_cancel(self):
        return self.status != "shipped"

    def place_and_notify(self, db_path, smtp_host, customer_email):
        conn = sqlite3.connect(db_path)
        conn.execute("BEGIN")
        try:
            conn.execute("INSERT INTO orders VALUES (?)", (self.order_id,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise

        server = smtplib.SMTP(smtp_host)
        server.sendmail("noreply@example.com", customer_email, "order placed")
        server.quit()
