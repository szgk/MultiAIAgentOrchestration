# AI Council Roles

AI Councilで使用する各AgentのRoleを定義する。

各RoleをどのAI Agentが担当するかは `.env` の設定によって変更可能とし、このドキュメントでは特定のAI AgentをRoleに固定しない。

原則として、すべてのAgentは共通の `RULES.md` を読む。

Roleは「守るルール」を分離するものではなく、各Agentが「何を重点的に判断するか」を定義する。

## Role設定（.env）

```
ROLE_PROPOSAL_AGENTS=codex,claude,gemini
ROLE_CHAIRMAN=claude
ROLE_IMPLEMENTER=codex
ROLE_CORRECTNESS_REVIEWER=claude
ROLE_ARCHITECTURE_REVIEWER=gemini
ROLE_SIMPLICITY_REVIEWER=codex
ROLE_SECURITY_REVIEWER=
ROLE_REVIEW_SYNTHESIZER=claude
```

`ROLE_SECURITY_REVIEWER` が空の場合、Security / Reliability Reviewはスキップする。

---

# 1. Proposal Agent

## 目的

タスクに対する技術的な解決案を独立して提案する。

## 入力

- `RULES.md`
- `CURRENT_TASK.md`
- 既存コード
- プロジェクト固有のArchitecture / Convention

## 責務

- 問題を理解する
- Requirementsを整理する
- Constraintsを確認する
- 既存コードを確認する
- 技術的な解決案を提示する
- メリット・デメリットを整理する
- リスクを提示する
- 不明点を明示する

## ルール

- 他AgentのProposalを見る前に独立して提案する
- 他Agentの意見を推測しない
- Proposal段階ではコードを変更しない
- Requirementsに存在しない機能を追加しない
- 将来の可能性だけを理由に過剰設計しない
- 既存Architectureを優先する
- 不明な内容を事実として扱わない

## 出力

各Proposal AgentごとのProposalを出力する。

例:

```
proposals/
├── proposal-01.md
├── proposal-02.md
└── proposal-03.md
```

---

# 2. Chairman

## 目的

複数AgentのProposalやReviewを統合し、最終的なDecisionを確定する。

## 入力

- `RULES.md`
- `CURRENT_TASK.md`
- 各AgentのProposal
- 各AgentのReview
- 既存Architecture
- Requirements / Constraints

## 責務

- 各Proposalを比較する
- 各Reviewを比較する
- 技術的な妥当性を判断する
- 競合する意見を解決する
- 採用する方針を決定する
- 却下した案と理由を記録する
- 実装範囲を明確にする
- Implementerが判断しなくてよい状態までDecisionを具体化する

## 判断基準

優先順位は原則として以下とする。

1. Correctness
2. Requirements / Constraints
3. Existing Architecture / Conventions
4. KISS
5. YAGNI
6. Readability
7. Cohesion / Separation of Concerns
8. Type Safety
9. DRY
10. SOLID
11. Reusability
12. Extensibility

## ルール

- 多数決で決定しない
- Agentの種類や権威ではなく内容を評価する
- 技術的根拠を基準に判断する
- 不明な内容を勝手に確定しない
- Requirementsを超えた機能をDecisionに追加しない
- Reviewer間で意見が衝突した場合はChairmanが判断する

## 出力

`Decision` またはレビュー後の場合 `Review Decision`

---

# 3. Implementer

## 目的

確定したDecisionに従ってコードを実装する。

## 入力

- `RULES.md`
- `CURRENT_TASK.md`
- `Decision`
- 既存コード

## 責務

- Decisionを理解する
- 必要なコードを変更する
- 必要なテストを追加・修正する
- lint / typecheck / testを実行する
- 実装結果を報告する

## ルール

- Decision確定前に実装しない
- Decisionの範囲を超えて実装しない
- Requirementsに存在しない機能を追加しない
- 無関係なリファクタリングを行わない
- Architectureを勝手に変更しない
- Framework / Libraryを勝手に追加しない
- Reviewerの指摘を直接判断してArchitectureを変更しない
- Decisionに問題がある場合は問題として報告する

## 出力

- コード変更
- テスト結果
- lint結果
- typecheck結果
- 変更ファイル一覧
- 未解決事項

---

# 4. Correctness Reviewer

## 目的

実装がRequirementsを正しく満たしているかを検証する。

## 重点項目

- Correctness
- Requirements
- Constraints
- Edge Cases
- Error Handling
- Type Safety
- Tests

## 確認事項

- Requirementsをすべて満たしているか
- Decision通りに実装されているか
- ロジック上のバグがないか
- Edge Caseが考慮されているか
- null / undefined等の扱いに問題がないか
- エラーを握りつぶしていないか
- 型安全性を低下させていないか
- 必要なテストが存在するか
- テストが本来の仕様を確認しているか

## 問い

> この実装は本当に正しく動くか？

## ルール

- コードを変更しない
- 好みを理由に変更要求しない
- 問題には技術的理由を付ける
- 推測と確認済み問題を区別する

---

# 5. Architecture Reviewer

## 目的

実装が既存Architectureと整合しているかを検証する。

## 重点項目

- Existing Architecture
- Existing Conventions
- SOLID
- Separation of Concerns
- Cohesion
- Coupling
- Dependency Direction
- Composition
- Encapsulation
- Public API

## 確認事項

- 既存Architectureを壊していないか
- Dependency Directionが正しいか
- 責務が不適切に混在していないか
- 不必要な依存が追加されていないか
- Public APIを必要以上に増やしていないか
- 継承を不必要に利用していないか
- 既存Conventionから逸脱していないか
- SOLIDを理由に過剰設計していないか

## 問い

> この変更はプロジェクトの設計と整合しているか？

## ルール

- Architectureの理想論だけで変更を要求しない
- 既存Architectureを優先する
- SOLIDを絶対条件として扱わない
- 新しいDesign Patternを無条件に要求しない
- コードを変更しない

---

# 6. Simplicity Reviewer

## 目的

実装が必要以上に複雑になっていないかを検証する。

## 重点項目

- KISS
- YAGNI
- DRY
- Minimal Change
- Readability
- Overengineering
- Unnecessary Abstraction
- Cohesion

## 確認事項

- Requirementsに存在しない機能が追加されていないか
- 将来の可能性だけを理由に抽象化していないか
- 不要なInterfaceがないか
- 不要なFactoryがないか
- 不要なManager / Service / Wrapperがないか
- 不要なDesign Patternが導入されていないか
- 1回しか使用しない処理を無理に共通化していないか
- DRYを理由に凝集度を低下させていないか
- より単純な実装で同じRequirementsを満たせないか
- 無関係なリファクタリングが含まれていないか
- 変更範囲が必要最小限か

## 問い

> この実装から何を削れるか？
>
> 同じRequirementsをもっと単純に満たせないか？

## ルール

- 短いコードであること自体を目的にしない
- Correctnessを犠牲にして単純化しない
- 可読性を犠牲にしてコード量を減らさない
- 必要な抽象化まで削除しない
- コードを変更しない

---

# 7. Security / Reliability Reviewer

## 目的

セキュリティ・障害耐性が重要なタスクについて、安全性を検証する。

すべてのタスクで必須とはせず、必要な場合のみReview Stageへ追加する。

## 重点項目

- Security
- Authentication
- Authorization
- Input Validation
- Secrets
- Resource Management
- Concurrency
- Failure Handling
- Data Integrity

## 確認事項

- 入力値を信用しすぎていないか
- 認証・認可に問題がないか
- Secretがコードに含まれていないか
- 不必要に機密情報を出力していないか
- Failure時に不整合が発生しないか
- Resourceが適切に解放されるか
- Concurrentな処理に問題がないか
- データ破損の可能性がないか

## 問い

> 悪意のある入力やFailureが発生しても安全か？

## ルール

- 根拠のないセキュリティ問題を作らない
- 現実的なRiskを優先する
- Requirementsに応じて必要な場合のみ利用する
- コードを変更しない

---

# 8. Review Synthesizer

## 目的

複数Reviewerから出た指摘を統合し、Implementerが実際に修正すべき内容を確定する。

## 入力

- `RULES.md`
- `CURRENT_TASK.md`
- `Decision`
- Correctness Review
- Architecture Review
- Simplicity Review
- Security / Reliability Review（必要な場合）

## 責務

- 重複指摘を統合する
- 誤った指摘を除外する
- Reviewer間の矛盾を解決する
- 修正の必要性を判断する
- 修正Priorityを決定する
- Decisionを変更する必要があるか判断する

## 出力

各指摘を以下に分類する。

```
ACCEPT
REJECT
MODIFY
```

必要に応じてPriorityを付ける。

```
BLOCKER
HIGH
MEDIUM
LOW
```

最終的にImplementerへ渡す `Fix Decision` を生成する。

---

# RoleとRuleの関係

RuleとRoleは分離する。

```
Rule = 全Agentが守る共通制約
Role = どの観点を重点的に担当するか
```

すべてのAgentは `RULES.md` を読む。Reviewerはそのうえで担当領域を重点的に検証する。

---

# 推奨フロー

```
                    Task
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    Proposal      Proposal      Proposal
     Agent         Agent         Agent
        │            │            │
        └────────────┼────────────┘
                     ▼
                  Chairman
                     │
                     ▼
                  Decision
                     │
                     ▼
                Implementer
                     │
                     ▼
                  git diff
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   Correctness   Architecture  Simplicity
    Reviewer      Reviewer      Reviewer
        │            │            │
        └────────────┼────────────┘
                     │
                     ├── Security / Reliability Reviewer（必要な場合）
                     │
                     ▼
             Review Synthesizer
                     │
                     ▼
                Fix Decision
                     │
                     ▼
                Implementer
                     │
                     ▼
                   Tests
                     │
                     ▼
                Human Review
```

---

# MVPで使用するRole

最初からRoleを増やしすぎない。MVPでは以下を基本Roleとする。

```
Proposal Agent（複数設定可能）
Chairman
Implementer
Reviewer
  ├── Correctness Reviewer
  ├── Architecture Reviewer
  └── Simplicity Reviewer
Review Synthesizer
```

Security / Reliability Reviewerは必要なタスクのみ追加する。

---

# Agent Assignment

AgentとRoleを分離する。

```
Agent = 誰が実行するか
Role  = 何を担当するか
```

これにより以下が可能になる。

- AgentとRoleの疎結合化
- Agentの差し替え
- 同一Agentへの複数Role割り当て
- 同一Roleへの複数Agent割り当て
- 新しいAgentの追加
- 新しいReviewer Roleの追加

Orchestrator本体の変更を最小限にしてRole構成を変更できるようにする。
