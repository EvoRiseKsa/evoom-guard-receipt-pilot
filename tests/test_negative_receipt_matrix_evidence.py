"""Consistency checks for the frozen receipt-negative matrix."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "evidence" / "negative-receipt-matrix"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class NegativeReceiptMatrixEvidenceTests(unittest.TestCase):
    def test_manifest_covers_every_frozen_file(self) -> None:
        lines = (EVIDENCE / "MANIFEST.sha256").read_text(encoding="ascii").splitlines()
        manifest = {}
        for line in lines:
            digest, name = line.split("  ", 1)
            self.assertRegex(digest, r"^[0-9a-f]{64}$")
            self.assertNotIn(name, manifest)
            manifest[name] = digest
        actual = {
            path.relative_to(EVIDENCE).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in EVIDENCE.rglob("*")
            if path.is_file() and path.name != "MANIFEST.sha256"
        }
        self.assertEqual(manifest, actual)

    def test_aggregate_record_is_nonadmitting_and_complete(self) -> None:
        record = load_json(EVIDENCE / "OBSERVATION.json")
        self.assertEqual(record["schema_version"], "evoguard-receipt-negative-matrix-v1")
        self.assertFalse(record["admitting"])
        self.assertFalse(record["independent_review"])
        self.assertEqual(record["head_sha"], "3276acc17ac009115530e46d73ee743c53da536d")
        self.assertEqual(record["runs"]["a"]["conclusion"], "success")
        self.assertEqual(record["runs"]["b"]["conclusion"], "success")
        self.assertEqual(record["runs"]["c"]["conclusions"], {"2": "success", "3": "success", "4": "success"})
        self.assertEqual(
            set(record["temporary_variables_deleted"]),
            {
                "EVOGUARD_RECEIPT_PILOT_CHAIN_ENABLED",
                "EVOGUARD_RECEIPT_PILOT_NEGATIVE_RECEIPT_CONTROL",
            },
        )

    def test_upstream_exact_bytes_are_consistent(self) -> None:
        a = EVIDENCE / "a" / "evoguard-release-source-evidence-v1-1"
        b = EVIDENCE / "b" / "evoguard-release-source-producer-receipt-v1-1"
        for name in ("source.json", "context.json", "verdict.json", "handoff.json"):
            self.assertEqual((a / name).read_bytes(), (b / name).read_bytes(), name)
        receipt = (b / "producer-receipt.json").read_bytes()
        self.assertEqual(
            hashlib.sha256(receipt).hexdigest(),
            "7717c53a6a8874955aaf4cbc556fe69042be562e48dc236d9c04043b6b961061",
        )

    def test_each_control_records_the_intended_expected_rejection(self) -> None:
        expected = {
            "altered-artifact": ("altered-artifact-v1", "github-artifact-attestation-subject-digest"),
            "wrong-workflow": ("wrong-workflow-v1", "producer-workflow-identity-preflight"),
            "wrong-run-attempt": ("wrong-run-attempt-v1", "producer-run-attempt-binding"),
        }
        for directory, (control, layer) in expected.items():
            record = load_json(EVIDENCE / directory / "negative-observation.json")
            self.assertEqual(record["schema_version"], "evoguard-receipt-negative-control-v1")
            self.assertEqual(record["control"], control)
            self.assertEqual(record["rejection_layer"], layer)
            self.assertEqual(record["result"], "EXPECTED_REJECTION")
            self.assertFalse(record["admitting"])

    def test_altered_bytes_had_a_same_run_positive_provider_baseline(self) -> None:
        control = load_json(EVIDENCE / "altered-artifact" / "negative-observation.json")
        baseline = load_json(EVIDENCE / "altered-artifact" / "unaltered-provider-baseline.json")
        self.assertEqual(len(baseline), 1)
        subjects = baseline[0]["verificationResult"]["statement"]["subject"]
        self.assertEqual(len(subjects), 1)
        self.assertEqual(subjects[0]["digest"]["sha256"], control["before_sha256"])
        self.assertNotEqual(control["before_sha256"], control["after_sha256"])
        self.assertFalse(control["semantic_change"])
        self.assertNotEqual(control["provider_exit_code"], 0)
        stderr = (EVIDENCE / "altered-artifact" / "negative-provider-stderr.txt").read_text(encoding="utf-8")
        self.assertIn(control["after_sha256"], stderr)
        self.assertIn("HTTP 404", stderr)

    def test_wrong_identity_and_attempt_are_distinct(self) -> None:
        workflow = load_json(EVIDENCE / "wrong-workflow" / "negative-observation.json")
        attempt = load_json(EVIDENCE / "wrong-run-attempt" / "negative-observation.json")
        self.assertNotEqual(workflow["expected_workflow_id"], workflow["deliberately_wrong_workflow_id"])
        self.assertNotEqual(attempt["expected_run_attempt"], attempt["observed_run_attempt"])
        self.assertEqual(workflow["observed_producer_run_id"], attempt["producer_run_id"])


if __name__ == "__main__":
    unittest.main()
