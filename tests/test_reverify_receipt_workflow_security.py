"""Static safety checks for the dormant receipt-pilot fresh verifier."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "evoguard-reverify-release-source-receipt.yml"


class ReverifyReceiptWorkflowSecurityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_accepts_only_the_named_completed_b_workflow_when_enabled(self) -> None:
        for required in (
            "workflow_run:",
            'workflows: ["EvoGuard Receipt Pilot Produce Receipt"]',
            "types: [completed]",
            "github.event.workflow_run.event == 'workflow_run'",
            "EVOGUARD_RECEIPT_PILOT_CHAIN_ENABLED == 'true'",
            "String(run.workflow_id) !== expected",
            "run.conclusion !== 'success'",
            "run.head_branch !== 'main'",
            "run.head_repository?.full_name",
            "protected main changed after receipt production",
        ):
            self.assertIn(required, self.workflow)
        for forbidden in (
            "workflow_dispatch:",
            "workflow_call:",
            "pull_request_target:",
            "\n  push:",
            "\n  pull_request:",
        ):
            self.assertNotIn(forbidden, self.workflow)
        self.assertLess(
            self.workflow.index("protected main changed after receipt production"),
            self.workflow.index("Download exact producer receipt attempt"),
        )

    def test_has_read_only_nonadmitting_authority(self) -> None:
        self.assertIn("permissions: {}", self.workflow)
        for required in ("actions: read", "attestations: read", "contents: read"):
            self.assertIn(required, self.workflow)
        for forbidden in (
            "contents: write",
            "actions: write",
            "attestations: write",
            "id-token: write",
            "pull-requests: write",
            "checks: write",
            "deployments: write",
            "actions/checkout",
            "actions/attest",
            "environment:",
            "secrets.",
            "self-hosted",
            "sign-key",
            "git checkout",
            "git clone",
            "pip install",
            "npm install",
            "pytest",
            "GITHUB_WORKSPACE",
        ):
            self.assertNotIn(forbidden, self.workflow)

    def test_pins_b_and_binds_all_upstream_administrative_anchors(self) -> None:
        for required in (
            "EVOGUARD_RELEASE_SOURCE_REVERIFY_WORKFLOW_ID",
            "EVOGUARD_RELEASE_SOURCE_REVERIFY_WORKFLOW_BLOB_SHA",
            "EVOGUARD_RELEASE_SOURCE_RECEIPT_WORKFLOW_ID",
            "EVOGUARD_RELEASE_SOURCE_RECEIPT_WORKFLOW_BLOB_SHA",
            "git init --bare",
            "+refs/heads/main:refs/heads/main",
            "workflow_path': '.github/workflows/evoguard-produce-release-source-receipt.yml'",
            "trigger_workflow_path': '.github/workflows/evoguard-release-source-reverify.yml'",
            "producer.get('workflow_id') == producer.get('trigger_workflow_id')",
            "producer.get('workflow_run_id') == producer.get('trigger_workflow_run_id')",
        ):
            self.assertIn(required, self.workflow)

    def test_downloads_only_the_exact_b_attempt_and_snapshots_bounded_data(self) -> None:
        for required in (
            "evoguard-release-source-producer-receipt-v1-${{ github.event.workflow_run.run_attempt }}",
            "run-id: ${{ github.event.workflow_run.id }}",
            "github-token: ${{ github.token }}",
            "O_NOFOLLOW",
            "source.json': 128 * 1024",
            "context.json': 256 * 1024",
            "verdict.json': 8 * 1024 * 1024",
            "handoff.json': 512 * 1024",
            "producer.json': 128 * 1024",
            "producer-receipt.json': 512 * 1024",
            "downloaded receipt has an unexpected file set",
        ):
            self.assertIn(required, self.workflow)

    def test_freshly_verifies_the_receipt_and_provider_attestation_as_archive_only(self) -> None:
        for required in (
            "EVOGUARD_BOOTSTRAP_RUNTIME_URL",
            "EVOGUARD_BOOTSTRAP_RUNTIME_SHA256",
            "sha256sum --check",
            "GH_TOKEN: ${{ github.token }}",
            "reverify-attested-release-source-producer-receipt",
            "--github-policy",
            "--github-receipt-out",
            "--github-raw-output-out",
            "--allow-nonadmitting-evidence",
            "https://token.actions.githubusercontent.com",
            ".github/workflows/evoguard-produce-release-source-receipt.yml",
            "evoguard-release-source-preflight-v1-${{ github.run_attempt }}",
            "retention-days: 1",
            "No release-source ALLOW",
        ):
            self.assertIn(required, self.workflow)
        self.assertLess(
            self.workflow.index("Bind downloaded inputs to both protected workflow runs"),
            self.workflow.index("Freshly verify raw Git, receipt bytes, and provider attestation"),
        )

    def test_uses_only_full_sha_pins(self) -> None:
        for required in (
            "actions/github-script@3a2844b7e9c422d3c10d287c895573f7108da1b3",
            "actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c",
            "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
        ):
            self.assertIn(required, self.workflow)
        action_lines = [line for line in self.workflow.splitlines() if "uses:" in line]
        self.assertTrue(action_lines)
        for line in action_lines:
            self.assertRegex(
                line,
                r"uses:\s+[^\s@]+/[^\s@]+@[0-9a-f]{40}(?:\s+#|$)",
            )


if __name__ == "__main__":
    unittest.main()
