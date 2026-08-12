from ai_council.agents import run_claude, run_codex, run_gemini

agents = {
    "claude": run_claude,
    "codex": run_codex,
    "gemini": run_gemini,
}

for name, fn in agents.items():
    try:
        result = fn("Hello、1+1の答えを一言で答えてください")
        print(f"[{name}] OK: {result[:80]}")
    except Exception as e:
        print(f"[{name}] ERROR: {e}")
