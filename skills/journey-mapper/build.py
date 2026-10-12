#!/usr/bin/env python3
"""Validate journey-map JSON and build the HTML map from TEMPLATE.html.

Usage:
    python3 build.py <data.json> <output.html> [--product "Product name"]
    python3 build.py <data.json> --check

Exit codes: 0 = written (or valid, with --check), 1 = the JSON has errors,
2 = bad arguments or a template that no longer has the expected markers.
Standard library only, so it runs anywhere Python 3.8+ does.
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

TEMPLATE_PATH = Path(__file__).resolve().parent / "TEMPLATE.html"

TITLE_MARKER = "<title>Journey Maps</title>"
HEADING_MARKER = "<h1>Journey Maps</h1>"
DATA_BLOCK = re.compile(
    r'(<script type="application/json" id="journeys-data">)(.*?)(</script>)',
    re.DOTALL,
)

KEBAB_CASE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TEXT_FIELDS = ("doing", "thinking", "pain", "opportunity", "evidence",
               "frontstage", "backstage", "support")
ASSUMPTION_FIELDS = ("thinking", "pain", "opportunity")


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, message):
        self.errors.append(f"{where}: {message}")

    def warn(self, where, message):
        self.warnings.append(f"{where}: {message}")


def check_list(report, parent, key, where):
    value = parent.get(key)
    if not isinstance(value, list) or not value:
        report.error(where, f"'{key}' must be a non-empty list")
        return []
    return value


def check_id(report, item, where, seen):
    item_id = item.get("id")
    if not isinstance(item_id, str) or not KEBAB_CASE.match(item_id):
        report.error(where, f"id {item_id!r} must be kebab-case, e.g. 'sign-up'")
        return None
    if item_id in seen:
        report.error(where, f"duplicate id '{item_id}'")
    seen.add(item_id)
    return item_id


def check_text(report, item, key, where, required=False):
    value = item.get(key)
    if value is None:
        if required:
            report.error(where, f"'{key}' is required")
        return
    if not isinstance(value, str):
        report.error(where, f"'{key}' must be a string")
    elif required and not value.strip():
        report.error(where, f"'{key}' must not be empty")


def check_moment(report, moment, where):
    check_text(report, moment, "title", where, required=True)
    for field in TEXT_FIELDS:
        check_text(report, moment, field, where)

    feeling = moment.get("feeling")
    # bool is a subclass of int in Python, so rule it out explicitly.
    if feeling is not None and (isinstance(feeling, bool) or not isinstance(feeling, int)
                                or not 1 <= feeling <= 5):
        report.error(where, f"'feeling' must be an integer 1–5 or omitted, got {feeling!r}")

    for field in ASSUMPTION_FIELDS:
        value = moment.get(field)
        if isinstance(value, str) and value.strip() and not value.startswith("[Assumption]"):
            report.warn(where, f"'{field}' is inferred and should start with '[Assumption]'")
    evidence = moment.get("evidence")
    if isinstance(evidence, str) and evidence.strip():
        report.warn(where, "'evidence' should be left blank for the human to fill")


def validate(data):
    report = Report()
    if not isinstance(data, dict):
        report.error("root", "must be a JSON object with actors, categories and journeys")
        return report

    actor_ids, category_ids = set(), set()
    for i, actor in enumerate(check_list(report, data, "actors", "root")):
        where = f"actors[{i}]"
        if not isinstance(actor, dict):
            report.error(where, "must be an object")
            continue
        check_id(report, actor, where, actor_ids)
        check_text(report, actor, "name", where, required=True)

    for i, category in enumerate(check_list(report, data, "categories", "root")):
        where = f"categories[{i}]"
        if not isinstance(category, dict):
            report.error(where, "must be an object")
            continue
        check_id(report, category, where, category_ids)
        check_text(report, category, "title", where, required=True)

    journeys = check_list(report, data, "journeys", "root")
    journey_ids, moment_ids = set(), set()
    used_actors, used_categories = set(), set()
    for i, journey in enumerate(journeys):
        where = f"journeys[{i}]"
        if not isinstance(journey, dict):
            report.error(where, "must be an object")
            continue
        journey_id = check_id(report, journey, where, journey_ids)
        if journey_id:
            where = f"journey '{journey_id}'"
        check_text(report, journey, "title", where, required=True)
        check_text(report, journey, "scenario", where)
        check_text(report, journey, "goal", where)

        actor = journey.get("actor")
        if actor not in actor_ids:
            report.error(where, f"actor {actor!r} doesn't match any actors[].id")
        used_actors.add(actor)
        category = journey.get("category")
        if category not in category_ids:
            report.error(where, f"category {category!r} doesn't match any categories[].id")
        used_categories.add(category)

        stages = check_list(report, journey, "stages", where)
        if stages and not 2 <= len(stages) <= 5:
            report.warn(where, f"has {len(stages)} stages; aim for 2–5")
        for s, stage in enumerate(stages):
            stage_where = f"{where} stage {s + 1}"
            if not isinstance(stage, dict):
                report.error(stage_where, "must be an object")
                continue
            check_text(report, stage, "title", stage_where, required=True)
            moments = check_list(report, stage, "moments", stage_where)
            if moments and not 2 <= len(moments) <= 4:
                report.warn(stage_where, f"has {len(moments)} moments; aim for 2–4")
            for m, moment in enumerate(moments):
                moment_where = f"{stage_where} moment {m + 1}"
                if not isinstance(moment, dict):
                    report.error(moment_where, "must be an object")
                    continue
                # Moment ids key saved annotations, so they must be unique file-wide.
                moment_id = check_id(report, moment, moment_where, moment_ids)
                if moment_id:
                    moment_where = f"moment '{moment_id}'"
                check_moment(report, moment, moment_where)

    if journeys and not 4 <= len(journeys) <= 12:
        report.warn("root", f"{len(journeys)} journeys; aim for 4–12")
    for actor_id in sorted(actor_ids - used_actors):
        report.warn(f"actor '{actor_id}'", "isn't the actor of any journey")
    for category_id in sorted(category_ids - used_categories):
        report.warn(f"category '{category_id}'", "has no journeys and won't appear in the rail")
    return report


def embed_json(data):
    # Escaping every "<" keeps text like "</script>" or "<!--" in the data from
    # ending the <script> block early. < is still valid JSON for "<".
    return "\n" + json.dumps(data, indent=2, ensure_ascii=False).replace("<", "\\u003c") + "\n"


def build_html(template, data, product):
    for marker in (TITLE_MARKER, HEADING_MARKER):
        if marker not in template:
            raise ValueError(f"TEMPLATE.html no longer contains {marker}")
    if not DATA_BLOCK.search(template):
        raise ValueError("TEMPLATE.html no longer contains the journeys-data script block")

    page = template
    if product:
        name = html.escape(product)
        page = page.replace(TITLE_MARKER, f"<title>{name} — Journey Maps</title>", 1)
        page = page.replace(HEADING_MARKER, f"<h1>{name}</h1>", 1)
    # A function replacement, so backslashes in the JSON aren't read as regex escapes.
    return DATA_BLOCK.sub(lambda m: m.group(1) + embed_json(data) + m.group(3), page, count=1)


def count_moments(data):
    return sum(len(stage["moments"]) for journey in data["journeys"] for stage in journey["stages"])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate journey-map JSON and build the HTML map.")
    parser.add_argument("data", help="path to the journeys JSON file")
    parser.add_argument("output", nargs="?", help="path to write the HTML map to")
    parser.add_argument("--product", help="product name for the page title and rail heading")
    parser.add_argument("--check", action="store_true", help="validate only; write nothing")
    args = parser.parse_args(argv)
    if not args.check and not args.output:
        parser.error("give an output path, or --check to validate only")

    try:
        data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: {args.data} not found", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: {args.data} isn't valid JSON: {e}", file=sys.stderr)
        return 1

    report = validate(data)
    for warning in report.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    if report.errors:
        for error in report.errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"{len(report.errors)} error(s); nothing written. Fix the JSON and run again.",
              file=sys.stderr)
        return 1

    summary = (f"{len(data['journeys'])} journeys · {count_moments(data)} moments · "
               f"{len(data['categories'])} categories · {len(report.warnings)} warning(s)")
    if args.check:
        print(f"Valid: {summary}")
        return 0

    try:
        page = build_html(TEMPLATE_PATH.read_text(encoding="utf-8"), data, args.product)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    print(f"Wrote {output}: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
