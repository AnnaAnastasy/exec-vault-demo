"""Telegram -> 00-Inbox bridge.

Polls a Telegram bot and saves each text message from an allowed chat
as a Markdown inbox note. It never sends vault content back.

Setup:
  1. Create a bot with @BotFather, put the token in .env as TELEGRAM_BOT_TOKEN.
  2. Put your chat ID(s) in TELEGRAM_ALLOWED_CHAT_IDS (comma-separated).
  3. pip install requests python-dotenv
  4. python integrations/telegram_inbox.py
"""

import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

VAULT = Path(__file__).resolve().parent.parent
INBOX = VAULT / "00-Inbox"
load_dotenv(VAULT / ".env")

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ALLOWED = {c.strip() for c in os.environ.get("TELEGRAM_ALLOWED_CHAT_IDS", "").split(",") if c.strip()}
API = f"https://api.telegram.org/bot{TOKEN}"


def slugify(text: str, max_words: int = 5) -> str:
    words = re.findall(r"[a-z0-9]+", text.lower())[:max_words]
    return "-".join(words) or "message"


def note_path(date: str, slug: str) -> Path:
    path = INBOX / f"{date}-telegram-{slug}.md"
    n = 2
    while path.exists():
        path = INBOX / f"{date}-telegram-{slug}-{n}.md"
        n += 1
    return path


def save_message(msg: dict) -> Path:
    sent = datetime.fromtimestamp(msg["date"], tz=timezone.utc)
    date = sent.strftime("%Y-%m-%d")
    sender = msg.get("from", {}).get("first_name", "unknown")
    text = msg["text"]
    path = note_path(date, slugify(text))
    path.write_text(
        "---\n"
        "type: inbox\n"
        f"created: {date}\n"
        f"updated: {date}\n"
        "tags: []\n"
        "source: telegram\n"
        f"received: {date}\n"
        "processed: false\n"
        "---\n\n"
        f"# Telegram from {sender}, {sent.strftime('%Y-%m-%d %H:%M')} UTC\n\n"
        "## Original\n\n"
        f"{text}\n",
        encoding="utf-8",
    )
    return path


def main() -> None:
    INBOX.mkdir(exist_ok=True)
    offset = None
    print("Listening for Telegram messages. Ctrl+C to stop.")
    while True:
        try:
            resp = requests.get(f"{API}/getUpdates", params={"timeout": 30, "offset": offset}, timeout=40)
            resp.raise_for_status()
        except requests.RequestException as err:
            print(f"Network error: {err}. Retrying in 5s.")
            time.sleep(5)
            continue
        for update in resp.json().get("result", []):
            offset = update["update_id"] + 1
            msg = update.get("message")
            if not msg or "text" not in msg:
                continue
            if str(msg["chat"]["id"]) not in ALLOWED:
                continue  # drop messages from unknown chats
            print(f"Saved {save_message(msg).name}")


if __name__ == "__main__":
    main()
