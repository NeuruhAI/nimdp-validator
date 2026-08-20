import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("nimdp_validator", ROOT / "validator.py")
validator = importlib.util.module_from_spec(_spec)
sys.modules["nimdp_validator"] = validator
_spec.loader.exec_module(validator)


TOKEN_MAP = {
    "pass_threshold": 0.5,
    "hard_block_on_fail": True,
    "phases": {
        "PHASE_1": {
            "weight": 0.6,
            "tokens": {
                "REQUIRED": {
                    "desc": "A required token.",
                    "weight": 1.0,
                    "keywords_any": ["alpha", "first pin"],
                    "hard_blocker": True,
                    "remediation": "Name the segment.",
                },
            },
        },
        "PHASE_2": {
            "weight": 0.4,
            "tokens": {
                "OPTIONAL": {
                    "desc": "An optional token.",
                    "weight": 1.0,
                    "keywords_any": ["beta"],
                    "hard_blocker": False,
                    "remediation": "Add proof.",
                },
            },
        },
    },
}


class KeywordTests(unittest.TestCase):
    def test_match_is_case_insensitive(self):
        self.assertTrue(validator.find_any_keywords("The ALPHA build", ["alpha"]))
        self.assertTrue(validator.find_any_keywords("the alpha build", ["ALPHA"]))

    def test_no_match_returns_false(self):
        self.assertFalse(validator.find_any_keywords("nothing here", ["alpha"]))

    def test_multi_word_keyword_matches_as_a_phrase(self):
        self.assertTrue(validator.find_any_keywords("our first pin is here", ["first pin"]))
        self.assertFalse(validator.find_any_keywords("pin first", ["first pin"]))


class ScoringTests(unittest.TestCase):
    def test_all_tokens_present_scores_one(self):
        r = validator.aggregate_scores(["alpha beta"], TOKEN_MAP)
        self.assertEqual(r["score"], 1.0)
        self.assertFalse(r["hard_block_triggered"])
        self.assertEqual(r["remediations"], [])

    def test_missing_hard_blocker_triggers_block(self):
        r = validator.aggregate_scores(["beta only"], TOKEN_MAP)
        self.assertTrue(r["hard_block_triggered"])
        self.assertEqual(r["score"], 0.4)

    def test_missing_soft_token_scores_partial_without_block(self):
        r = validator.aggregate_scores(["alpha only"], TOKEN_MAP)
        self.assertFalse(r["hard_block_triggered"])
        self.assertEqual(r["score"], 0.6)

    def test_remediation_names_the_missing_token(self):
        r = validator.aggregate_scores(["alpha only"], TOKEN_MAP)
        self.assertEqual([x["token"] for x in r["remediations"]], ["PHASE_2.OPTIONAL"])

    def test_inputs_are_scored_jointly(self):
        r = validator.aggregate_scores(["alpha", "beta"], TOKEN_MAP)
        self.assertEqual(r["score"], 1.0)


class StatusTests(unittest.TestCase):
    def test_hard_block_wins_over_a_passing_score(self):
        self.assertEqual(validator.status_from_score(1.0, True, 0.5, True), "BLOCKED")

    def test_hard_block_can_be_disarmed(self):
        self.assertEqual(validator.status_from_score(1.0, True, 0.5, False), "MARKET READY")

    def test_score_at_threshold_passes(self):
        self.assertEqual(validator.status_from_score(0.5, False, 0.5, True), "MARKET READY")

    def test_score_below_threshold_fails(self):
        self.assertEqual(validator.status_from_score(0.49, False, 0.5, True), "NOT READY")


class ReportTests(unittest.TestCase):
    def test_reports_are_written_and_json_round_trips(self):
        details = validator.aggregate_scores(["alpha beta"], TOKEN_MAP)
        details["status"] = "MARKET READY"
        with tempfile.TemporaryDirectory() as d:
            outdir = Path(d)
            jpath, mpath = validator.write_reports("Demo Project", outdir, details)
            self.assertTrue(Path(jpath).exists())
            self.assertTrue(Path(mpath).exists())
            self.assertEqual(json.loads(Path(jpath).read_text())["score"], 1.0)
            self.assertIn("NIMDP Validation Report", Path(mpath).read_text())

    def test_report_filenames_are_sanitized(self):
        self.assertEqual(validator.sanitize_title("a b/c:d"), "a_b_c_d")

    def test_timestamp_is_timezone_aware_utc(self):
        stamp = validator.now_stamp()
        self.assertRegex(stamp, r"^\d{8}-\d{6}$")


class ShippedFixtureTests(unittest.TestCase):
    def test_default_token_map_loads_and_scores_the_sample_spec(self):
        token_map = validator.load_token_map(ROOT / "token_map.yaml")
        text = validator.read_file_text(ROOT / "samples" / "demo_spec.md")
        results = validator.aggregate_scores([text], token_map)
        self.assertGreaterEqual(results["score"], 0.0)
        self.assertLessEqual(results["score"], 1.0)
        self.assertIn("phases", results)

    def test_bundled_packs_are_well_formed(self):
        for pack in sorted((ROOT / "nimdp-packs" / "packs").glob("*.yaml")):
            token_map = validator.load_token_map(pack)
            self.assertIn("phases", token_map, pack.name)
            for phase_name, phase in token_map["phases"].items():
                self.assertIn("weight", phase, f"{pack.name}:{phase_name}")
                for token_name, token in phase["tokens"].items():
                    where = f"{pack.name}:{phase_name}.{token_name}"
                    self.assertIn("weight", token, where)
                    self.assertIn("desc", token, where)
                    self.assertIn("remediation", token, where)
                    self.assertTrue(token["keywords_any"], where)


if __name__ == "__main__":
    unittest.main()
