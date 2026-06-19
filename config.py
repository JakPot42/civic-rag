import os

DEMO_MODE = os.getenv("DEMO_MODE", "False").lower() in ("true", "1", "yes")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
DATABASE_URL = "civic.db"
TOP_K = 5
CLAUDE_MODEL = "claude-haiku-4-5-20251001"
