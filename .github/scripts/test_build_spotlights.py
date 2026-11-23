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
            self.assertEqual(build(root, catalog), [first, second])
            for overrides in ({"path": "/b/"}, {"guides": ["missing"]}, {"schedule": {"startDate": "tomorrow"}}):
                with self.subTest(overrides=overrides):
                    (root / "b.json").write_text(json.dumps([second | overrides]))
                    with self.assertRaises(ValueError):
                        build(root, catalog)
            (root / "b.json").unlink()
            self.assertEqual(build(root, catalog), [first])
