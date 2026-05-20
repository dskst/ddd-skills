"""SQL 用語が漏れたリポジトリインターフェースのサンプル。"""

from abc import ABC, abstractmethod


class OrderRepository(ABC):
    @abstractmethod
    def select_by_id(self, order_id):
        ...

    @abstractmethod
    def select_where_status_equals(self, status):
        ...

    @abstractmethod
    def select_join_items_by_customer_id(self, customer_id):
        ...

    @abstractmethod
    def insert(self, order):
        ...

    @abstractmethod
    def update(self, order):
        ...

    @abstractmethod
    def delete_by_id(self, order_id):
        ...

    @abstractmethod
    def count_rows(self):
        ...
