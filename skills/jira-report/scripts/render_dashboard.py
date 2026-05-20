#!/usr/bin/env python3
"""Render a CETIN-branded HTML dashboard from a JIRA metrics JSON."""
from __future__ import annotations

import argparse
import json
import html
import math
from datetime import datetime
from pathlib import Path

# CETIN brand tokens
CETIN_BLUE = "#003DA5"
CETIN_BLUE_DARK = "#002A73"
CETIN_BLUE_LIGHT = "#E5EDF8"
CETIN_RED = "#E4002B"
CETIN_RED_LIGHT = "#FCE5EA"
CETIN_GRAY = "#54595F"
CETIN_GRAY_LIGHT = "#F4F5F7"
CETIN_BORDER = "#D7DCE0"
CETIN_SUCCESS = "#2E7D32"
CETIN_WARN = "#ED6C02"

# Palette for categorical charts
PALETTE = [
    CETIN_BLUE, CETIN_RED, "#0091EA", "#F9A825", CETIN_SUCCESS,
    "#7B1FA2", "#00897B", "#5D4037", "#C2185B", CETIN_GRAY,
]


def esc(s) -> str:
    return html.escape(str(s) if s is not None else "")


def svg_donut(items, size=220, stroke=44):
    """Render an SVG donut chart from [{label, count}, ...]."""
    total = sum(i["count"] for i in items) or 1
    r = (size - stroke) / 2
    cx = cy = size / 2
    circumference = 2 * math.pi * r
    offset = 0
    segments = []
    for idx, item in enumerate(items):
        color = PALETTE[idx % len(PALETTE)]
        frac = item["count"] / total
        length = frac * circumference
        segments.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
            f'stroke="{color}" stroke-width="{stroke}" '
            f'stroke-dasharray="{length:.2f} {circumference - length:.2f}" '
            f'stroke-dashoffset="{-offset:.2f}" transform="rotate(-90 {cx} {cy})">'
            f'<title>{esc(item["label"])}: {item["count"]}</title></circle>'
        )
        offset += length
    center_text = (
        f'<text x="{cx}" y="{cy - 4}" text-anchor="middle" '
        f'font-size="26" font-weight="700" fill="{CETIN_BLUE}">{total}</text>'
        f'<text x="{cx}" y="{cy + 18}" text-anchor="middle" '
        f'font-size="11" fill="{CETIN_GRAY}">TOTAL</text>'
    )
    return (
        f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" '
        f'xmlns="http://www.w3.org/2000/svg">{"".join(segments)}{center_text}</svg>'
    )


def svg_legend(items):
    rows = []
    total = sum(i["count"] for i in items) or 1
    for idx, item in enumerate(items):
        color = PALETTE[idx % len(PALETTE)]
        pct = round(100 * item["count"] / total, 1)
        rows.append(
            f'<div class="legend-row">'
            f'<span class="swatch" style="background:{color}"></span>'
            f'<span class="legend-label">{esc(item["label"])}</span>'
            f'<span class="legend-count">{item["count"]} <span class="muted">({pct}%)</span></span>'
            f'</div>'
        )
    return f'<div class="legend">{"".join(rows)}</div>'


def hbar(items, max_value=None, color=CETIN_BLUE, height=22):
    """Horizontal bar chart from [{label, count}, ...]."""
    if not items:
        return '<div class="muted">No data</div>'
    max_v = max_value or max((i["count"] for i in items), default=1) or 1
    rows = []
    for item in items:
        pct = 100 * item["count"] / max_v if max_v else 0
        rows.append(
            f'<div class="hbar-row">'
            f'<div class="hbar-label">{esc(item["label"])}</div>'
            f'<div class="hbar-track"><div class="hbar-fill" '
            f'style="width:{pct:.1f}%;background:{color};height:{height}px"></div></div>'
            f'<div class="hbar-count">{item["count"]}</div>'
            f'</div>'
        )
    return f'<div class="hbar">{"".join(rows)}</div>'


def kpi_card(label, value, accent=CETIN_BLUE, sublabel=None):
    sub = f'<div class="kpi-sub">{esc(sublabel)}</div>' if sublabel else ""
    return (
        f'<div class="kpi" style="border-top-color:{accent}">'
        f'<div class="kpi-value" style="color:{accent}">{esc(value)}</div>'
        f'<div class="kpi-label">{esc(label)}</div>'
        f'{sub}</div>'
    )


def table(headers, rows, classes=""):
    th = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body_rows = []
    for r in rows:
        tds = "".join(f"<td>{esc(c)}</td>" for c in r)
        body_rows.append(f"<tr>{tds}</tr>")
    return (
        f'<table class="data {classes}"><thead><tr>{th}</tr></thead>'
        f'<tbody>{"".join(body_rows) or "<tr><td colspan=99 class=muted>No rows</td></tr>"}</tbody></table>'
    )


def render(metrics: dict) -> str:
    generated_at = metrics.get("generated_at", datetime.utcnow().isoformat())
    source = metrics.get("source_file", "—")
    total = metrics.get("total_issues", 0)

    if metrics.get("empty") or total == 0:
        body = (
            '<div class="empty"><h1>No issues found</h1>'
            '<p>The provided JIRA export does not contain any rows.</p></div>'
        )
        return wrap_html(body, source, generated_at)

    kpis = metrics.get("kpis", {})
    kpi_html = (
        kpi_card("Total issues", kpis.get("total", 0))
        + kpi_card("Open", kpis.get("open", 0), CETIN_WARN)
        + kpi_card("In progress", kpis.get("in_progress", 0), "#0091EA")
        + kpi_card("Done", f"{kpis.get('done_pct', 0)}%", CETIN_SUCCESS,
                   sublabel=f"{kpis.get('done', 0)} of {kpis.get('total', 0)}")
        + kpi_card("Blockers", kpis.get("blockers", 0), CETIN_RED)
    )

    sections = []

    # A. Status overview
    if "by_status" in metrics:
        donut = svg_donut(metrics["by_status"])
        legend = svg_legend(metrics["by_status"])
        type_bar = hbar(metrics.get("by_type", []), color=CETIN_BLUE)
        assignee_bar = hbar(metrics.get("by_assignee", []), color=CETIN_BLUE_DARK)
        priority_bar = hbar(metrics.get("by_priority", []), color=CETIN_RED)
        sections.append(f'''
        <section class="card">
          <h2>Status overview</h2>
          <div class="grid-2">
            <div>
              <h3>By status</h3>
              <div class="donut-wrap">{donut}{legend}</div>
            </div>
            <div>
              <h3>By issue type</h3>{type_bar}
              <h3 style="margin-top:18px">By priority</h3>{priority_bar}
            </div>
          </div>
          <h3 style="margin-top:20px">Top assignees</h3>{assignee_bar}
        </section>
        ''')

    # B. Sprint / velocity
    sprints = metrics.get("sprints") or []
    if sprints:
        velocity = metrics.get("velocity_last6", [])
        velocity_chart = hbar(
            [{"label": s["sprint"], "count": s["points_done"]} for s in velocity],
            color=CETIN_BLUE,
        )
        current = metrics.get("current_sprints", [])
        current_html = ""
        if current:
            cur_rows = [s for s in sprints if s["sprint"] in current]
            cards = []
            for s in cur_rows:
                pct = s["done_pct"]
                cards.append(f'''
                <div class="sprint-card">
                  <div class="sprint-name">{esc(s["sprint"])}</div>
                  <div class="sprint-meta">{s["done"]} / {s["issues"]} issues · {s["points_done"]} / {s["points_total"]} pts</div>
                  <div class="progress"><div class="progress-fill" style="width:{pct}%"></div></div>
                  <div class="sprint-pct">{pct}% done</div>
                </div>
                ''')
            current_html = f'<div class="sprint-grid">{"".join(cards)}</div>'

        sprint_table = table(
            ["Sprint", "Issues", "Done", "% done", "Points planned", "Points done"],
            [
                [s["sprint"], s["issues"], s["done"], f"{s['done_pct']}%",
                 s["points_total"], s["points_done"]]
                for s in sprints
            ],
        )
        sections.append(f'''
        <section class="card">
          <h2>Sprint &amp; velocity</h2>
          {current_html}
          <h3>Velocity — last 6 sprints (story points done)</h3>
          {velocity_chart}
          <h3 style="margin-top:18px">All sprints</h3>
          {sprint_table}
        </section>
        ''')

    # C. Aging & blockers
    if "aging_buckets" in metrics:
        aging_chart = hbar(metrics["aging_buckets"], color=CETIN_RED)
        stale = metrics.get("stale_count", 0)
        oldest = metrics.get("oldest_open", [])
        oldest_table = table(
            ["Key", "Summary", "Status", "Assignee", "Age (days)"],
            [
                [r["key"], r["summary"], r["status"], r["assignee"], r["age_days"]]
                for r in oldest
            ],
        )
        sections.append(f'''
        <section class="card">
          <h2>Aging &amp; blockers</h2>
          <div class="grid-2">
            <div>
              <h3>Open issues by age</h3>
              {aging_chart}
              <p class="muted" style="margin-top:10px">Stale (no update 14+ days): <b>{stale}</b></p>
            </div>
            <div>
              <h3>Top 10 oldest open</h3>
              {oldest_table}
            </div>
          </div>
        </section>
        ''')

    if metrics.get("blocker_list"):
        blocker_table = table(
            ["Key", "Summary", "Status", "Priority", "Assignee"],
            [
                [r["key"], r["summary"], r["status"], r["priority"], r["assignee"]]
                for r in metrics["blocker_list"]
            ],
        )
        sections.append(f'''
        <section class="card">
          <h2>Blocker list</h2>
          {blocker_table}
        </section>
        ''')

    # D. Project & epic breakdown
    if metrics.get("by_project"):
        proj_table = table(
            ["Project", "Issues", "Done", "% done"],
            [[r["project"], r["issues"], r["done"], f"{r['done_pct']}%"]
             for r in metrics["by_project"]],
        )
        sections.append(f'''
        <section class="card">
          <h2>Projects</h2>
          {proj_table}
        </section>
        ''')

    if metrics.get("by_epic"):
        epic_rows = []
        for r in metrics["by_epic"]:
            pct = r["done_pct"]
            bar = (
                f'<div class="progress mini"><div class="progress-fill" '
                f'style="width:{pct}%"></div></div>'
            )
            epic_rows.append([
                r["epic"], r["issues"], r["done"], f"{pct}%", bar
            ])
        # Manually build so bar is raw HTML (not escaped)
        thead = "<tr>" + "".join(f"<th>{h}</th>" for h in
                ["Epic", "Issues", "Done", "% done", "Progress"]) + "</tr>"
        tbody_rows = []
        for r in epic_rows:
            cells = "".join(
                f"<td>{c if i == 4 else esc(c)}</td>" for i, c in enumerate(r)
            )
            tbody_rows.append(f"<tr>{cells}</tr>")
        epic_table = (
            f'<table class="data"><thead>{thead}</thead>'
            f'<tbody>{"".join(tbody_rows)}</tbody></table>'
        )
        sections.append(f'''
        <section class="card">
          <h2>Epics</h2>
          {epic_table}
        </section>
        ''')

    if metrics.get("by_component"):
        comp_bar = hbar(metrics["by_component"], color=CETIN_BLUE_DARK)
        sections.append(f'''
        <section class="card">
          <h2>Components</h2>
          {comp_bar}
        </section>
        ''')

    missing = metrics.get("missing_sections", [])
    missing_html = ""
    if missing:
        missing_html = (
            '<div class="note">Some sections were omitted because these '
            f'columns were missing from the export: <b>{esc(", ".join(missing))}</b>.</div>'
        )

    body = f'''
      <div class="kpis">{kpi_html}</div>
      {missing_html}
      {"".join(sections)}
    '''
    return wrap_html(body, source, generated_at)


def wrap_html(body: str, source: str, generated_at: str) -> str:
    try:
        gen_dt = datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
        gen_str = gen_dt.strftime("%d %b %Y %H:%M UTC")
    except Exception:
        gen_str = generated_at

    css = f"""
    :root {{
      --blue: {CETIN_BLUE};
      --blue-dark: {CETIN_BLUE_DARK};
      --blue-light: {CETIN_BLUE_LIGHT};
      --red: {CETIN_RED};
      --red-light: {CETIN_RED_LIGHT};
      --gray: {CETIN_GRAY};
      --gray-light: {CETIN_GRAY_LIGHT};
      --border: {CETIN_BORDER};
      --success: {CETIN_SUCCESS};
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: 'Avenir', 'Avenir Next', 'Segoe UI', Arial, sans-serif;
      background: var(--gray-light);
      color: #1A1A1A;
      margin: 0;
      padding: 24px;
      line-height: 1.45;
    }}
    .container {{ max-width: 1280px; margin: 0 auto; }}
    header.report {{
      background: var(--blue);
      color: white;
      padding: 24px 28px;
      border-radius: 8px 8px 0 0;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    header.report .brand {{
      font-weight: 800;
      font-size: 22px;
      letter-spacing: 1px;
    }}
    header.report .meta {{
      text-align: right;
      font-size: 13px;
      opacity: 0.85;
    }}
    header.report h1 {{
      margin: 0;
      font-size: 26px;
      font-weight: 700;
    }}
    .kpis {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 12px;
      padding: 20px 0;
    }}
    .kpi {{
      background: white;
      border: 1px solid var(--border);
      border-top: 4px solid var(--blue);
      border-radius: 6px;
      padding: 18px 16px;
    }}
    .kpi-value {{ font-size: 32px; font-weight: 800; line-height: 1; }}
    .kpi-label {{ font-size: 12px; color: var(--gray); margin-top: 6px; text-transform: uppercase; letter-spacing: 0.5px; }}
    .kpi-sub {{ font-size: 12px; color: var(--gray); margin-top: 4px; }}
    .card {{
      background: white;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 22px 24px;
      margin-bottom: 16px;
    }}
    .card h2 {{
      margin: 0 0 16px 0;
      font-size: 18px;
      color: var(--blue);
      border-bottom: 2px solid var(--blue-light);
      padding-bottom: 8px;
    }}
    .card h3 {{
      margin: 12px 0 8px 0;
      font-size: 13px;
      text-transform: uppercase;
      color: var(--gray);
      letter-spacing: 0.5px;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }}
    .donut-wrap {{ display: flex; gap: 18px; align-items: center; }}
    .legend {{ flex: 1; }}
    .legend-row {{
      display: flex; align-items: center; gap: 8px;
      padding: 4px 0; font-size: 13px;
      border-bottom: 1px dashed var(--border);
    }}
    .legend-row:last-child {{ border: 0; }}
    .swatch {{ width: 12px; height: 12px; border-radius: 2px; flex: 0 0 auto; }}
    .legend-label {{ flex: 1; }}
    .legend-count {{ font-weight: 600; }}
    .muted {{ color: var(--gray); font-size: 12px; }}
    .hbar-row {{
      display: grid;
      grid-template-columns: 160px 1fr 50px;
      align-items: center;
      gap: 10px;
      padding: 3px 0;
      font-size: 13px;
    }}
    .hbar-label {{ text-overflow: ellipsis; overflow: hidden; white-space: nowrap; }}
    .hbar-track {{ background: var(--gray-light); border-radius: 3px; overflow: hidden; }}
    .hbar-fill {{ background: var(--blue); border-radius: 3px; }}
    .hbar-count {{ text-align: right; font-weight: 600; }}
    table.data {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    table.data th {{
      text-align: left;
      background: var(--blue-light);
      color: var(--blue-dark);
      padding: 8px 10px;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.4px;
      cursor: pointer;
      user-select: none;
    }}
    table.data th::after {{ content: ' ⇅'; opacity: 0.4; font-size: 10px; }}
    table.data td {{
      padding: 7px 10px;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
    }}
    table.data tbody tr:hover {{ background: #FAFBFC; }}
    .sprint-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 12px;
      margin-bottom: 18px;
    }}
    .sprint-card {{
      background: var(--blue-light);
      border-radius: 6px;
      padding: 14px 16px;
    }}
    .sprint-name {{ font-weight: 700; color: var(--blue-dark); }}
    .sprint-meta {{ font-size: 12px; color: var(--gray); margin-top: 4px; }}
    .progress {{
      background: white;
      height: 12px;
      border-radius: 6px;
      overflow: hidden;
      margin-top: 8px;
    }}
    .progress.mini {{ height: 8px; }}
    .progress-fill {{
      background: var(--blue);
      height: 100%;
    }}
    .sprint-pct {{ font-size: 12px; margin-top: 4px; color: var(--blue-dark); font-weight: 600; }}
    .note {{
      background: #FFF8E1;
      border-left: 4px solid var(--red);
      padding: 10px 14px;
      border-radius: 4px;
      font-size: 13px;
      margin-bottom: 16px;
    }}
    footer.report {{
      text-align: center;
      color: var(--gray);
      font-size: 12px;
      padding: 24px 0;
    }}
    .empty {{ background: white; padding: 48px; text-align: center; border-radius: 8px; }}
    @media (max-width: 900px) {{
      .kpis {{ grid-template-columns: repeat(2, 1fr); }}
      .grid-2 {{ grid-template-columns: 1fr; }}
      .donut-wrap {{ flex-direction: column; }}
      .hbar-row {{ grid-template-columns: 110px 1fr 40px; }}
    }}
    @media print {{
      body {{ background: white; padding: 0; }}
      .card {{ break-inside: avoid; box-shadow: none; }}
      header.report {{ border-radius: 0; }}
    }}
    """

    sort_js = """
    document.querySelectorAll('table.data').forEach(function(t){
      t.querySelectorAll('th').forEach(function(th, idx){
        th.addEventListener('click', function(){
          var tbody = t.tBodies[0];
          var rows = Array.from(tbody.rows);
          var asc = !th.classList.contains('asc');
          t.querySelectorAll('th').forEach(function(x){ x.classList.remove('asc','desc'); });
          th.classList.add(asc ? 'asc' : 'desc');
          rows.sort(function(a,b){
            var av = a.cells[idx].innerText.trim();
            var bv = b.cells[idx].innerText.trim();
            var an = parseFloat(av.replace('%','').replace(/,/g,''));
            var bn = parseFloat(bv.replace('%','').replace(/,/g,''));
            if (!isNaN(an) && !isNaN(bn)) return asc ? an-bn : bn-an;
            return asc ? av.localeCompare(bv) : bv.localeCompare(av);
          });
          rows.forEach(function(r){ tbody.appendChild(r); });
        });
      });
    });
    """

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>JIRA Report — {esc(source)}</title>
<style>{css}</style>
</head>
<body>
<div class="container">
  <header class="report">
    <div>
      <div class="brand">CETIN</div>
      <h1>JIRA Report</h1>
    </div>
    <div class="meta">
      <div>Source: <b>{esc(source)}</b></div>
      <div>Generated: <b>{esc(gen_str)}</b></div>
    </div>
  </header>
  {body}
  <footer class="report">CETIN · JIRA dashboard · Generated by Copilot Cowork</footer>
</div>
<script>{sort_js}</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description="Render JIRA dashboard HTML.")
    ap.add_argument("--metrics", required=True, help="Path to metrics JSON")
    ap.add_argument("--output", required=True, help="Path to write HTML")
    args = ap.parse_args()

    metrics = json.loads(Path(args.metrics).read_text(encoding="utf-8"))
    html_out = render(metrics)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_out, encoding="utf-8")
    print(f"Wrote {out_path} ({len(html_out):,} bytes)")


if __name__ == "__main__":
    main()
