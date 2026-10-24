# Conventions

## File names

| Type | Pattern | Example |
|---|---|---|
| person | `first-last.md` | `priya-nair.md` |
| client | `company-name.md` | `harbor-logistics.md` |
| project | `client-short-project.md` | `harbor-route-optimization.md` |
| meeting | `YYYY-MM-DD-title.md` | `2026-10-21-calder-kickoff.md` |
| decision | `YYYY-MM-DD-title.md` | `2026-10-22-pause-pinecrest-phase-2.md` |
| brief | `YYYY-MM-DD-daily-brief.md` / `YYYY-Www-weekly-review.md` | `2026-10-23-daily-brief.md` |
| inbox | `YYYY-MM-DD-source-title.md` | `2026-10-23-telegram-voice-note.md` |

If two meetings share a date and title, add `-2`.

## Frontmatter by type

All notes: `type`, `created`, `updated`, `tags`.

**person**
```yaml
role: ""
company: "[[client-slug]]"   # or "Ridgeline" for team
email: ""
relationship: client | team | partner | vendor
last_contact: YYYY-MM-DD
```

**client**
```yaml
status: active | prospect | paused | former
owner: "[[person-slug]]"     # Ridgeline lead
ghl_contact_id: ""
since: YYYY-MM-DD
```

**project**
```yaml
client: "[[client-slug]]"
status: planning | active | on-hold | done
lead: "[[person-slug]]"
start: YYYY-MM-DD
due: YYYY-MM-DD
clickup_list_id: ""
```

**meeting**
```yaml
date: YYYY-MM-DD
time: "HH:MM"
attendees: ["[[person-slug]]"]
client: "[[client-slug]]"
project: "[[project-slug]]"
calendar_event_id: ""
```

**decision**
```yaml
date: YYYY-MM-DD
status: proposed | final | superseded
decided_by: ["[[person-slug]]"]
project: "[[project-slug]]"
supersedes: ""
superseded_by: ""
```

**inbox**
```yaml
source: telegram | manual | email
received: YYYY-MM-DD
processed: false
```

## Tags

Keep tags few and lowercase. Allowed: `#risk`, `#follow-up`, `#waiting`, `#urgent`, `#idea`. Add new tags only when the user asks.

## Callouts

- `> [!question]` — unknown fact; needs a human
- `> [!warning]` — risk or deadline in danger
- `> [!sync]` — block written by an integration, with source and date. Overwrite only this block on the next sync.
