"""Unit tests for skills/journey-mapper/build.py. Run with `make test`."""

import copy
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "journey-mapper"
sys.path.insert(0, str(SKILL_DIR))

import build  # noqa: E402

TEMPLATE = build.TEMPLATE_PATH.read_text(encoding="utf-8")


def sample_data():
    """The sample data shipped in TEMPLATE.html, which must always be valid."""
    return json.loads(build.DATA_BLOCK.search(TEMPLATE).group(2))


def embedded_data(page):
    return json.loads(build.DATA_BLOCK.search(page).group(2))


def first_moment(data):
    return data["journeys"][0]["stages"][0]["moments"][0]


def run_cli(*args):
    """Run build.main quietly; return (exit code, stderr text)."""
    err = StringIO()
    with redirect_stdout(StringIO()), redirect_stderr(err):
        code = build.main(list(args))
    return code, err.getvalue()


class ValidateTests(unittest.TestCase):
    def assertError(self, data, fragment):
        errors = build.validate(data).errors
        self.assertTrue(any(fragment in e for e in errors), f"no error containing {fragment!r} in {errors}")

    def test_template_sample_data_is_valid(self):
        self.assertEqual(build.validate(sample_data()).errors, [])

    def test_rejects_non_object_root(self):
        self.assertError([], "must be a JSON object")

    def test_rejects_unknown_actor_and_category(self):
        data = sample_data()
        data["journeys"][0]["actor"] = "ghost"
        data["journeys"][0]["category"] = "nowhere"
        self.assertError(data, "actor 'ghost'")
        self.assertError(data, "category 'nowhere'")

    def test_rejects_duplicate_moment_ids_across_journeys(self):
        data = sample_data()
        duplicate = first_moment(data)["id"]
        data["journeys"][1]["stages"][0]["moments"][0]["id"] = duplicate
        self.assertError(data, f"duplicate id '{duplicate}'")

    def test_rejects_non_kebab_ids(self):
        data = sample_data()
        data["actors"][0]["id"] = "New User"
        self.assertError(data, "must be kebab-case")

    def test_rejects_bad_feelings(self):
        for bad in (0, 6, 2.5, "3", True):
            data = sample_data()
            first_moment(data)["feeling"] = bad
            self.assertError(data, "'feeling' must be an integer")

    def test_allows_omitted_feeling(self):
        data = sample_data()
        first_moment(data).pop("feeling", None)
        self.assertEqual(build.validate(data).errors, [])

    def test_rejects_empty_stages(self):
        data = sample_data()
        data["journeys"][0]["stages"] = []
        self.assertError(data, "'stages' must be a non-empty list")

    def test_warns_on_missing_assumption_prefix(self):
        data = sample_data()
        first_moment(data)["pain"] = "Too many fields."
        report = build.validate(data)
        self.assertEqual(report.errors, [])
        self.assertTrue(any("'pain' is inferred" in w for w in report.warnings))

    def test_warns_on_unused_actor(self):
        data = sample_data()
        data["actors"].append({"id": "admin", "name": "Admin"})
        self.assertTrue(any("actor 'admin'" in w for w in build.validate(data).warnings))


class BuildHtmlTests(unittest.TestCase):
    def test_sets_title_and_heading_escaped(self):
        page = build.build_html(TEMPLATE, sample_data(), "Fish & <Chips>")
        self.assertIn("<title>Fish &amp; &lt;Chips&gt; — Journey Maps</title>", page)
        self.assertIn("<h1>Fish &amp; &lt;Chips&gt;</h1>", page)

    def test_keeps_template_title_without_product(self):
        page = build.build_html(TEMPLATE, sample_data(), None)
        self.assertIn(build.TITLE_MARKER, page)

    def test_round_trips_data_and_neutralises_script_end_tags(self):
        data = sample_data()
        first_moment(data)["backstage"] = 'Renders </script><script>alert(1)</script> and <!-- x'
        page = build.build_html(TEMPLATE, data, "Test")
        block = build.DATA_BLOCK.search(page).group(2)
        self.assertNotIn("<", block)
        self.assertEqual(embedded_data(page), data)

    def test_handles_backslashes_in_data(self):
        data = sample_data()
        first_moment(data)["support"] = r"C:\new\table \1 \g<0>"
        self.assertEqual(embedded_data(build.build_html(TEMPLATE, data, "Test")), data)

    def test_changes_nothing_outside_the_markers(self):
        page = build.build_html(TEMPLATE, sample_data(), "Test")
        strip = lambda html: build.DATA_BLOCK.sub("", html)  # noqa: E731
        expected = strip(TEMPLATE).replace(build.TITLE_MARKER, "<title>Test — Journey Maps</title>") \
                                  .replace(build.HEADING_MARKER, "<h1>Test</h1>")
        self.assertEqual(strip(page), expected)

    def test_refuses_a_template_without_markers(self):
        with self.assertRaises(ValueError):
            build.build_html("<html></html>", sample_data(), "Test")


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.data_path = self.tmp / "journeys.json"
        self.out_path = self.tmp / "out" / "journey-map.html"

    def write_data(self, data):
        self.data_path.write_text(json.dumps(data), encoding="utf-8")

    def test_writes_the_map(self):
        self.write_data(sample_data())
        code, _ = run_cli(str(self.data_path), str(self.out_path), "--product", "Test")
        self.assertEqual(code, 0)
        self.assertEqual(embedded_data(self.out_path.read_text(encoding="utf-8")), sample_data())

    def test_writes_nothing_on_errors(self):
        data = copy.deepcopy(sample_data())
        data["journeys"][0]["actor"] = "ghost"
        self.write_data(data)
        code, err = run_cli(str(self.data_path), str(self.out_path))
        self.assertEqual(code, 1)
        self.assertIn("nothing written", err)
        self.assertFalse(self.out_path.exists())

    def test_check_only_writes_nothing(self):
        self.write_data(sample_data())
        code, _ = run_cli(str(self.data_path), "--check")
        self.assertEqual(code, 0)
        self.assertFalse(self.out_path.exists())

    def test_reports_invalid_json(self):
        self.data_path.write_text("{not json", encoding="utf-8")
        code, err = run_cli(str(self.data_path), "--check")
        self.assertEqual(code, 1)
        self.assertIn("isn't valid JSON", err)

    def test_reports_missing_file(self):
        code, _ = run_cli(str(self.tmp / "missing.json"), "--check")
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
