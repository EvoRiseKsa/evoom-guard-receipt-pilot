"""Integrity checks for the public archive of receipt-pilot live round 1."""

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "evidence" / "round1"
COMMIT = "eaec5be2d1f98ea1aa665438ec90f9531d33da2b"
RECEIPT_SHA256 = "6cce351ea8722d5c1f6055a265baa4492de7d5bbdcb07721e5dafa3bb444345d"


class RoundOneEvidenceTests(unittest.TestCase):
    def test_manifest_matches_each_archived_artifact_byte_for_byte(self) -> None:
        entries = {}
        for line in (EVIDENCE / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
            digest, relative_path = line.split("  ", 1)
            self.assertRegex(digest, r"^[0-9a-f]{64}$")
            self.assertNotIn("..", Path(relative_path).parts)
            entries[relative_path] = digest

        self.assertEqual(len(entries), 14)
        for relative_path, expected_digest in entries.items():
            actual_digest = hashlib.sha256(
                (EVIDENCE / relative_path).read_bytes()
            ).hexdigest()
            self.assertEqual(actual_digest, expected_digest, relative_path)

    def test_archived_stages_bind_the_same_commit_and_receipt_bytes(self) -> None:
        a_source = json.loads((EVIDENCE / "a" / "source.json").read_text(encoding="utf-8"))
        b_receipt = json.loads(
            (EVIDENCE / "b" / "producer-receipt.json").read_text(encoding="utf-8")
        )
        c_receipt = json.loads(
            (EVIDENCE / "c" / "fresh-provider-receipt.json").read_text(encoding="utf-8")
        )

        self.assertEqual(a_source["target_commit_sha"], COMMIT)
        self.assertEqual(b_receipt["source"]["target_commit_sha"], COMMIT)
        self.assertEqual(b_receipt["producer"]["workflow_commit_sha"], COMMIT)
        self.assertEqual(b_receipt["producer"]["trigger_workflow_run_id"], "29673270182")
        self.assertEqual(b_receipt["producer"]["workflow_run_id"], "29673284587")
        self.assertEqual(b_receipt["producer"]["workflow_id"], "315921551")
        self.assertEqual(b_receipt["producer"]["trigger_workflow_id"], "315913599")
        self.assertEqual(b_receipt["format"], "EVOGUARD_RELEASE_SOURCE_PRODUCER_RECEIPT_V1")
        self.assertEqual(c_receipt["artifact"]["sha256"], RECEIPT_SHA256)
        self.assertEqual(c_receipt["artifact"]["size"], 2420)
        self.assertEqual(c_receipt["verification_output"]["verified_attestation_count"], 1)
        self.assertTrue(c_receipt["verification_policy"]["deny_self_hosted_runners"])


if __name__ == "__main__":
    unittest.main()
