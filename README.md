# ddd-skills

A comprehensive Claude Code plugin for Domain-Driven Design (DDD) practices.

Covers strategic design to tactical patterns with 12 features, for beginners to advanced practitioners.

> **[日本語版 README はこちら](README.ja.md)**

## Features

### Skills (8) — Knowledge & Guidance

Available via auto-trigger (context matching) and slash commands.

| Skill | Description |
|-------|-------------|
| `ubiquitous-language` | Define, manage, and check consistency of Ubiquitous Language; generate glossary files |
| `bounded-context` | Analyze and extract Bounded Contexts; generate mermaid Context Maps |
| `domain-event` | Identify and design Domain Events; interactive Event Storming |
| `aggregate-design` | Design Aggregate Roots, boundaries, and invariants |
| `value-object` | Identify Value Object candidates and assist implementation |
| `domain-classifier` | Determine whether logic belongs to the Domain layer or Application layer |
| `repository-design` | Design Repository interfaces |
| `exception-design` | Design, classify, and structure Domain Exceptions |

### Agents (4) — Autonomous Code Analysis

Available proactively (auto-trigger) and reactively (explicit request).

| Agent | Description |
|-------|-------------|
| `architecture-checker` | Check consistency of Layered, Onion, Hexagonal, and Clean Architecture |
| `ddd-reviewer` | Strict DDD compliance review (always at advanced-level standards) |
| `anti-pattern-detector` | Automatically detect 8 DDD anti-patterns |
| `evolvability-assessor` | Assess evolvability across 6 axes: changeability, testability, SOLID, and more |

## Installation

```
/plugin marketplace add dskst/ddd-skills
```

Then install the plugin from the marketplace:

```
/plugin install ddd-skills
```

### Alternative (local)

```bash
claude --plugin-dir /path/to/ddd-skills
```

## Usage

### Auto-trigger

Ask DDD-related questions in normal conversation, and the appropriate skill will trigger automatically.

```
"I want to define a Ubiquitous Language"
"I want to determine Aggregate boundaries"
"Does this logic belong in the Domain layer?"
"Detect any DDD anti-patterns"
```

### Slash Commands

```
/ddd-skills:ubiquitous-language
/ddd-skills:aggregate-design Order
/ddd-skills:domain-classifier
```

## Language

Language-agnostic. Provides pseudocode samples applicable to any programming language.

## License

MIT License
