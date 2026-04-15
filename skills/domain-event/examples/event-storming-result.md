# イベントストーミング結果 — EC注文プロセス例

## プロセス概要

顧客が商品を注文し、配送されるまでの一連のプロセス。

## イベントフロー

```
[顧客] → カートに追加 → [カート集約] → ItemAddedToCart
                                           │
[顧客] → 注文確定    → [注文集約]   → OrderPlaced
                                           │
                                    ┌──────┴──────┐
                                    ▼             ▼
                              [在庫ポリシー]  [会計ポリシー]
                                    │             │
                              在庫引当       請求書生成
                                    │             │
                              [在庫集約]     [請求書集約]
                                    │             │
                              StockReserved  InvoiceCreated
                                    │             │
                                    ▼             ▼
                              [決済ポリシー] ←────┘
                                    │
                              決済処理
                                    │
                              [決済集約]
                                    │
                              PaymentReceived
                                    │
                              [注文確定ポリシー]
                                    │
                              注文確定
                                    │
                              [注文集約]
                                    │
                              OrderConfirmed
                                    │
                              [配送ポリシー]
                                    │
                              配送手配
                                    │
                              [配送集約]
                                    │
                              ShipmentDispatched
                                    │
                              ShipmentDelivered
```

## イベント一覧

| イベント | 集約 | コマンド | ポリシー/リアクション |
|---------|------|---------|-------------------|
| ItemAddedToCart | Cart | AddItemToCart | - |
| ItemRemovedFromCart | Cart | RemoveItemFromCart | - |
| OrderPlaced | Order | PlaceOrder | → 在庫引当、請求書生成 |
| StockReserved | Stock | ReserveStock | → 決済処理待ち |
| StockInsufficient | Stock | ReserveStock | → 注文キャンセル通知 |
| InvoiceCreated | Invoice | CreateInvoice | → 決済処理 |
| PaymentReceived | Payment | ProcessPayment | → 注文確定 |
| PaymentFailed | Payment | ProcessPayment | → 注文キャンセル、在庫解放 |
| OrderConfirmed | Order | ConfirmOrder | → 配送手配 |
| OrderCancelled | Order | CancelOrder | → 在庫解放、返金処理 |
| ShipmentDispatched | Shipment | DispatchShipment | → 顧客通知 |
| ShipmentDelivered | Shipment | ConfirmDelivery | → 注文完了 |

## ドメインイベントの設計例

```
OrderPlaced:
  eventId: UUID
  occurredAt: DateTime
  orderId: OrderId
  customerId: CustomerId
  items:
    - productId: ProductId
      quantity: Quantity
      unitPrice: Money
  totalAmount: Money

PaymentReceived:
  eventId: UUID
  occurredAt: DateTime
  paymentId: PaymentId
  orderId: OrderId
  amount: Money
  paymentMethod: PaymentMethod
```

## 例外フロー

| トリガー | 例外イベント | リアクション |
|---------|------------|------------|
| 在庫不足 | StockInsufficient | 注文キャンセル → 顧客通知 |
| 決済失敗 | PaymentFailed | 在庫解放 → 注文キャンセル → 顧客通知 |
| 配送不可 | ShipmentFailed | 再配送手配 or 注文キャンセル |
