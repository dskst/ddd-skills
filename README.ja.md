# ddd-skills

DDD（ドメイン駆動設計）の実践を包括的に支援する Claude Code プラグイン。

初心者から上級者まで、DDDの戦略的設計から戦術的パターンまでを12の機能でカバーする。

> **[English README](README.md)**

## 機能一覧

### Skills（8つ） — 知識・ガイダンス提供

自動発動（コンテキストマッチ）およびスラッシュコマンドで利用可能。

| スキル | 説明 |
|--------|------|
| `ubiquitous-language` | ユビキタス言語の定義・管理・一貫性チェック・用語集ファイル生成 |
| `bounded-context` | 境界づけられたコンテキストの分析・抽出・mermaid コンテキストマップ生成 |
| `domain-event` | ドメインイベントの特定・設計・対話的イベントストーミング |
| `aggregate-design` | 集約ルート・境界・不変条件の設計 |
| `value-object` | Value Object 候補の特定と実装支援 |
| `domain-classifier` | ロジックがドメイン層かアプリケーション層かの判定 |
| `repository-design` | リポジトリインターフェースの設計 |
| `exception-design` | ドメイン例外の設計・分類・階層構造 |

### Agents（4つ） — 自律的コード分析

プロアクティブ（自動発動）およびリアクティブ（明示的依頼）で利用可能。

| エージェント | 説明 |
|------------|------|
| `architecture-checker` | レイヤード・オニオン・ヘキサゴナル・クリーンアーキテクチャの整合性チェック |
| `ddd-reviewer` | DDD準拠度の厳密レビュー（常に上級者向け基準） |
| `anti-pattern-detector` | 8つのDDDアンチパターンの自動検出 |
| `evolvability-assessor` | 変更容易性・テスタビリティ・SOLID等6軸の進化可能性評価 |

## インストール

```bash
claude --plugin-dir /path/to/ddd-skills
```

## 使い方

### 自動発動

通常の会話でDDD関連の質問をすると、適切なスキルが自動的に発動する。

```
「ユビキタス言語を定義したい」
「集約の境界を決めたい」
「このロジックはドメイン層に属するか？」
「DDDのアンチパターンがないか検出して」
```

### スラッシュコマンド

```
/ddd-skills:ubiquitous-language
/ddd-skills:aggregate-design 注文
/ddd-skills:domain-classifier
```

## 言語

言語非依存。擬似コードによるサンプルを提供し、あらゆるプログラミング言語で適用可能。

## ライセンス

MIT License
