"""Issue 5: AI相互レビュー"""
from ai_council.agents import run_claude, run_codex, run_gemini
from orchestrator.paths import DISCUSSIONS, REVIEWS

AGENTS = {
    "claude": run_claude,
    "codex": run_codex,
    "gemini": run_gemini,
}

PROMPT_TEMPLATE = """\
あなたは設計レビュアーです。

以下の3つの提案を読み、それぞれについてレビューしてください。

{proposals}

以下の観点を含めてください。

- 技術的な誤り
- 要件漏れ
- セキュリティ上の問題
- 過剰設計
- 保守性
- 実装コスト
- テスト容易性
- 各案の良い部分
- 各案の問題点
- 推奨する方針（単純な多数決ではなく、技術的な根拠を示すこと）
"""


def _load_proposals() -> str:
    proposals = []
    for name in ("codex", "claude", "gemini"):
        path = DISCUSSIONS / f"{name}-proposal.md"
        if path.exists():
            proposals.append(f"## {name.capitalize()} Proposal\n\n{path.read_text()}")
    if not proposals:
        raise FileNotFoundError("No proposals found. Run proposal phase first.")
    return "\n\n---\n\n".join(proposals)


def run(timeout: int = 180) -> dict[str, str]:
    proposals_text = _load_proposals()
    prompt = PROMPT_TEMPLATE.format(proposals=proposals_text)

    REVIEWS.mkdir(parents=True, exist_ok=True)

    results = {}
    for name, fn in AGENTS.items():
        print(f"[review] {name} ...")
        try:
            output = fn(prompt, timeout=timeout)
            path = REVIEWS / f"{name}-review.md"
            path.write_text(output)
            print(f"[review] {name} -> {path}")
            results[name] = output
        except Exception as e:
            print(f"[review] {name} SKIPPED ({e})")

    return results


if __name__ == "__main__":
    run()
