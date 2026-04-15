---
name: リポジトリ設計
description: >-
  This skill should be used when the user asks to "リポジトリを設計する", "repositoryインターフェースを作る",
  "永続化層を設計する", "リポジトリパターンを適用する", "集約の保存方法を決める",
  "データアクセス層を設計する", "リポジトリをレビューする", "リポジトリを改善する",
  or mentions リポジトリ、repository、永続化、データアクセス、集約の保存。
  DDD におけるリポジトリインターフェースの設計を支援する。
version: 0.1.0
argument-hint: "[集約名やドメインの説明]"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep"]
---

# リポジトリ設計

DDD におけるリポジトリインターフェース（ポート）の設計を支援する。

## リポジトリとは

集約の永続化を抽象化するインターフェースである。ドメイン層に定義し、インフラ層で実装する。

**基本原則:**
- **1集約 = 1リポジトリ**: エンティティ単位ではなく集約単位で作成する
- **コレクションのように振る舞う**: インメモリのコレクションと同じ感覚で操作できる
- **ドメイン層に定義**: インターフェースはドメイン層に置く（Driven Port）
- **インフラ層で実装**: 具体的なDB操作はインフラ層のアダプタが担う

## リポジトリインターフェースの設計

### 基本メソッド

```
OrderRepository:
  findById(id: OrderId) → Order?          // 取得
  save(order: Order) → void               // 保存（新規・更新両方）
  delete(order: Order) → void             // 削除
  nextId() → OrderId                      // ID生成（必要な場合）
```

### メソッド命名の原則

| 推奨 | 非推奨 | 理由 |
|------|--------|------|
| `findById` | `getById` | 見つからない場合がある |
| `save` | `insert` / `update` | 新規か更新かはリポジトリが判断 |
| `findByStatus` | `selectByStatus` | SQLの語彙を使わない |
| `delete` | `remove` | コレクションセマンティクスに合わせる |

### 検索メソッドの設計

ドメインの問いかけとして命名する。技術的なクエリ名を使わない。

```
推奨:
  findPendingOrders() → List<Order>
  findByCustomer(customerId: CustomerId) → List<Order>
  existsByEmail(email: EmailAddress) → boolean

非推奨:
  selectWhereStatusEquals(status: String) → List<Order>
  queryByCustomerIdJoinItems(id: int) → List<Order>
```

### 仕様パターン（Specification）

複雑な検索条件はSpecificationパターンで表現する。

```
OrderSpecification:
  - PendingOrdersSpec: 未確定の注文
  - OverdueOrdersSpec: 期限超過の注文
  - HighValueOrdersSpec(threshold: Money): 高額注文

OrderRepository:
  findBySpec(spec: OrderSpecification) → List<Order>
```

## 集約の保存単位

集約全体を保存する。子エンティティや値オブジェクトを個別に保存しない。

```
正しい:
  orderRepository.save(order)  // Order + OrderItems + Money を一括保存

誤り:
  orderRepository.save(order)
  orderItemRepository.save(orderItem)  // 子エンティティを個別保存
```

## リポジトリの戻り値

| メソッド種別 | 戻り値 | 補足 |
|------------|--------|------|
| findById | Optional/Nullable | 見つからない場合がある |
| findByXxx | リスト | 空リストを返す（nullを返さない） |
| save | void または 保存後の集約 | イベント発行が必要な場合は集約を返す |
| exists | boolean | 存在チェック |
| count | 整数 | 件数取得 |

## トランザクション管理

リポジトリ自体はトランザクションを管理しない。トランザクション境界はアプリケーション層（ユースケース）で管理する。

```
// アプリケーション層
PlaceOrderUseCase:
  execute(command):
    transactionManager.begin()
    order = Order.create(command)
    orderRepository.save(order)
    transactionManager.commit()
```

Unit of Work パターンを使って複数のリポジトリ操作を1トランザクションにまとめることも可能である。

## 実装側の考慮事項

インターフェース設計時に、実装側の考慮も念頭に置く:

- **楽観的ロック**: バージョン番号やタイムスタンプによる競合検出
- **遅延読み込み**: 必要に応じてコレクションを遅延読み込みする
- **キャッシュ**: 頻繁に読まれる集約のキャッシュ戦略
- **バッチ処理**: 大量の集約を扱う場合のバッチ操作

ただし、これらはインターフェースに漏れ出してはならない。

## アンチパターン

| アンチパターン | 問題 | 対処 |
|--------------|------|------|
| **Repository per Entity** | 集約境界を無視 | 1集約 = 1リポジトリにする |
| **汎用リポジトリ** | `GenericRepository<T>` で全エンティティ対応 | 集約固有のインターフェースを定義する |
| **SQLの漏洩** | メソッド名にSQL用語 | ドメインの言葉で命名する |
| **検索メソッドの爆発** | findByXAndYAndZ が大量 | Specificationパターンを使う |
| **集約の部分取得** | 子エンティティだけ取得 | 集約全体を取得する |

## 擬似コード例

`examples/` ディレクトリに具体例がある:
- **`examples/repository-interface.pseudo`** — リポジトリインターフェースの設計例
