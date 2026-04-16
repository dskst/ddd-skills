---
name: value-object
description: >-
  This skill should be used when the user asks to "Value Objectを作る", "値オブジェクトを設計する",
  "VOを抽出する", "プリミティブ型を置き換える", "value objectを実装する",
  "型を定義する", "ドメインの値を設計する", "値オブジェクトをレビューする",
  "イミュータブルにする", "不変オブジェクトを作る",
  or mentions Value Object、値オブジェクト、VO、プリミティブ型の置き換え、型安全。
  DDD における Value Object の候補特定と実装を支援する。
version: 0.1.0
argument-hint: "[対象のエンティティや値]"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash"]
---

# Value Object設計

DDD における Value Object（値オブジェクト）の候補特定と実装を支援する。

## Value Objectとは

同一性（ID）を持たず、属性の値のみによって等価性が決まる不変のオブジェクトである。

**特性:**
- **不変（Immutable）**: 生成後に状態を変更しない。変更は新しいインスタンスを返す
- **等価性（Equality）**: すべての属性が等しければ等しい。IDによる比較をしない
- **自己検証（Self-Validation）**: 生成時に不変条件を検証し、不正な状態を許さない
- **副作用なし（Side-Effect Free）**: メソッドは新しい値を返すか、計算結果を返す

## Value Object候補の特定

### プリミティブ型の過剰使用を検出する

コードベースを走査し、以下のパターンを検出する:

| 検出パターン | 例 | Value Object候補 |
|------------|-----|----------------|
| String型のメールアドレス | `email: String` | `EmailAddress` |
| String型の電話番号 | `phone: String` | `PhoneNumber` |
| int型の金額 | `price: int` | `Money` |
| String型の住所 | `address: String` | `Address` |
| int型の数量 | `quantity: int` | `Quantity` |
| String型のURL | `url: String` | `Url` |
| 2つの値が常にペア | `currency + amount` | `Money` |

### 判断ツリー

```
この値はValue Objectにすべきか？
├─ ドメイン上の意味を持つ               → VO候補
├─ バリデーションルールがある           → VO候補
├─ 他の値と組み合わせて1つの概念を成す → VO候補（複合VO）
├─ 単なる技術的な値（DBのID等）        → VOにしない
├─ コレクションの要素として使う        → VO候補
└─ 変換・計算ロジックを持つべき        → VO候補
```

## Value Object設計のガイドライン

### 生成時の検証

不正な値でインスタンスを生成できないようにする。

```
EmailAddress:
  生成時チェック:
    - null/空文字でない
    - @を含む
    - ドメイン部分が有効
  不正な値 → 例外を投げる
```

### 振る舞いの定義

Value Object にはドメインに関連する振る舞いを持たせる。

```
Money:
  属性: amount, currency
  振る舞い:
    - add(other: Money) → Money     ※通貨が異なれば例外
    - subtract(other: Money) → Money
    - multiply(factor) → Money
    - isGreaterThan(other: Money) → boolean
```

### 等価性の実装

すべての属性を比較して等価性を判定する。

```
Address:
  equals(other):
    return this.street == other.street
       AND this.city == other.city
       AND this.zipCode == other.zipCode
       AND this.country == other.country
```

## 複合Value Object

複数の値が1つの概念を成す場合、複合VOとして設計する。

```
DateRange:
  属性: startDate, endDate
  不変条件: startDate <= endDate
  振る舞い:
    - contains(date) → boolean
    - overlaps(other: DateRange) → boolean
    - duration() → Duration
```

## ファクトリメソッド

生成方法が複数ある場合、意図を明確にするファクトリメソッドを提供する。

```
Money:
  Money.of(100, "JPY")        — 明示的な生成
  Money.zero("JPY")           — ゼロ値
  Money.fromString("¥100")    — 文字列からの変換
```

## アンチパターン

| アンチパターン | 問題 | 対処 |
|--------------|------|------|
| **Primitive Obsession** | ドメイン値をプリミティブ型で扱う | VOに置き換える |
| **Mutable VO** | セッターで値を変更可能 | 不変にし、新インスタンスを返す |
| **検証なしVO** | 不正な値を許容する | コンストラクタで検証する |
| **振る舞いなしVO** | データの入れ物のみ | ドメインロジックをVOに移動する |
| **巨大VO** | 多数の属性を持つ | 概念ごとに分割する |

## 擬似コード例

`examples/` ディレクトリに具体例がある:
- **`examples/value-objects.pseudo`** — 代表的な Value Object の実装例
