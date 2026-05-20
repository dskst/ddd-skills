# ドメインモジュール構成

EC サイトの現在のモジュール構成（パッケージ構造）を以下に示す。

## sales (販売)

- Order
- OrderItem
- Product
- Customer
- Pricing

販売チームが担当。注文の受付・確定までを扱う。

## shipping (配送)

- Shipment
- Parcel
- DeliverySchedule
- Carrier

配送チームが担当。注文確定後の出荷・配送ステータス管理を扱う。
外部配送業者の API を呼び出す必要がある。

## billing (会計)

- Invoice
- Payment
- Refund
- TaxRule

経理チームが担当。請求・支払い・返金を扱う。法令対応が多い。

## inventory (在庫)

- StockItem
- Warehouse
- StockMovement

物流チームが担当。在庫の引当・移動を管理する。
販売側からは「在庫を引き当てられるか」のチェックがある。

## メモ

- 「商品」は販売では Product、配送では Parcel、会計では LineItem と呼ばれている
- 配送と在庫はチームの規模・リリース速度が大きく異なる
- 会計は外部の税務サービスと連携している
