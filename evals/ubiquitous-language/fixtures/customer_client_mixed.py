"""Customer と Client が同じ概念を指す形で混在しているサンプル。"""


class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email


class ClientAccount:
    """Customer と同じ意味で使われている。"""

    def __init__(self, client_id, name, mail_address):
        self.client_id = client_id
        self.name = name
        self.mail_address = mail_address


def register_user(client: ClientAccount):
    """user という第三の用語まで登場している。"""
    return Customer(
        customer_id=client.client_id,
        name=client.name,
        email=client.mail_address,
    )


def find_buyer_by_email(email, repository):
    """buyer はさらに別の同義語。"""
    return repository.find_by_email(email)
