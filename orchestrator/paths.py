from pathlib import Path

ROOT = Path(__file__).parent.parent
AI_DIR = ROOT / ".ai"

RULES = AI_DIR / "RULES.md"
CURRENT_TASK = AI_DIR / "CURRENT_TASK.md"
DISCUSSIONS = AI_DIR / "discussions" / "current"
REVIEWS = AI_DIR / "reviews" / "current"
DECISIONS = AI_DIR / "decisions"
