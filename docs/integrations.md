# Integrations

All tools are **read-only by default**. Writing to any external tool needs the user's yes in the current session (CLAUDE.md rule 4). API keys live in `.env` only.

Everything an integration writes into a note goes inside a sync block, so the next sync replaces only that block and never touches human-written text:

```markdown
> [!sync] ClickUp — synced 2026-10-23
> - [ ] Map depot constraints (Priya, due 2026-10-30)
> - [x] Collect route data
```

---

## Google Calendar

| | |
|---|---|
| Connection | MCP server registered with Claude Code (`claude mcp add ...`) |
| Access | Read events |
| Used by | `prep meetings`, `daily brief` |
| Writes to | `40-Meetings/` |

**Field mapping**

| Calendar | Note frontmatter |
|---|---|
| event id | `calendar_event_id` |
| start date / time | `date`, `time` |
| attendees (email) | `attendees` — matched to `10-People/` by `email` field |
| title | file name slug + `# heading` |
| description | copied into `## Agenda` |

**Matching rules:** attendee email not found in `10-People/` → create the person note with an open question for role and company. Client is set from the attendee's `company` field; if attendees are from two clients, ask.

**Limits:** recurring internal meetings are skipped (see `prep meetings` step 2).

## ClickUp

| | |
|---|---|
| Connection | MCP server or REST API (`CLICKUP_API_TOKEN`) |
| Access | Read tasks; create/update **only when asked** |
| Used by | `prep meetings`, `daily brief`, `weekly review` |
| Writes to | `## Tasks` sync block on project notes |

**Mapping:** project note `clickup_list_id` → ClickUp list. Pull open tasks plus tasks closed in the last 7 days: name, assignee, due date, status.

**Limits:** never close, reassign, or comment on a task without approval. Never copy task comments into the vault (they may contain client data not meant for execs).

## Go High Level (CRM)

| | |
|---|---|
| Connection | REST API (`GHL_API_KEY`, `GHL_LOCATION_ID`) |
| Access | Read contacts and opportunities |
| Writes to | `## Pipeline` sync block on client notes; `email` / `role` on person notes |

**Mapping:** client note `ghl_contact_id` → GHL contact. Pull opportunity stage, value, and last activity date.

**Limits:** deal values are confidential — only on client notes, never in briefs unless the user asks. Status: designed, not built (needs an account).

## Telegram (inbound)

| | |
|---|---|
| Connection | Bot script `integrations/telegram_inbox.py` (`TELEGRAM_BOT_TOKEN`) |
| Access | Receive messages from allowed chat IDs only |
| Writes to | `00-Inbox/YYYY-MM-DD-telegram-<slug>.md` |

The bot only saves messages to the inbox. It never replies with vault content, so a leaked bot token can't expose the vault. Messages from chat IDs not in `TELEGRAM_ALLOWED_CHAT_IDS` are dropped.

Run: `python integrations/telegram_inbox.py` (polls; stop with Ctrl+C). Then ask Claude to `process inbox`.

---

## Status

| Tool | Status | Last tested |
|---|---|---|
| Google Calendar | to build | — |
| ClickUp | to build | — |
| Go High Level | designed | — |
| Telegram | script written, to test | — |
