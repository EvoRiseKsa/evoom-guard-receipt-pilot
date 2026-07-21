"""Consistency checks for the controlled moved-main rejection record."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
OBSERVATION = ROOT / "evidence" / "negative-main-move" / "OBSERVATION.json"
SOURCE = "a3fc9f14a8c683fa5466d0d4124826f3151cb4d0"
TARGET = "1e7b0213ada2f03f1b4e3028a37398b45ad6eb02"


def no_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


class NegativeMainMoveEvidenceTests(unittest.TestCase):
    def load(self) -> dict[str, object]:
        return json.loads(
            OBSERVATION.read_text(encoding="utf-8"),
            object_pairs_hook=no_duplicate_keys,
        )

    def test_observation_binds_the_intended_direct_successor(self) -> None:
        record = self.load()
        self.assertEqual(record["schema_version"], "evoguard-receipt-negative-main-move-v1")
        self.assertEqual(record["claim_scope"], "controlled-fail-closed-non-admitting-observation")
        self.assertEqual(record["source_commit_sha"], SOURCE)
        self.assertEqual(record["target_commit_sha"], TARGET)
        self.assertEqual(record["target_parent_sha"], SOURCE)
        self.assertEqual(record["marker_pr"]["number"], 16)

    def test_b_rejected_after_gate_without_producing_a_receipt(self) -> None:
        record = self.load()
        self.assertEqual(record["a_reverify"]["run_id"], 29675987307)
        self.assertEqual(record["a_reverify"]["conclusion"], "success")
        self.assertEqual(record["a_reverify"]["head_sha"], SOURCE)

        producer = record["b_producer"]
        self.assertEqual(producer["run_id"], 29676005850)
        self.assertEqual(producer["head_sha"], SOURCE)
        self.assertEqual(producer["negative_main_move_gate_conclusion"], "success")
        self.assertEqual(producer["preflight_conclusion"], "failure")
        self.assertEqual(producer["receipt_conclusion"], "skipped")
        self.assertEqual(producer["artifact_count"], 0)
        self.assertEqual(
            producer["failure_text"],
            "protected main changed after reverify; refuse receipt production",
        )

    def test_c_rejected_failed_b_before_artifact_download(self) -> None:
        consumer = self.load()["c_fresh_reverification"]
        self.assertEqual(consumer["run_id"], 29867423549)
        self.assertEqual(consumer["head_sha"], TARGET)
        self.assertEqual(consumer["preflight_conclusion"], "failure")
        self.assertEqual(consumer["download_conclusion"], "skipped")
        self.assertEqual(consumer["artifact_count"], 0)
        self.assertEqual(
            consumer["failure_text"],
            "trigger is not the configured successful producer-receipt workflow_run",
        )

    def test_temporary_controls_were_recorded_as_removed(self) -> None:
        record = self.load()
        self.assertEqual(record["main_ci"]["head_sha"], TARGET)
        self.assertEqual(record["main_ci"]["conclusion"], "success")
        self.assertEqual(
            record["temporary_variables_removed"],
            [
                "EVOGUARD_RECEIPT_PILOT_CHAIN_ENABLED",
                "EVOGUARD_RECEIPT_PILOT_NEGATIVE_MAIN_MOVE_CONTROL",
            ],
        )


if __name__ == "__main__":
    unittest.main()
