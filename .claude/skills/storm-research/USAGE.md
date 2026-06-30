# Using STORM Research In Claude Code

This folder is a Claude Code-oriented reconstruction of Nate Herk's STORM workflow. It is not Nate's original private skill file; it is a practical package based on the transcript.

## Install

Copy or move this folder into your Claude skills area:

```text
~/.claude/skills/storm-research/
```

If your Claude Code setup uses a project-local skill folder, place it there instead. Keep the folder structure intact:

```text
storm-research/
  SKILL.md
  prompts/
  assets/
  scripts/
  references/
```

## Basic Invocation

In Claude Code, ask naturally:

```text
Run STORM research on voice AI agents for an AI educator deciding whether the topic is worth a video.
```

You can also give business context:

```text
Run STORM research on AI customer-support agents for a mid-market SaaS company. The reader is a COO deciding whether to pilot this in Q3.
```

## What Claude Code Should Do

The main Claude session should orchestrate the pipeline:

1. Scope the topic with `prompts/phase-0-scope-topic.md`.
2. Launch five subagents when available:
   - practitioner
   - academic
   - skeptic
   - economist
   - historian
3. Compare the five outputs with `prompts/phase-2-contradiction-map.md`.
4. Synthesize V1 with `prompts/phase-3-synthesis.md`.
5. Verify claims and citations with `prompts/phase-4-peer-review-verification.md`.
6. Produce a V2 HTML briefing using `assets/report_template.html`.

Subagents report back to the main session; they do not talk directly to one another. The contradiction-map phase is where their views are compared.

## Expected Output

The final briefing should include:

- 60-second summary.
- Reliability-ranked key findings.
- Which lenses supported or challenged each finding.
- Assumptions the briefing depends on.
- Missing sixth lens or stakeholder gap.
- Practical takeaways.
- Source verification table with `confirmed`, `corrected`, or `demoted` labels.

## Optional HTML Rendering Script

If Claude creates a structured JSON briefing, render it with:

```powershell
python .\scripts\render_storm_report.py .\briefing.json .\storm-briefing.html
```

The JSON should use this shape:

```json
{
  "title": "STORM Briefing",
  "subtitle": "Reader and decision context",
  "summary": ["One or more paragraphs."],
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
    {
      "source": "Source name or URL",
      "status": "confirmed",
      "note": "Why it supports the claim."
    }
  ]
}
```

## Customization

Edit the prompt files if you want a different research council.

Common additions:

- `customer` lens for buyer/user impact.
- `frontline-employee` lens for implementation friction.
- `regulator` lens for compliance-heavy domains.
- `beginner` lens for education products.
- `content-creator` lens for video or newsletter strategy.

If you add a lens, update `SKILL.md` and the contradiction-map prompt so Claude knows to include it.
