# STORM Research — a Claude Code skill

Turn a **decision question** into a **source-verified, multi-perspective HTML briefing**.
`storm-research` is a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill
that runs a STORM-inspired research pipeline: it fans out five independent "lens"
subagents, maps where they agree and collide, synthesizes a draft, then adversarially
verifies every claim before writing the report.

**▶ Live example briefing:** https://az9713.github.io/STORM-research-skill/

> **Credit / inspiration.** Reverse-engineered from the YouTube walkthrough
> **"Stanford's Method Turns Claude Into a PHD Level Research Team"**
> — https://www.youtube.com/watch?v=Tj3018n5MVg&t=14s.
> This is a rebuilt *approximation* from the video, not the original private skill.
> "STORM" refers to Stanford's multi-perspective research method (Synthesis of Topic
> Outlines through Retrieval and Multi-perspective question asking).

## What it produces

A self-contained HTML briefing with: a 60-second summary, reliability-ranked findings
(each with per-lens support/challenge notes), core assumptions, the missing stakeholder
lens, practical takeaways, and a **source-verification table** labelling each claim
`Confirmed` / `Corrected` / `Demoted`. It informs a decision — it does not issue a verdict,
and surfaces uncertainty on purpose.

See the **[live briefing](https://az9713.github.io/STORM-research-skill/)** (or the source
[`storm-llm-essays-briefing.html`](storm-llm-essays-briefing.html)) for a full example
run (topic: *should a high-school department permit LLMs on graded essays?*).

## The five lenses (parallel subagents)

The pipeline launches five subagents **simultaneously and blind to one another** — so any
agreement between them is independent convergence, which is stronger evidence than a single
chain of reasoning. Each does its own live web research.

| Lens | Role |
|---|---|
| 🔧 **Practitioner** | What works in practice, what setup is needed, what breaks first. |
| 🎓 **Academic** | What the peer-reviewed evidence actually supports; methodology limits. |
| 🕵 **Skeptic** | Red-teams *all* sides — hype, unsupported assumptions, failure modes. |
| 💰 **Economist** | Costs, ROI, incentives, who pays and who benefits. |
| 📜 **Historian** | Prior adoption cycles, analogies, repeated failure patterns. |

## The process (6 phases)

```
1. Scope        → frame the decision, reader, and must-answer questions
2. Five lenses  → parallel subagents research independently (no cross-talk)
3. Contradiction map → where lenses agree, collide, and what's weakly evidenced
4. Synthesis (V1)    → reliability-ranked draft; disagreement preserved, not averaged
5. Verification (V2) → adversarially check every name/number/date; label sources
6. HTML briefing     → render the verified report
```

The main session orchestrates; subagents never talk to each other, so the contradiction
map is the only place their outputs meet.

## Install

Copy the skill into your personal Claude Code skills directory:

```bash
cp -r .claude/skills/storm-research ~/.claude/skills/storm-research
```

(Or keep it project-scoped in any repo's `.claude/skills/`.)

## Use

Natural language (auto-triggers) or `/storm-research`:

> "Run STORM research on `<decision>`, for `<who>` deciding `<what>` by `<when>`."

**Good topics** are real decisions with bull/bear tension, costs, history, and verifiable
claims. **Poor topics** are single-fact lookups, how-to/code, live-precision data, or
settled consensus.

## Layout

```
.claude/skills/storm-research/
  SKILL.md          # contract Claude loads; frontmatter auto-triggers the skill
  USAGE.md          # install + invoke guide, JSON shape, customization
  DOCUMENTATION.md  # full dissection of every file, use cases, showcases
  prompts/          # phase-0, 5× lens-*, phase-2/3/4 — one file per pipeline step
  assets/report_template.html      # {{placeholder}} HTML shell, inline CSS, no JS
  scripts/render_storm_report.py   # optional stdlib renderer: briefing.json → HTML
  references/source-basis.md
storm-llm-essays-briefing.html     # example output
```

## Notes & limitations

- A full run launches 5 parallel subagents + verification — **token-heavy**, a few minutes.
- Output is **not financial/legal advice**; it informs, it does not advise.
- Known gaps (documented, not yet fixed): the HTML template folds the "missing lens" note
  into `{{assumptions}}` rather than its own placeholder; the Python renderer lists findings
  in JSON order rather than sorting by `reliability`.

## License

No license specified — all rights reserved by the author unless stated otherwise.
