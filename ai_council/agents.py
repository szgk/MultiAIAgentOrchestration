import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

DEFAULT_TIMEOUT = 120


def _run(cmd: list[str], timeout: int = DEFAULT_TIMEOUT, env: dict | None = None) -> str:
    merged_env = {**os.environ, **(env or {})}
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=merged_env,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed (exit {result.returncode}): {' '.join(cmd)}\n"
            f"stderr: {result.stderr.strip()}"
        )
    return result.stdout.strip()


def run_codex(prompt: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    return _run(["codex", "exec", prompt], timeout=timeout)


def run_claude(prompt: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    return _run(["claude", "-p", prompt], timeout=timeout)


def run_gemini(prompt: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    env = {"GEMINI_API_KEY": api_key} if api_key else {}
    return _run(["gemini", "--skip-trust", "-p", prompt], timeout=timeout, env=env)
