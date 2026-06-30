# STORM_nate_herk — project context

This project packages **one Claude Code skill**: `storm-research`, a
reverse-engineered approximation of Nate Herk's STORM multi-perspective
research workflow ([video](https://www.youtube.com/watch?v=Tj3018n5MVg), see
`README.txt`). It is *not* Nate's original private skill — it's rebuilt from the
transcript.

## What the skill does

Turns a **decision question** into a **source-verified, multi-lens HTML
briefing** via a 6-step pipeline: scope → 5 parallel lens subagents →
contradiction map → synthesis (V1) → adversarial verification (V2) → HTML.

The **five lenses are hardcoded** (one `prompts/lens-*.md` each), not chosen
dynamically: practitioner · academic · skeptic · economist · historian.

## Layout

```
.claude/skills/storm-research/
  SKILL.md                 # contract Claude loads; frontmatter desc auto-triggers the skill
  USAGE.md                 # install + invoke guide; JSON shape; customization
  DOCUMENTATION.md         # full dissection of every file, use cases, showcases (I wrote this)
  prompts/                 # phase-0, 5x lens-*, phase-2/3/4 — one file per pipeline step
  assets/report_template.html   # {{placeholder}} HTML shell, inline CSS, no JS
  scripts/render_storm_report.py # optional stdlib renderer: briefing.json -> HTML
  references/source-basis.md
README.txt                 # just the source YouTube URL
CLAUDE.md                  # this file
```

## How to invoke

Natural language (auto-matches) or `/storm-research`:
> "Run STORM research on `<decision>`, for `<who>` deciding `<what>` by `<when>`."

Good topics = a real **decision** with bull+bear tension, costs, history, and
implementation friction, where claims are verifiable. Bad topics = single-fact
lookups, how-to/code, live-precision data, settled consensus, definitive
verdicts. Full rationale + 7 showcase examples in `DOCUMENTATION.md`.

## Known limitations (real, found by reading the code)

1. `report_template.html` heading says "Assumptions **And Missing Lens**" but
   has no separate `{{missing_lens}}` placeholder — missing-lens note must fold
   into `{{assumptions}}`.
2. `render_storm_report.py` renders findings in **JSON order**; it does *not*
   sort by `reliability` despite the "reliability-ranked" spec.

Both are documented but **not yet fixed**. User was offered the fix; pending.

## Notes

- A full run launches 5 parallel subagents + verification — token-heavy, few
  minutes. Output surfaces uncertainty on purpose; it does not give a single
  verdict (informs, doesn't advise — e.g. investment topics are not financial
  advice).
- No build/test/deps — the only executable is the stdlib-only Python renderer.
- Adding/swapping a lens = new `prompts/lens-<name>.md` + update `SKILL.md`'s
  list and `phase-2-contradiction-map.md` (per `USAGE.md` customization).
