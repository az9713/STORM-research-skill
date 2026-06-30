---
name: storm-research
description: Turn a topic into a verified multi-perspective HTML briefing using a STORM-inspired Claude Code workflow with practitioner, academic, skeptic, economist, and historian lenses.
---

# STORM Research

Use this skill when the user asks for STORM research, multi-perspective research, source-verified research briefings, or a Nate Herk-style research pipeline.

This is a reverse-engineered operational approximation based on the Nate Herk video transcript, not the original private skill file.

## Required Inputs

- Research topic.
- Reader or decision context, if known.
- Optional business/user context for tailoring.

If the topic is vague, ask up to three clarifying questions before running the pipeline.

## Pipeline

1. Scope the topic using `prompts/phase-0-scope-topic.md`.
2. Launch five subagents in parallel when available:
   - practitioner
   - academic
   - skeptic
   - economist
   - historian
3. Use `prompts/phase-2-contradiction-map.md` to compare lens outputs.
4. Use `prompts/phase-3-synthesis.md` to create V1 of the report.
5. Use `prompts/phase-4-peer-review-verification.md` to verify claims and citations.
6. Deliver a V2 HTML briefing using `assets/report_template.html`.

## Output

Create a self-contained HTML report with:

- 60-second summary.
- Key findings ranked by reliability.
- Lens support and challenge notes.
- Assumptions.
- Missing sixth lens or stakeholder gap.
- Practical takeaways.
- Source verification table with confirmed, corrected, or demoted labels.

## Claude Code Behavior

- Prefer subagents for the five lenses.
- Keep the main session responsible for orchestration, contradiction mapping, synthesis, and final verification.
- Remember that subagents do not talk to one another; use the contradiction map to compare their outputs.
- If the user asks for a deeper council/debate, propose an agent-team version separately because it is more expensive.
- Save the final HTML report in the current project unless the user specifies another path.
