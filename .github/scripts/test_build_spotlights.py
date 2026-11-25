import json
from pathlib import Path
import tempfile
import unittest

from build_spotlights import build


class TeamFilesTest(unittest.TestCase):
    def test_aggregation_and_conflicts(self):
        catalog = {"guide": {"type": "guide", "path": "guide/"}}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = {"path": "/a", "additionalPaths": ["/b"], "heading": "First", "guides": ["guide"]}
            second = {"path": "/c", "heading": "Second", "guides": ["guide"]}
            (root / "a.json").write_text(json.dumps([first]))
            (root / "b.json").write_text(json.dumps([second]))
            self.assertEqual(build(root, catalog), {"schemaVersion": 1, "spotlights": [first, second]})
            for overrides in ({"path": "/b/"}, {"path": "/a/./"}, {"path": "/a/../b"}, {"guides": ["missing"]}, {"schedule": {"startDate": "tomorrow"}}):
                with self.subTest(overrides=overrides):
                    (root / "b.json").write_text(json.dumps([second | overrides]))
                    with self.assertRaises(ValueError):
                        build(root, catalog)
            (root / "b.json").unlink()
            self.assertEqual(build(root, catalog)["spotlights"], [first])

    def test_nested_members_and_wire_fixture(self):
        catalog = {"course": {"type": "path", "path": "course/", "milestones": ["step"],
                              "tracks": [{"guides": ["track-step"]}]}}
        for guide in ("step", "track-step", "course/chapter", "solo"):
            catalog[guide] = {"type": "guide", "path": guide + "/"}
        fixture = json.loads((Path(__file__).parent / "testdata/spotlights-v1.json").read_text())
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            team = root / "team.json"
            team.write_text(json.dumps(fixture["spotlights"]))
            self.assertEqual(build(root, catalog), fixture)
            for member in ("step", "track-step", "course/chapter"):
                team.write_text(json.dumps([dict(fixture["spotlights"][0], guides=[member])]))
                with self.assertRaisesRegex(ValueError, "standalone"):
                    build(root, catalog)

    def test_expired_claim_warns(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "team.json").write_text(json.dumps([{
                "path": "/", "heading": "Past", "guides": ["solo"],
                "schedule": {"endDate": "2000-01-01"}
            }]))
            with self.assertWarnsRegex(UserWarning, "expired spotlight"):
                build(root, {"solo": {"type": "guide", "path": "solo/"}})
