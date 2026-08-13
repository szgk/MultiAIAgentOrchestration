import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

DEFAULT_TIMEOUT = 120


class QuotaError(RuntimeError):
    pass


def _first_error_line(stderr: str) -> str:
    for line in stderr.splitlines():
        line = line.strip()
        if line and not line.startswith("(") and "WARNING" not in line:
            return line[:120]
    return "(no stderr)"


def _classify_error(stderr: str, returncode: int) -> RuntimeError:
    s = stderr.lower()
    if "QuotaError" in stderr or "quota exceeded" in s or returncode == 41:
        return QuotaError("quota exceeded")
    if "429" in stderr or "rate limit" in s or "exhausted" in s:
        return QuotaError(f"rate limit / quota ({_first_error_line(stderr)})")
    if "401" in stderr or "unauthorized" in s:
        return RuntimeError("authentication failed (401)")
    if "context" in s and ("length" in s or "limit" in s or "window" in s):
        return RuntimeError("context length exceeded")
    if "timeout" in s or "timed out" in s:
        return RuntimeError("timeout")
    return RuntimeError(f"exit {returncode}: {_first_error_line(stderr)}")


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
        raise _classify_error(result.stderr, result.returncode)
    return result.stdout.strip()


def run_codex(prompt: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    return _run(["codex", "exec", prompt], timeout=timeout)


def run_claude(prompt: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    return _run(["claude", "-p", prompt], timeout=timeout)


def run_gemini(prompt: str, timeout: int = DEFAULT_TIMEOUT) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    env = {"GEMINI_API_KEY": api_key} if api_key else {}
    return _run(["gemini", "--skip-trust", "-p", prompt], timeout=timeout, env=env)
