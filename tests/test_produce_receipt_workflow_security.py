"""Static safety checks for the dormant receipt-producer workflow."""

from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "evoguard-produce-release-source-receipt.yml"


class ProduceReceiptWorkflowSecurityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_accepts_only_the_named_completed_a_workflow_when_enabled(self) -> None:
        self.assertIn("workflow_run:", self.workflow)
        self.assertIn('workflows: ["EvoGuard Receipt Pilot Reverify"]', self.workflow)
        self.assertIn("types: [completed]", self.workflow)
        self.assertIn("EVOGUARD_RECEIPT_PILOT_CHAIN_ENABLED == 'true'", self.workflow)
        self.assertNotIn("workflow_dispatch:", self.workflow)
        self.assertNotIn("pull_request_target:", self.workflow)
        self.assertNotIn("\n  push:", self.workflow)

    def test_has_only_the_minimum_producer_authority(self) -> None:
        self.assertIn("permissions: {}", self.workflow)
        self.assertIn("attestations: write", self.workflow)
        self.assertIn("id-token: write", self.workflow)
        self.assertNotIn("contents: write", self.workflow)
        self.assertNotIn("actions/checkout", self.workflow)
        self.assertEqual(self.workflow.count("environment:"), 1)
        self.assertNotIn("self-hosted", self.workflow)
        self.assertNotIn("release create", self.workflow)

    def test_test_only_moved_main_gate_is_before_preflight_and_receipt(self) -> None:
        for required in (
            "negative_main_move_gate:",
            "EVOGUARD_RECEIPT_PILOT_NEGATIVE_MAIN_MOVE_CONTROL == 'moved-main-control-v1'",
            "evoguard-receipt-pilot-negative-main-move",
            "deployment: false",
            "Require the approved marker to advance protected main",
            "moved-main control requires protected main to advance before approval",
            "moved-main control requires one direct protected-main successor",
            "needs: negative_main_move_gate",
            "needs.negative_main_move_gate.result == 'success'",
            "needs.negative_main_move_gate.result == 'skipped'",
        ):
            self.assertIn(required, self.workflow)
        gate = self.workflow.index("negative_main_move_gate:")
        preflight = self.workflow.index("  preflight:")
        receipt = self.workflow.index("  receipt:")
        current_main_check = self.workflow.index("protected main changed after reverify")
        download = self.workflow.index("Download exactly the triggering reverify evidence attempt")
        self.assertLess(gate, preflight)
        self.assertLess(preflight, receipt)
        self.assertLess(gate, current_main_check)
        self.assertLess(current_main_check, download)
        gate_text = self.workflow[gate:preflight]
        self.assertIn("permissions:\n      contents: read", gate_text)
        self.assertNotIn("actions: read", gate_text)
        self.assertNotIn("attestations: write", gate_text)
        self.assertNotIn("id-token: write", gate_text)
        self.assertNotIn("secrets.", gate_text)

    def test_pins_the_trigger_and_rechecks_raw_git_before_receipt_creation(self) -> None:
        for required in (
            "EVOGUARD_RELEASE_SOURCE_REVERIFY_WORKFLOW_ID",
            "EVOGUARD_RELEASE_SOURCE_REVERIFY_WORKFLOW_BLOB_SHA",
            "EVOGUARD_RELEASE_SOURCE_RECEIPT_WORKFLOW_ID",
            "EVOGUARD_RELEASE_SOURCE_RECEIPT_WORKFLOW_BLOB_SHA",
            "run.conclusion !== 'success'",
            "protected main changed after reverify",
            "git init --bare",
            "derive-release-source-controls",
            "cmp \"$EVIDENCE/source.json\" \"$RUNNER_TEMP/source.json\"",
            "create-release-source-producer-receipt",
        ):
            self.assertIn(required, self.workflow)

    def test_snapshots_exactly_the_bounded_data_only_evidence_set(self) -> None:
        for required in (
            "evoguard-release-source-evidence-v1-${{ needs.preflight.outputs.trigger_run_attempt }}",
            "O_NOFOLLOW",
            "source.json': 128 * 1024",
            "context.json': 256 * 1024",
            "verdict.json': 8 * 1024 * 1024",
            "handoff.json': 512 * 1024",
            "evoguard-release-source-producer-receipt-v1-${{ github.run_attempt }}",
        ):
            self.assertIn(required, self.workflow)

    def test_uses_only_full_sha_pins_and_attests_after_receipt_creation(self) -> None:
        for required in (
            "actions/github-script@3a2844b7e9c422d3c10d287c895573f7108da1b3",
            "actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c",
            "actions/attest@f7c74d28b9d84cb8768d0b8ca14a4bac6ef463e6",
            "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
            "sha256sum --check",
        ):
            self.assertIn(required, self.workflow)
        self.assertLess(
            self.workflow.index("create-release-source-producer-receipt"),
            self.workflow.index("actions/attest@"),
        )
        action_lines = [line for line in self.workflow.splitlines() if "uses:" in line]
        self.assertTrue(action_lines)
        for line in action_lines:
            self.assertRegex(
                line,
                r"uses:\s+[^\s@]+/[^\s@]+@[0-9a-f]{40}(?:\s+#|$)",
            )


if __name__ == "__main__":
    unittest.main()
