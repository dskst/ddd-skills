"""技術的・汎用的すぎるイベント定義のサンプル。"""

from dataclasses import dataclass


@dataclass
class OrderUpdated:
    order_id: str
    changed_fields: dict


@dataclass
class OrderRecordInserted:
    order_id: str


@dataclass
class DatabaseRowChanged:
    table: str
    row_id: str
    new_values: dict


@dataclass
class OrderChanged:
    order_id: str
    snapshot: dict


@dataclass
class DataSaved:
    entity_type: str
    entity_id: str
