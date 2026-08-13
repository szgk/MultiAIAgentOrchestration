"""独立Proposal生成フロー（ROLE_PROPOSAL_AGENTS）"""
from orchestrator.paths import CURRENT_TASK, DISCUSSIONS, RULES
from orchestrator.roles import get_proposal_agents

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
    agents = get_proposal_agents()
    rules = RULES.read_text()
    task = CURRENT_TASK.read_text()
    prompt = PROMPT_TEMPLATE.format(rules=rules, task=task)

    DISCUSSIONS.mkdir(parents=True, exist_ok=True)

    results = {}
    for name, fn in agents.items():
        print(f"[proposal] {name} ...")
        try:
            output = fn(prompt, timeout=timeout)
            path = DISCUSSIONS / f"{name}-proposal.md"
            path.write_text(output)
            print(f"[proposal] {name} -> {path}")
            results[name] = output
        except Exception as e:
            print(f"[proposal] {name} SKIPPED ({e})")

    return results


if __name__ == "__main__":
    run()
