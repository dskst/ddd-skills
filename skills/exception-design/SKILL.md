---
name: 例外設計
description: >-
  This skill should be used when the user asks to "ドメイン例外を設計する", "例外クラスを作る",
  "エラーハンドリングを設計する", "例外の分類を整理する", "ビジネスエラーを定義する",
  "例外戦略を決める", "例外設計をレビューする", "エラーハンドリングを改善する",
  or mentions ドメイン例外、ビジネスエラー、例外設計、エラーハンドリング、例外の分類。
  DDD におけるドメイン例外の設計・分類・階層構造を支援する。
version: 0.1.0
argument-hint: "[ドメインやエラーケースの説明]"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep"]
---

# 例外設計

DDD におけるドメイン例外の設計・分類・階層構造の構築を支援する。

## ドメイン例外とは

ビジネスルールの違反を表現する例外である。技術的なエラー（DB接続エラー等）とは明確に分離する。

**原則:**
- ドメイン例外はドメイン層に定義する
- 例外名はドメイン用語で命名する（技術用語を使わない）
- 例外はビジネスルール違反の「何が」「なぜ」起きたかを伝える
- 例外の捕捉・変換はアプリケーション層またはインフラ層で行う

## 例外の分類体系

### 層別の例外分類

```
例外の種類
├── ドメイン例外（ドメイン層）
│   ├── 不変条件違反: ビジネスルールに反する操作
│   ├── 存在条件違反: 必要なオブジェクトが見つからない
│   └── 状態遷移違反: 許可されない状態遷移
│
├── アプリケーション例外（アプリケーション層）
│   ├── 認証エラー: 認証に失敗
│   ├── 認可エラー: 権限がない操作
│   └── ユースケースエラー: ユースケース前提条件の不成立
│
└── インフラ例外（インフラ層）
    ├── 永続化エラー: DB操作の失敗
    ├── 通信エラー: 外部サービスとの通信失敗
    └── 設定エラー: 構成の不備
```

### ドメイン例外の詳細分類

| 分類 | 説明 | 例 |
|------|------|-----|
| **不変条件違反** | ビジネスルールに反する | 在庫不足、残高不足、上限超過 |
| **存在条件違反** | 必要なものが見つからない | 商品が存在しない、顧客が見つからない |
| **状態遷移違反** | 許可されない状態変更 | キャンセル済み注文の確定、配送済みの取消 |
| **整合性違反** | データ間の不整合 | 合計金額の不一致、重複登録 |

## 例外の命名規則

ドメイン用語で、何が問題かを明確に伝える。

```
推奨:
  InsufficientStockException     — 在庫不足
  OrderAlreadyCancelledException — 注文は既にキャンセル済み
  InvalidOrderAmountException    — 注文金額が不正
  CustomerNotFoundException      — 顧客が見つからない

非推奨:
  BusinessException              — 抽象的すぎる
  ValidationError                — 何の検証か不明
  IllegalStateException          — 技術用語
  Error001                       — 意味が不明
```

## 例外階層の設計

```
DomainException（基底）
├── InvariantViolationException（不変条件違反の基底）
│   ├── InsufficientStockException
│   ├── InsufficientBalanceException
│   └── OrderLimitExceededException
├── EntityNotFoundException（存在条件違反の基底）
│   ├── CustomerNotFoundException
│   ├── ProductNotFoundException
│   └── OrderNotFoundException
└── InvalidStateTransitionException（状態遷移違反の基底）
    ├── OrderAlreadyCancelledException
    ├── OrderAlreadyShippedException
    └── PaymentAlreadyCompletedException
```

## 例外に含める情報

```
ドメイン例外:
  ├── メッセージ: ビジネス用語での説明
  ├── エラーコード: 一意の識別コード（APIレスポンス用）
  ├── 関連データ: 問題の特定に必要な情報
  └── 原因: 根本原因の例外（ある場合）
```

**エラーコードの体系例:**

| プレフィックス | 分類 | 例 |
|-------------|------|-----|
| `ORD-` | 注文ドメイン | `ORD-001: 在庫不足` |
| `PAY-` | 決済ドメイン | `PAY-001: 残高不足` |
| `USR-` | ユーザードメイン | `USR-001: 重複登録` |

## 例外の発生場所

| 場所 | 例外の種類 | 例 |
|------|----------|-----|
| Value Object コンストラクタ | 不変条件違反 | `InvalidEmailFormatException` |
| エンティティのメソッド | 状態遷移違反、不変条件違反 | `OrderAlreadyCancelledException` |
| ドメインサービス | ビジネスルール違反 | `InsufficientStockException` |
| ファクトリ | 生成条件違反 | `InvalidOrderException` |

## 例外の変換戦略

ドメイン例外をアプリケーション層・プレゼンテーション層で適切に変換する。

```
変換フロー:
  ドメイン例外
    → アプリケーション層: ログ出力、イベント発行
    → プレゼンテーション層: HTTPステータスコード + エラーレスポンスに変換
```

| ドメイン例外 | HTTPステータス | 理由 |
|------------|--------------|------|
| 不変条件違反 | 422 Unprocessable Entity | ビジネスルール違反 |
| 存在条件違反 | 404 Not Found | リソースが存在しない |
| 状態遷移違反 | 409 Conflict | 現在の状態と矛盾 |
| 認可エラー | 403 Forbidden | 権限がない |

## アンチパターン

| アンチパターン | 問題 | 対処 |
|--------------|------|------|
| **汎用例外の多用** | `throw new Exception("error")` | ドメイン固有の例外を定義する |
| **例外による制御フロー** | 正常フローを例外で制御 | 例外は異常系のみに使う |
| **例外の握りつぶし** | catch して何もしない | 適切に処理またはリスローする |
| **技術例外の漏洩** | SQLExceptionがドメインまで到達 | インフラ層で変換する |
| **過度な例外階層** | 5段以上のネスト | 2〜3段に抑える |

## 擬似コード例

`examples/` ディレクトリに具体例がある:
- **`examples/exception-hierarchy.pseudo`** — 例外階層の設計例
