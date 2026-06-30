#!/usr/bin/env python3
"""Render a STORM briefing JSON file into the bundled HTML template."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def paras(items: object) -> str:
    if isinstance(items, str):
        items = [items]
    return "\n".join(f"<p>{esc(item)}</p>" for item in (items or []))


def render_findings(findings: list[dict]) -> str:
    parts = []
    for finding in findings:
        parts.append(
            '<article class="finding">'
            f'<span class="badge">Reliability: {esc(finding.get("reliability", "unrated"))}</span>'
            f'<h3>{esc(finding.get("title", "Finding"))}</h3>'
            f'<p>{esc(finding.get("claim", ""))}</p>'
            f'<p><strong>Supported by:</strong> {esc(", ".join(finding.get("supported_by", [])))}</p>'
            f'<p><strong>Challenged by:</strong> {esc(", ".join(finding.get("challenged_by", [])))}</p>'
            "</article>"
        )
    return "\n".join(parts)


def render_sources(sources: list[dict]) -> str:
    rows = ["<table><thead><tr><th>Source</th><th>Status</th><th>Note</th></tr></thead><tbody>"]
    for source in sources:
        rows.append(
            "<tr>"
            f"<td>{esc(source.get('source', ''))}</td>"
            f"<td>{esc(source.get('status', ''))}</td>"
            f"<td>{esc(source.get('note', ''))}</td>"
            "</tr>"
        )
    rows.append("</tbody></table>")
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_html", type=Path)
    parser.add_argument("--template", type=Path, default=Path(__file__).parents[1] / "assets" / "report_template.html")
    args = parser.parse_args()

    data = json.loads(args.input_json.read_text(encoding="utf-8"))
    template = args.template.read_text(encoding="utf-8")
    replacements = {
        "title": esc(data.get("title", "STORM Research Briefing")),
        "subtitle": esc(data.get("subtitle", "")),
        "summary": paras(data.get("summary", [])),
        "findings": render_findings(data.get("findings", [])),
        "assumptions": paras(data.get("assumptions", [])),
        "takeaways": paras(data.get("takeaways", [])),
        "sources": render_sources(data.get("sources", [])),
    }
    rendered = template
    for key, value in replacements.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    args.output_html.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
