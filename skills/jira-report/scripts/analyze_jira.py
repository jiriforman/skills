#!/usr/bin/env python3
"""Analyze a JIRA CSV export and produce a metrics JSON file."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


DATE_FORMATS = [
    "%d/%b/%y %I:%M %p",
    "%d/%b/%y %H:%M",
    "%Y-%m-%dT%H:%M:%S.%f%z",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
]

DONE_STATUSES = {"done", "closed", "resolved", "complete", "completed"}
BLOCKED_HINTS = {"block", "blocked", "blocker"}


def parse_date(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    s = str(value).strip()
    if not s:
        return None
    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(s, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    try:
        return pd.to_datetime(s, utc=True, errors="coerce").to_pydatetime()
    except Exception:
        return None


def coalesce_multi_columns(df: pd.DataFrame) -> pd.DataFrame:
    """JIRA exports duplicate column names (Sprint, Components, Labels).
    Coalesce duplicates into a single column holding lists of unique values."""
    counts = Counter(df.columns)
    duplicated = [c for c, n in counts.items() if n > 1]
    if not duplicated:
        return df
    new_df = df.loc[:, ~df.columns.duplicated(keep=False)].copy()
    for col in duplicated:
        sub = df.loc[:, df.columns == col]
        combined = sub.apply(
            lambda row: sorted({str(v).strip() for v in row if pd.notna(v) and str(v).strip()}),
            axis=1,
        )
        new_df[col] = combined
    return new_df


def split_multi(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, float) and pd.isna(value):
        return []
    s = str(value).strip()
    if not s:
        return []
    return [p.strip() for p in re.split(r"[;,]", s) if p.strip()]


def is_done(status: str) -> bool:
    return status.strip().lower() in DONE_STATUSES


def is_blocked(row) -> bool:
    status = str(row.get("Status", "")).lower()
    priority = str(row.get("Priority", "")).lower()
    labels = row.get("_labels_list", []) or []
    if any(h in status for h in BLOCKED_HINTS):
        return True
    if priority == "blocker":
        return True
    if any("block" in l.lower() for l in labels):
        return True
    return False


def top_n(counter: Counter, n: int = 15, other_label: str = "Other"):
    items = counter.most_common()
    top = items[:n]
    rest = items[n:]
    result = [{"label": k, "count": int(v)} for k, v in top]
    if rest:
        result.append({"label": other_label, "count": int(sum(v for _, v in rest))})
    return result


def detect_current_sprints(sprint_series) -> list[str]:
    counts = Counter()
    for entry in sprint_series:
        for s in split_multi(entry):
            counts[s] += 1
    if not counts:
        return []
    # Heuristic: keep sprints whose name doesn't contain "closed"/"completed"
    candidates = [s for s in counts if not any(x in s.lower() for x in ("closed", "completed", "done"))]
    if not candidates:
        return []
    candidates.sort(key=lambda s: counts[s], reverse=True)
    return candidates[:3]


def analyze(csv_path: Path) -> dict:
    df_raw = pd.read_csv(csv_path, dtype=str, keep_default_na=False, na_values=[""])
    df = coalesce_multi_columns(df_raw)

    cols = {c.lower(): c for c in df.columns}

    def col(name: str) -> str | None:
        return cols.get(name.lower())

    issue_key_col = col("Issue key") or col("Key")
    status_col = col("Status")
    type_col = col("Issue Type") or col("Type")
    priority_col = col("Priority")
    assignee_col = col("Assignee")
    created_col = col("Created")
    updated_col = col("Updated")
    sprint_col = col("Sprint")
    points_col = col("Custom field (Story Points)") or col("Story Points")
    project_col = col("Project key") or col("Project Key") or col("Project")
    project_name_col = col("Project name") or col("Project Name")
    epic_col = col("Custom field (Epic Link)") or col("Epic Link") or col("Parent")
    components_col = col("Components") or col("Component/s") or col("Component")
    labels_col = col("Labels")
    summary_col = col("Summary")

    now = datetime.now(timezone.utc)

    # Pre-compute helper columns
    df["_created"] = df[created_col].map(parse_date) if created_col else None
    df["_updated"] = df[updated_col].map(parse_date) if updated_col else None
    df["_labels_list"] = df[labels_col].map(split_multi) if labels_col else [[] for _ in range(len(df))]
    df["_sprints_list"] = df[sprint_col].map(split_multi) if sprint_col else [[] for _ in range(len(df))]
    df["_done"] = df[status_col].fillna("").map(is_done) if status_col else False
    df["_blocked"] = df.apply(is_blocked, axis=1)
    if points_col:
        df["_points"] = pd.to_numeric(df[points_col], errors="coerce").fillna(0.0)
    else:
        df["_points"] = 0.0

    total = len(df)
    missing_sections = []

    metrics: dict = {
        "generated_at": now.isoformat(),
        "source_file": csv_path.name,
        "total_issues": total,
        "missing_sections": missing_sections,
    }

    if total == 0:
        metrics["empty"] = True
        return metrics

    # KPIs
    done_count = int(df["_done"].sum())
    open_count = total - done_count
    in_progress = 0
    if status_col:
        in_progress = int(df[status_col].fillna("").str.lower().str.contains("progress").sum())
    blockers = int(df["_blocked"].sum())
    metrics["kpis"] = {
        "total": total,
        "open": open_count,
        "in_progress": in_progress,
        "done": done_count,
        "done_pct": round(100 * done_count / total, 1) if total else 0,
        "blockers": blockers,
    }

    # A. Status overview
    if status_col:
        metrics["by_status"] = top_n(Counter(df[status_col].fillna("Unknown")), n=10)
    else:
        missing_sections.append("Status")
    if type_col:
        metrics["by_type"] = top_n(Counter(df[type_col].fillna("Unknown")), n=10)
    else:
        missing_sections.append("Issue Type")
    if priority_col:
        metrics["by_priority"] = top_n(Counter(df[priority_col].fillna("Unknown")), n=10)
    else:
        missing_sections.append("Priority")
    if assignee_col:
        metrics["by_assignee"] = top_n(
            Counter(df[assignee_col].fillna("Unassigned").replace("", "Unassigned")), n=15
        )
    else:
        missing_sections.append("Assignee")

    # B. Sprint / velocity
    if sprint_col:
        current_sprints = detect_current_sprints(df[sprint_col])
        per_sprint_total = Counter()
        per_sprint_done = Counter()
        per_sprint_points_done = defaultdict(float)
        per_sprint_points_total = defaultdict(float)
        for _, row in df.iterrows():
            for s in row["_sprints_list"]:
                per_sprint_total[s] += 1
                per_sprint_points_total[s] += float(row["_points"] or 0)
                if row["_done"]:
                    per_sprint_done[s] += 1
                    per_sprint_points_done[s] += float(row["_points"] or 0)

        sprint_rows = []
        for s in sorted(per_sprint_total.keys()):
            total_s = per_sprint_total[s]
            done_s = per_sprint_done[s]
            sprint_rows.append({
                "sprint": s,
                "issues": total_s,
                "done": done_s,
                "done_pct": round(100 * done_s / total_s, 1) if total_s else 0,
                "points_total": round(per_sprint_points_total[s], 1),
                "points_done": round(per_sprint_points_done[s], 1),
                "is_current": s in current_sprints,
            })
        # Velocity = last 6 sprints by name (best effort, alphabetical)
        velocity = sprint_rows[-6:]
        metrics["sprints"] = sprint_rows
        metrics["velocity_last6"] = velocity
        metrics["current_sprints"] = current_sprints
    else:
        missing_sections.append("Sprint")

    # C. Aging & blockers
    if created_col:
        ages = []
        buckets = {"0-14d": 0, "15-30d": 0, "31-60d": 0, "61-90d": 0, ">90d": 0}
        oldest_open = []
        for _, row in df.iterrows():
            created = row["_created"]
            if not created or row["_done"]:
                continue
            age_days = (now - created).days
            ages.append(age_days)
            if age_days <= 14:
                buckets["0-14d"] += 1
            elif age_days <= 30:
                buckets["15-30d"] += 1
            elif age_days <= 60:
                buckets["31-60d"] += 1
            elif age_days <= 90:
                buckets["61-90d"] += 1
            else:
                buckets[">90d"] += 1
            oldest_open.append({
                "key": row.get(issue_key_col, "") if issue_key_col else "",
                "summary": (row.get(summary_col, "") if summary_col else "")[:120],
                "status": row.get(status_col, "") if status_col else "",
                "assignee": row.get(assignee_col, "") if assignee_col else "",
                "age_days": age_days,
            })
        oldest_open.sort(key=lambda r: r["age_days"], reverse=True)
        metrics["aging_buckets"] = [{"label": k, "count": v} for k, v in buckets.items()]
        metrics["oldest_open"] = oldest_open[:10]

        # Stale (no update in 14+ days, still open)
        if updated_col:
            stale = 0
            for _, row in df.iterrows():
                if row["_done"]:
                    continue
                u = row["_updated"]
                if u and (now - u).days >= 14:
                    stale += 1
            metrics["stale_count"] = stale
    else:
        missing_sections.append("Created")

    # Blocker list
    blocker_rows = []
    for _, row in df.iterrows():
        if not row["_blocked"]:
            continue
        blocker_rows.append({
            "key": row.get(issue_key_col, "") if issue_key_col else "",
            "summary": (row.get(summary_col, "") if summary_col else "")[:120],
            "status": row.get(status_col, "") if status_col else "",
            "priority": row.get(priority_col, "") if priority_col else "",
            "assignee": row.get(assignee_col, "") if assignee_col else "",
        })
    metrics["blocker_list"] = blocker_rows[:20]

    # D. Project / epic breakdown
    if project_col:
        proj_counts = Counter(df[project_col].fillna("Unknown"))
        proj_done = Counter()
        for _, row in df.iterrows():
            if row["_done"]:
                proj_done[row.get(project_col, "Unknown") or "Unknown"] += 1
        rows = []
        for p, n in proj_counts.most_common():
            rows.append({
                "project": p,
                "issues": int(n),
                "done": int(proj_done.get(p, 0)),
                "done_pct": round(100 * proj_done.get(p, 0) / n, 1) if n else 0,
            })
        metrics["by_project"] = rows
    else:
        missing_sections.append("Project")

    if epic_col:
        epic_counts = Counter()
        epic_done = Counter()
        for _, row in df.iterrows():
            e = (row.get(epic_col) or "").strip() or "(no epic)"
            epic_counts[e] += 1
            if row["_done"]:
                epic_done[e] += 1
        rows = []
        for e, n in epic_counts.most_common(20):
            rows.append({
                "epic": e,
                "issues": int(n),
                "done": int(epic_done.get(e, 0)),
                "done_pct": round(100 * epic_done.get(e, 0) / n, 1) if n else 0,
            })
        metrics["by_epic"] = rows

    if components_col:
        comp_counter = Counter()
        for _, row in df.iterrows():
            for c in split_multi(row.get(components_col)):
                comp_counter[c] += 1
        metrics["by_component"] = [
            {"label": k, "count": int(v)} for k, v in comp_counter.most_common(10)
        ]

    return metrics


def main():
    ap = argparse.ArgumentParser(description="Analyze a JIRA CSV export.")
    ap.add_argument("--input", required=True, help="Path to JIRA CSV file")
    ap.add_argument("--output", required=True, help="Path to write metrics JSON")
    args = ap.parse_args()

    csv_path = Path(args.input)
    if not csv_path.exists():
        print(f"ERROR: input file not found: {csv_path}", file=sys.stderr)
        sys.exit(2)

    metrics = analyze(csv_path)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False, default=str))
    print(f"Wrote {out_path} ({metrics['total_issues']} issues)")


if __name__ == "__main__":
    main()
