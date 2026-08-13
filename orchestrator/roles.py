"""環境変数からロール設定を読み込む"""
import os
from ai_council.agents import run_claude, run_codex, run_gemini

_AGENT_FN = {
    "claude": run_claude,
    "codex": run_codex,
    "gemini": run_gemini,
}


def get_proposal_agents() -> dict[str, object]:
    names = os.getenv("ROLE_PROPOSAL_AGENTS", "codex,claude,gemini")
    return {n: _AGENT_FN[n] for n in _parse(names) if n in _AGENT_FN}


def get_chairman():
    name = os.getenv("ROLE_CHAIRMAN", "claude")
    if name not in _AGENT_FN:
        raise ValueError(f"ROLE_CHAIRMAN '{name}' is not a valid agent.")
    return name, _AGENT_FN[name]


def get_review_agents() -> dict[str, object]:
    names = os.getenv("ROLE_PROPOSAL_AGENTS", "codex,claude,gemini")
    return {n: _AGENT_FN[n] for n in _parse(names) if n in _AGENT_FN}


def _parse(value: str) -> list[str]:
    return [v.strip() for v in value.split(",") if v.strip()]
