# Workflows

Follow these steps exactly when the user names a workflow. After each workflow: update the affected `_index.md` files, then make one git commit (see CLAUDE.md §9).

---

## process inbox

1. List files in `00-Inbox/` where `processed: false`.
2. For each item:
   1. Read it. Identify every person, client, project, date, task, and decision mentioned.
   2. Match each one to an existing note using the folder `_index.md` files. If a person or client has no note, create one from the template and mark unknown fields with an open question.
   3. Add the new facts to the right notes under a dated heading, e.g. `### 2026-10-23 (from inbox)`. Link back to the inbox item.
   4. If the item contains a decision, run `log decision` for it with `status: proposed` — never `final`. Only the user makes a decision final.
   5. If the item contradicts an existing note, do not overwrite. Add a `> [!question]` callout to both notes.
   6. Set `processed: true` and move the item to `99-Archive/inbox/`.
3. Reply with a short list: what was sorted where, and any open questions.

## prep meetings [date]

Default date: next working day.

1. Pull events for the date from Google Calendar (see `docs/integrations.md`).
2. Skip events with no external attendees unless the title contains a client name.
3. For each event, create `40-Meetings/YYYY-MM-DD-title.md` from the meeting template, unless a note with the same `calendar_event_id` exists — then update it.
4. Fill the **Context** section:
   - Each attendee: role, last contact date, last meeting note
   - The client's current status and open `#follow-up` items
   - The project's open ClickUp tasks (with sync date)
   - Any `> [!question]` callouts on the client or project
5. Link the meeting from the client and project notes under `## Meetings`.
6. Reply with the list of meetings prepared.

## daily brief

1. Create `60-Briefs/YYYY-MM-DD-daily-brief.md` from the brief template.
2. Fill it in this order, max 5 bullets per section:
   - **Today:** meetings (link to prepped notes; prep any that are missing)
   - **Needs a decision:** decisions with `status: proposed`
   - **At risk:** projects with `due` in the next 14 days or a `> [!warning]`
   - **Waiting on others:** items tagged `#waiting`
   - **Open questions:** all `> [!question]` callouts added in the last 7 days
3. Each bullet links to its source note. No bullet without a link.

## log decision

1. Ask for anything missing: what was decided, who decided, why, related project.
2. Create `50-Decisions/YYYY-MM-DD-title.md` from the decision template. Default `status: proposed` unless the user says it's final.
3. If it replaces an older decision: set the new note's `supersedes`, set the old note's `superseded_by` and `status: superseded`. This is the only edit allowed on a final decision.
4. Link it from the project under `## Decisions`.

## weekly review

1. Create `60-Briefs/YYYY-Www-weekly-review.md`.
2. Sections:
   - **Meetings this week** — one line each, with outcome
   - **Decisions made** — `final` decisions dated this week
   - **Stale projects** — `status: active` projects whose `updated` is older than 10 days
   - **Open follow-ups** — every `#follow-up` not yet done
   - **Inbox health** — count of unprocessed items
3. Do not change any project status. Suggest changes as open questions.
