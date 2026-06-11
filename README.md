# cvp-fifer org defaults

Org-default community health files: issue forms, a PR template, and CLI body
skeletons. Every repo in the org — including future ones — inherits these
automatically unless it overrides them (see [the override caveat](#the-override-caveat)).

> **This repository is PUBLIC** (GitHub requires it for org-wide defaults).
> Everything in it stays generic: no internal ticket IDs, customer names,
> hostnames, or agency identifiers — the same rule as commit messages.

## Picking a template

| Template | Use when |
|---|---|
| **Bug report** | Something is broken or behaving wrong. |
| **Feature / Story** | New capability, framed as a user story. |
| **Task / Chore** | Concrete work item — no story framing needed. |
| **Epic** | A multi-issue outcome, tracked via sub-issues. |
| **Spike / Research** | A timeboxed investigation that informs a decision. |

Each template asks for the human essentials first (story or summary,
acceptance criteria, how to verify), then optional **🤖 fields** that give an
AI agent the context to pick the work up: code pointers, constraints, out of
scope. Fill in what you know, skip what you don't.

## Filing from the CLI (humans and agents)

The web forms and the skeletons in [`issue-bodies/`](issue-bodies/) produce
identical body structure. To file from the terminal:

```sh
cp issue-bodies/story.md /tmp/i.md && $EDITOR /tmp/i.md
gh issue create -R cvp-fifer/<repo> -t "<title>" -l feature -F /tmp/i.md
```

Each skeleton's header comment names the labels to pass. `gh issue create`
cannot set the issue *type* — labels are the CLI-portable signal; set the type
afterward in the web UI or via API if you need it.

## The heading contract

GitHub renders each form field as `### <label>` in the issue body; the
skeletons carry the same headings. Agents parse issues by these headings:

| Template | Headings, in order |
|---|---|
| bug | Summary · Severity · Steps to reproduce · Expected vs actual · Environment · 🤖 Code pointers · 🤖 Constraints & out of scope |
| story | Story · Acceptance criteria · How to verify · 🤖 Code pointers · 🤖 Constraints · 🤖 Out of scope |
| task | What needs doing · Done when · 🤖 Code pointers |
| epic | Outcome · Done when · Child work plan · 🤖 Constraints & out of scope |
| spike | Question · Timebox · Expected output · 🤖 Starting points |

Contract rules:

1. Headings are stable identifiers — never renamed without regenerating the
   skeletons and announcing the change.
2. A section containing only `_No response_` (form path) or only an HTML
   comment (skeleton path) means **empty**.
3. Dropdown sections (Severity, Timebox) contain exactly one of the
   enumerated option strings.
4. Headings prefixed `🤖 ` are optional advisory context for agents — never
   requirements.

## Issue types and labels

Bug, Task, and Feature are GitHub's built-in org issue types; **Epic** and
**Spike** are custom org types and must exist before the forms can reference
them. Auto-applied `labels:` silently no-op in repos where the label doesn't
exist — run [`scripts/seed_labels.sh`](scripts/seed_labels.sh) against every
new repo.

## The override caveat

> **⚠️ If a repo adds *any* file to its own `.github/ISSUE_TEMPLATE/`, GitHub
> ignores this entire org default set for that repo** — there is no merging.
> A repo that needs one custom form must copy all five forms plus
> `config.yml`. (A repo-level `PULL_REQUEST_TEMPLATE.md` or `SECURITY.md`
> overrides only that one file.)

## Maintaining the templates

Edit the form YAML in [`ISSUE_TEMPLATE/`](ISSUE_TEMPLATE/) only, then:

```sh
uv run scripts/gen_issue_bodies.py
```

Never hand-edit `issue-bodies/` — it is generated, and CI
([skeleton drift](.github/workflows/skeleton-drift.yml)) fails on any
divergence. Note that form `markdown` elements render only in the web form,
never in the submitted issue — the `🤖 ` label prefix, not a divider, is the
durable section marker.
