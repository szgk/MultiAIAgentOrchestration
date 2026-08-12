# MultiAIAgentOrchestration

Codex CLI / Claude Code / Gemini CLI をローカルから呼び出し、複数のAIエージェントに設計議論・レビュー・実装を行わせるオーケストレーションシステム。

## 概要

AIを自由会話させるのではなく、以下の固定フローで動作させる。

```
Proposal → Review → Decision → Implementation → Review → Fix → Human Review
```

各フェーズでCodex / Claude / Geminiが役割を分担し、Source of Truthとして `.ai/` 以下のMarkdownファイルを共有する。

どのAIがどのRoleを担当するかは `.env` で設定する。詳細は `.ai/ROLES.md` を参照。

---

## セットアップ

### 1. CLIのインストール

```bash
# Claude Code
npm install -g @anthropic-ai/claude-code

# Codex CLI
npm install -g @openai/codex

# Gemini CLI
npm install -g @google/gemini-cli
```

バージョン確認:

```bash
claude --version
codex --version
gemini --version
```

### 2. 認証

**Claude Code**（Claude.ai アカウント）

```bash
claude login
```

**Codex**（ChatGPT Pro アカウント）

```bash
codex login --device-auth
```

ブラウザが開くのでChatGPT Proアカウントでログインする。

**Gemini**（Google AI Studio APIキー）

[Google AI Studio](https://aistudio.google.com/) でAPIキーを取得し、`.env` に設定する。

```bash
cp .env.example .env
# .env の GEMINI_API_KEY にキーを設定
```

### 3. Python依存パッケージ

```bash
pip install python-dotenv
```

### 4. Role設定

`.env` でどのAIがどのRoleを担当するか設定する。

```bash
# .env
ROLE_PROPOSAL_AGENTS=codex,claude,gemini
ROLE_CHAIRMAN=claude
ROLE_IMPLEMENTER=codex
ROLE_CORRECTNESS_REVIEWER=claude
ROLE_ARCHITECTURE_REVIEWER=gemini
ROLE_SIMPLICITY_REVIEWER=codex
ROLE_SECURITY_REVIEWER=
ROLE_REVIEW_SYNTHESIZER=claude
```

`ROLE_SECURITY_REVIEWER` を空にするとSecurity Reviewをスキップする。

---

## 使い方

### タスクを定義する

`.ai/CURRENT_TASK.md` に実装したい内容を記載する。

```markdown
# Task

## Goal
ログイン処理を実装する。

## Requirements
- メールアドレスとパスワードで認証する
- ...

## Constraints
- 外部認証ライブラリは使用しない
```

### フルフローを実行する

```bash
python -m orchestrator.run_council
```

### フェーズを個別実行する

```bash
python -m orchestrator.proposal   # Proposal生成
python -m orchestrator.review     # 相互レビュー
python -m orchestrator.decision   # Decision確定
```

---

## ディレクトリ構成

```
.
├── .ai/
│   ├── RULES.md              # 全AIが守る共通ルール
│   ├── ROLES.md              # Roleの定義
│   ├── CURRENT_TASK.md       # 現在のタスク定義
│   ├── discussions/current/  # 各AIのProposal（gitignore済み）
│   ├── decisions/            # 最終Decision（gitignore済み）
│   └── reviews/current/      # 各AIのレビュー（gitignore済み）
├── ai_council/
│   ├── __init__.py
│   └── agents.py             # CLI実行ラッパー
├── orchestrator/
│   ├── proposal.py           # Proposal生成フロー
│   ├── review.py             # 相互レビューフロー
│   ├── decision.py           # Decision生成フロー
│   └── run_council.py        # フルフロー実行
├── .env                      # APIキー・Role設定（gitignore済み）
└── .env.example              # 設定のサンプル
```

---

## エラー時の挙動

いずれかのAIがエラー（quota超過・認証失敗・タイムアウト等）になった場合、そのAIをスキップして続行する。

```
[review] gemini SKIPPED (quota exceeded)
```

---

## フロー詳細

| フェーズ | Role | 内容 |
|---------|------|------|
| Proposal | Proposal Agent × 複数 | 各AIが独立して提案を作成（他AIの回答なし） |
| Decision | Chairman | Proposalから最終方針を決定 |
| Implementation | Implementer | Decisionに従って実装 |
| Review | Correctness / Architecture / Simplicity Reviewer | git diffをレビュー |
| Review Synthesis | Review Synthesizer | 指摘を統合しFix Decisionを生成 |
| Fix | Implementer | Fix Decisionに従って修正 |
| Human Review | 人間 | 確認してcommit / push |

各Roleを担当するAIは `.env` で設定する。
