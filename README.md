# MultiAIAgentOrchestration

Codex CLI / Claude Code / Gemini CLI をローカルから呼び出し、複数のAIエージェントに設計議論・レビュー・実装を行わせるオーケストレーションシステム。

## 概要

AIを自由会話させるのではなく、以下の固定フローで動作させる。

```
Proposal → Review → Decision → Implementation → Review → Fix → Human Review
```

各フェーズでCodex / Claude / Geminiが役割を分担し、Source of Truthとして `.ai/` 以下のMarkdownファイルを共有する。

## セットアップ

### 必要なCLI

```bash
# Claude Code
claude --version

# Codex CLI
codex --version

# Gemini CLI
npm install -g @google/gemini-cli
gemini --version
```

### 認証

```bash
# Claude Code
claude login

# Codex（ChatGPT Proアカウント）
codex login --device-auth

# Gemini（Google AI Studioで取得したAPIキー）
cp .env.example .env
# .env に GEMINI_API_KEY を設定
```

### 依存パッケージ

```bash
pip install python-dotenv
```

## 使い方

```python
from ai_council.agents import run_claude, run_codex, run_gemini

print(run_claude("提案してください"))
print(run_codex("実装してください"))
print(run_gemini("レビューしてください"))
```

## ディレクトリ構成

```
.
├── .ai/
│   ├── RULES.md              # 全AIが守る共通ルール
│   ├── CURRENT_TASK.md       # 現在のタスク定義
│   ├── discussions/current/  # 各AIのProposal
│   ├── decisions/            # 最終Decision
│   └── reviews/current/      # 各AIのレビュー
├── ai_council/
│   ├── __init__.py
│   └── agents.py             # CLI実行ラッパー
├── .env                      # APIキー（gitignore済み）
└── .env.example              # キー名サンプル
```

## エラー時の挙動

いずれかのAIがエラー（quota超過・認証失敗・タイムアウト等）になった場合、そのAIをスキップして続行する。他のAIの結果は正常に保存される。

```
[review] gemini SKIPPED (quota exceeded)
```

## フロー詳細

| フェーズ | 担当 | 内容 |
|---------|------|------|
| Proposal | Codex / Claude / Gemini | 各AIが独立して提案を作成（他AIの回答なし） |
| Review | Codex / Claude / Gemini | 全Proposalを相互レビュー |
| Decision | Claude（議長） | Proposal + Reviewから最終方針を決定 |
| Implementation | Codex | Decisionに従って実装 |
| Review | Claude / Gemini | git diffをレビュー |
| Fix | Codex | レビュー指摘を修正 |
| Human Review | 人間 | 確認してcommit / push |
