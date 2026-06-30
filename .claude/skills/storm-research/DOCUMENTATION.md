# STORM Research — Documentation

A reverse-engineered, Claude Code-native approximation of Nate Herk's STORM
multi-perspective research workflow ([source video](https://www.youtube.com/watch?v=Tj3018n5MVg)).
It turns a **decision question** into a **source-verified, multi-lens HTML briefing**
by fanning out five fixed "lenses" (subagents), mapping where they disagree,
synthesizing, and then adversarially verifying every major claim.

This document covers three things:

1. [Dissecting the skill](#1-dissecting-the-skill) — what every file does.
2. [When to use it (and when not to)](#2-when-to-use-it--and-when-not-to).
3. [Showcase examples](#3-showcase-examples).

---

## 1. Dissecting the skill

> `references/` is intentionally omitted from this dissection.

### Folder map

```
storm-research/
  SKILL.md                 # the contract Claude reads — what the skill is + the pipeline
  USAGE.md                 # human-facing how-to-install / how-to-invoke guide
  DOCUMENTATION.md         # this file
  prompts/                 # the actual instructions for each pipeline step
    phase-0-scope-topic.md
    lens-practitioner.md
    lens-academic.md
    lens-skeptic.md
    lens-economist.md
    lens-historian.md
    phase-2-contradiction-map.md
    phase-3-synthesis.md
    phase-4-peer-review-verification.md
  assets/
    report_template.html   # the {{placeholder}} HTML shell for the final briefing
  scripts/
    render_storm_report.py # optional: fills the template from a briefing.json
```

### Top-level files

**`SKILL.md`** — The entry point Claude loads when the skill triggers. Its
frontmatter `description` is what makes the skill auto-fire on phrases like
"STORM research" or "multi-perspective research". The body defines the
**6-step pipeline** (scope → 5 lenses → contradiction map → synthesis →
verification → HTML), the **required inputs** (topic, reader/decision context,
optional business context), and **orchestration rules** — most importantly:
*the main session orchestrates; subagents never talk to each other; their
views are only ever reconciled in the contradiction-map step.*

**`USAGE.md`** — The human guide: how to install the folder under
`~/.claude/skills/`, how to invoke it in natural language, what the output
should contain, the **JSON shape** the render script expects, and a
**customization** section showing how to add/swap lenses (e.g. a `customer`,
`regulator`, or `beginner` lens).

### `prompts/` — one file per pipeline step

The pipeline is just these prompt files executed in order. Each is short and
declarative — a role + a checklist of what to return.

| File | Role in pipeline | What it instructs |
|------|------------------|-------------------|
| `phase-0-scope-topic.md` | **Step 1 — Scope** | Turn the raw topic into: scoped topic, reader, decision context, why-now, must-answer questions, source requirements. Ask ≤3 clarifying questions *only if needed*, else proceed. |
| `lens-practitioner.md` | **Step 2 — Lens** | "Operator who must implement the idea." Returns: what works in practice, setup required, what breaks first, what the reader should do differently — with sources + confidence. |
| `lens-academic.md` | **Step 2 — Lens** | "Evidence reviewer." Returns: research support, definitions, methodology quality, limits of evidence, claims needing careful wording. |
| `lens-skeptic.md` | **Step 2 — Lens** | "Red-team reviewer." Returns: hype, unsupported assumptions, failure modes, incentive problems, claims that should be demoted. |
| `lens-economist.md` | **Step 2 — Lens** | "Economist." Returns: costs, ROI, incentives, adoption constraints, market structure, who pays / who benefits. |
| `lens-historian.md` | **Step 2 — Lens** | "Historian." Returns: analogies, prior adoption cycles, repeated failure patterns, institutional constraints, what history suggests happens next. |
| `phase-2-contradiction-map.md` | **Step 3 — Reconcile** | Compare the five lens reports: where they agree, where they contradict, which claims have strong vs. weak evidence, which lens/stakeholder is missing, which claims must be verified. This is the only place the five views meet. |
| `phase-3-synthesis.md` | **Step 4 — V1** | Build the V1 briefing: 60-sec summary, reliability-ranked findings, support/challenge notes per lens, assumptions, missing sixth lens, takeaways, source list. Explicit instruction: **do not smooth over real disagreement; make uncertainty visible.** |
| `phase-4-peer-review-verification.md` | **Step 5 — V2** | Adversarially review V1. Per major claim: confirm the source supports it, correct wording if only partial, demote/remove if weak, check names/dates/numbers/comparisons, tighten reliability ratings. Outputs final V2 + a source-verification table. |

**The five lenses are hardcoded.** There is exactly one `lens-*.md` per role;
the skill does not pick lenses dynamically. Every run uses the same council
unless you edit these files (and update `SKILL.md` + the contradiction-map
prompt to match — per `USAGE.md`).

### `assets/report_template.html`

A self-contained, dependency-free HTML shell (~1.5 KB, inline CSS, no JS).
It exposes seven `{{placeholder}}` tokens the render script fills:

`{{title}}`, `{{subtitle}}`, `{{summary}}`, `{{findings}}`,
`{{assumptions}}`, `{{takeaways}}`, `{{sources}}`.

Sections rendered: 60-Second Summary · Key Findings · Assumptions And Missing
Lens · Practical Takeaways · Source Verification.

> **Known limitation:** the heading reads "Assumptions **And Missing Lens**"
> but there is no dedicated `{{missing_lens}}` placeholder — the missing-lens
> note has to be folded into `{{assumptions}}`. If you want it called out
> separately, add a placeholder here and a matching key in the script.

### `scripts/render_storm_report.py`

Optional, stdlib-only (`argparse`, `html`, `json`, `pathlib`) — no pip
install. It reads a `briefing.json`, HTML-escapes every value (`esc()` uses
`html.escape(..., quote=True)`, so it's injection-safe), and string-replaces
the template placeholders.

```powershell
python .\scripts\render_storm_report.py .\briefing.json .\storm-briefing.html
```

Expected JSON shape:

```json
{
  "title": "STORM Briefing",
  "subtitle": "Reader and decision context",
  "summary": ["Paragraph one.", "Paragraph two."],
  "findings": [
    {
      "title": "Finding title",
      "claim": "Finding claim.",
      "reliability": "high",
      "supported_by": ["academic", "skeptic"],
      "challenged_by": ["economist"]
    }
  ],
  "assumptions": ["Important assumption."],
  "takeaways": ["Practical takeaway."],
  "sources": [
    { "source": "Source name or URL", "status": "confirmed", "note": "Why it supports the claim." }
  ]
}
```

Helper functions: `paras()` wraps strings/lists into `<p>` tags;
`render_findings()` emits one `.finding` card per finding with a reliability
badge; `render_sources()` builds the verification `<table>`. `--template`
defaults to the bundled `assets/report_template.html`.

> **Known limitation:** despite the spec calling for "reliability-ranked"
> findings, the script renders findings in the **order given** — it does not
> sort by the `reliability` field. Order them yourself in the JSON, or add a
> sort in `render_findings()`.

> **Note:** the script is optional. Claude can also write the final HTML
> directly (filling the template inline) without producing a JSON file. The
> JSON+script path exists for reproducibility and re-rendering.

### End-to-end flow

```
topic ──▶ phase-0 scope ──▶ ┌─ practitioner ─┐
                            ├─ academic ─────┤
                            ├─ skeptic ──────┤──▶ phase-2 contradiction map
                            ├─ economist ────┤        │
                            └─ historian ────┘        ▼
                                              phase-3 synthesis (V1)
                                                       │
                                                       ▼
                                       phase-4 peer review + verify (V2)
                                                       │
                                                       ▼
                                   report_template.html  ◀─ (optional render_storm_report.py)
```

---

## 2. When to use it — and when not to

### What makes a topic STORM-good

The five lenses are generic **"should-we-adopt-this / is-this-claim-real"**
reviewers. The skill pays off when the question has all of:

- **It's a decision, not a fact lookup.** "Should X do Y?" / "Is Y worth it?"
  — not "what is Y?".
- **There's a genuine bull *and* bear case.** The skeptic lens needs something
  real to attack; the synthesis step is explicitly told *not to smooth over
  disagreement*.
- **Costs and incentives exist** (economist), **a track record exists**
  (historian), and **implementation has friction** (practitioner).
- **Claims can be checked against sources.** Phase 4 is the whole point —
  topics where claims are verifiable get the most value.
- **Multiple perspectives legitimately conflict.** If everyone agrees, you
  don't need five lenses.

### Best-fit use cases

- **Technology / tool adoption** — "Should we roll out AI coding assistants?"
- **Business strategy** — pricing-model changes, build-vs-buy, market entry.
- **Public policy / civic decisions** — 4-day week, zoning, a pilot program.
- **Health & lifestyle interventions** — diets, training protocols, supplements.
- **Education / EdTech policy** — LLMs in classrooms, grading changes.
- **Climate / infrastructure choices** — heat pumps, solar, EV fleet.
- **Investment theses** — bull/bear on a stock (informs, doesn't advise).

### Poor-fit use cases (use something else)

| Don't use STORM for… | Why | Use instead |
|----------------------|-----|-------------|
| **Single-fact lookups** ("capital of Peru", "what's React's latest version") | No perspectives to reconcile; five lenses is pure overhead. | A direct search / one web fetch. |
| **Pure how-to / code tasks** ("center this div", "write a regex") | No bull/bear tension; nothing for the skeptic to red-team. | Just do the task. |
| **Real-time precision data** (live stock price, today's exact metric) | Output is only as fresh as what subagents fetch; it reasons, it isn't a data feed. | A live API / terminal, then feed numbers in. |
| **Settled consensus questions** ("does smoking cause cancer") | Lenses won't disagree; no contradiction map to build. | A summary source. |
| **Personal/private decisions needing your data** ("should *I* take this job") | The council can't see your situation; it generalizes. | A structured 1:1 conversation. |
| **Anything needing a definitive verdict / professional advice** (medical, legal, "just tell me buy or sell") | Output is a ranked-uncertainty briefing, *not* a recommendation. | A licensed professional. |

### Cost & expectation notes

- A full run launches **five parallel subagents + verification** — it's
  token-heavy and takes a few minutes. Not for quick questions.
- The output **surfaces uncertainty on purpose**; it will not hand you a
  single clean answer. That's a feature for decisions, a bug for "just tell me".
- Freshness is bounded by subagent retrieval. For "right now" questions, the
  briefing flags low-confidence claims rather than inventing precision.

---

## 3. Showcase examples

Each is phrased the way the skill wants: **topic + who's deciding + what they
decide.** The lens column shows why the fixed council earns its keep.

### A. Technology adoption (B2B)
> "Run STORM research on adopting AI coding assistants org-wide, for a
> 200-engineer VP of Engineering deciding whether to roll out in Q4."

- economist → seat cost vs. measured productivity · skeptic → "10x" hype,
  IP/security leakage · historian → past dev-tool waves (IDEs, low-code) ·
  practitioner → what breaks in real workflows · academic → what the
  productivity studies actually measure.

### B. Business strategy / pricing
> "Run STORM research on moving from seat-based to usage-based pricing, for a
> SaaS founder deciding before the next fundraise."

- economist → revenue predictability, margins · skeptic → churn / billing-shock
  risk · historian → companies that switched (Snowflake, Twilio) · practitioner
  → billing infra & sales-motion changes · academic → pricing-research evidence.

### C. Public policy / civic
> "Run STORM research on a 4-day work week, for a city council deciding whether
> to pilot it for municipal staff."

- economist → cost, productivity, who pays · historian → prior trials (Iceland,
  NZ firms) · skeptic → selection bias in those trials · practitioner →
  coverage/scheduling friction · academic → how 'success' was measured.

### D. Health / lifestyle
> "Run STORM research on whether intermittent fasting (16:8) is worth adopting,
> for a healthy 40-year-old deciding on a 6-month trial."

- academic → RCT evidence quality · skeptic → overstated claims, adherence
  dropout · economist → opportunity cost vs. simpler changes · practitioner →
  what actually sticks day-to-day · historian → past diet-fad cycles.

### E. Education / EdTech policy
> "Run STORM research on letting students use LLMs for graded essays, for a
> high-school department head deciding next year's policy."

- academic → learning-outcome evidence · skeptic → cheating & skill-atrophy
  risk · economist → grading-time savings vs. integrity cost · practitioner →
  classroom enforcement reality · historian → calculators-in-math precedent.

### F. Climate / infrastructure
> "Run STORM research on residential heat pumps replacing gas furnaces, for a
> homeowner in a cold climate deciding this year."

- economist → install cost, payback, subsidies · practitioner → performance at
  -15°C, retrofit headaches · skeptic → optimistic vendor efficiency numbers ·
  historian → prior electrification pushes · academic → field-performance data.

### G. Investment thesis (informs, does not advise)
> "Run STORM research on the bull vs. bear case for Alphabet (GOOGL) as a 3-year
> hold, for a retail investor deciding whether to start a position now. Weight:
> AI/search-disruption risk, ad-revenue durability, Cloud/Waymo optionality,
> antitrust overhang, and valuation vs. peers."

- economist → valuation / macro · skeptic → search disruption + antitrust ·
  historian → past Big-Tech antitrust cycles · practitioner → ad-market reality
  · academic → AI competitive dynamics.
  *(Note: practitioner is the weakest fit for a pure stock decision; swap to a
  finance-native lens if you customize.)*

### The pattern

> A topic is STORM-good when it's a **decision** with a **real bull and bear
> case**, **costs/incentives** (economist), a **history** (historian), and
> **implementation friction** (practitioner) — and the claims can be
> **verified against sources** (phase 4). Drop the topic into the template
> "**Run STORM research on `<decision>`, for `<who>` deciding `<what>` by
> `<when>`.**" and the council does the rest.
