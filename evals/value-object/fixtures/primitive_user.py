"""プリミティブ型でドメイン値を扱っているサンプル。"""


class User:
    def __init__(
        self,
        user_id: str,
        email: str,
        phone: str,
        zip_code: str,
        city: str,
        street: str,
        country: str,
        balance_amount: int,
        balance_currency: str,
    ):
        self.user_id = user_id
        self.email = email
        self.phone = phone
        self.zip_code = zip_code
        self.city = city
        self.street = street
        self.country = country
        self.balance_amount = balance_amount
        self.balance_currency = balance_currency

    def deposit(self, amount: int, currency: str):
        if currency != self.balance_currency:
            raise ValueError("currency mismatch")
        self.balance_amount += amount

    def update_email(self, email: str):
        if "@" not in email:
            raise ValueError("invalid email")
        self.email = email
