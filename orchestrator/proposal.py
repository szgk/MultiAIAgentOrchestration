"""Issue 4: 独立Proposal生成フロー"""
from ai_council.agents import run_claude, run_codex, run_gemini
from orchestrator.paths import CURRENT_TASK, DISCUSSIONS, RULES

AGENTS = {
    "claude": run_claude,
    "codex": run_codex,
    "gemini": run_gemini,
}

PROMPT_TEMPLATE = """\
あなたは設計議論の参加者です。

以下のルールを守ってください。

{rules}

以下のタスクについて、他のAIとは独立して技術的な提案を作成してください。

{task}

以下を含めてください。

- 問題の理解
- 提案
- 実装方法
- メリット
- デメリット
- リスク
- 不明点
"""


def run(timeout: int = 180) -> dict[str, str]:
    rules = RULES.read_text()
    task = CURRENT_TASK.read_text()
    prompt = PROMPT_TEMPLATE.format(rules=rules, task=task)

    DISCUSSIONS.mkdir(parents=True, exist_ok=True)

    results = {}
    for name, fn in AGENTS.items():
        print(f"[proposal] {name} ...")
        output = fn(prompt, timeout=timeout)
        path = DISCUSSIONS / f"{name}-proposal.md"
        path.write_text(output)
        print(f"[proposal] {name} -> {path}")
        results[name] = output

    return results


if __name__ == "__main__":
    run()
