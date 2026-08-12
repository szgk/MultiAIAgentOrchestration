# AI Council MVP

## 概要

Codex CLI / Claude Code / Gemini CLI をローカルから呼び出し、複数AIに設計議論・レビュー・実装を行わせるオーケストレーションシステム。

## ディレクトリ構成

```
.ai/
├── RULES.md              # 全AIが守る共通ルール
├── CURRENT_TASK.md       # 現在のタスク定義
├── discussions/current/  # 各AIのProposal
├── decisions/            # 最終Decision
└── reviews/current/      # 各AIのレビュー

ai_council/
├── __init__.py
└── agents.py             # CLI実行ラッパー（run_codex / run_claude / run_gemini）
```

## 実行フロー

1. **Proposal** — 各AIが独立して提案生成（他AIの回答なし）
2. **Review** — 全Proposalを全AIに渡しレビュー
3. **Decision** — Claudeが議長としてProposal+Reviewから最終方針を決定
4. **Implementation** — Codexが実装
5. **Review** — Claude / GeminiがDiffをレビュー
6. **Fix** — Codexが修正
7. **Human Review** — 人間が確認してcommit / push

## AI CLI実行方法

```bash
codex exec "プロンプト"
claude -p "プロンプト"
gemini -p "プロンプト"
```

`ai_council/agents.py` の `run_codex` / `run_claude` / `run_gemini` でsubprocessラップ済み。

## 環境変数 / 認証

| CLI | 認証方法 |
|-----|---------|
| `claude` | Claude Codeアカウントログイン（`claude login`） |
| `codex` | ChatGPT Proアカウントログイン（`codex login --device-auth`） |
| `gemini` | `.env` の `GEMINI_API_KEY`（Google AI Studio で無料取得） |

APIキーは `.env` で管理し、`python-dotenv` で読み込む。`.env` は `.gitignore` 済み。

```
.env               # gitignore済み・コミット禁止
.env.example       # キー名だけ記載したサンプル（コミットOK）
```

`ai_council/agents.py` がモジュールロード時に `.env` を自動読み込みする。

## 基本方針

- `.ai/` 以下のMarkdownがSource of Truth（DBなし）
- AI間の同調防止のため、Proposal生成時は他AIの回答を渡さない
- 単純な多数決禁止、必ず技術的根拠を記載
- MVP完成後にMCP / SQLite / Git worktree / GitHub連携を追加予定
