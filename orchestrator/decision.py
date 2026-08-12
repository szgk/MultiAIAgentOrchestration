"""Issue 6: 最終Decision生成（議長: Claude）"""
from ai_council.agents import run_claude
from orchestrator.paths import CURRENT_TASK, DECISIONS, DISCUSSIONS, REVIEWS, RULES

PROMPT_TEMPLATE = """\
あなたはAI Councilの議長です。

以下のルールを守ってください。

{rules}

## 現在のタスク

{task}

## 各AIの提案

{proposals}

## 各AIのレビュー

{reviews}

上記を踏まえ、最終的な実装方針を決定してください。

以下を含めてください。

- 採用する実装方針
- 採用理由（技術的根拠）
- 却下した案と理由
- 実装上の注意点
- Codexへの実装指示（実装者が迷わない粒度で記載すること）

単純な多数決ではなく、技術的に最も優れた方針を選択してください。
"""


def _load_files(directory, names, suffix) -> str:
    parts = []
    for name in names:
        path = directory / f"{name}-{suffix}.md"
        if path.exists():
            parts.append(f"## {name.capitalize()}\n\n{path.read_text()}")
    if not parts:
        raise FileNotFoundError(f"No {suffix} files found in {directory}")
    return "\n\n---\n\n".join(parts)


def run(timeout: int = 300) -> str:
    names = ("codex", "claude", "gemini")
    prompt = PROMPT_TEMPLATE.format(
        rules=RULES.read_text(),
        task=CURRENT_TASK.read_text(),
        proposals=_load_files(DISCUSSIONS, names, "proposal"),
        reviews=_load_files(REVIEWS, names, "review"),
    )

    print("[decision] Claude（議長）が最終方針を決定中 ...")
    output = run_claude(prompt, timeout=timeout)

    DECISIONS.mkdir(parents=True, exist_ok=True)
    path = DECISIONS / "DECISION.md"
    path.write_text(output)
    print(f"[decision] -> {path}")

    return output


if __name__ == "__main__":
    run()
