"""Static safety checks for the dormant receipt-pilot reverify workflow."""

from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "evoguard-release-source-reverify.yml"


class ReverifyWorkflowSecurityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_is_manual_and_disabled_until_the_chain_is_explicitly_enabled(self) -> None:
        self.assertIn("workflow_dispatch:", self.workflow)
        self.assertIn("EVOGUARD_RECEIPT_PILOT_CHAIN_ENABLED == 'true'", self.workflow)
        self.assertNotIn("pull_request_target:", self.workflow)
        self.assertNotIn("workflow_call:", self.workflow)
        self.assertNotIn("\n  push:", self.workflow)
        self.assertNotIn("\n  pull_request:", self.workflow)

    def test_has_no_privileged_or_admission_capability(self) -> None:
        self.assertIn("permissions: {}", self.workflow)
        self.assertNotIn("contents: write", self.workflow)
        self.assertNotIn("id-token: write", self.workflow)
        self.assertNotIn("attestations: write", self.workflow)
        self.assertNotIn("environment:", self.workflow)
        self.assertNotIn("actions/attest", self.workflow)
        self.assertNotIn("self-hosted", self.workflow)
        self.assertNotIn("release create", self.workflow)

    def test_binds_the_candidate_to_pre_execution_and_raw_git_controls(self) -> None:
        for required in (
            "workflow_run_id",
            "workflow_run_attempt",
            "persist-credentials: false",
            "--base-tree-sha",
            "--head-tree-sha",
            "derive-release-source-controls",
            "release-source-handoff",
            "git init --bare",
            "cmp \"$CONTROL\" \"$RUNNER_TEMP/source.json\"",
        ):
            self.assertIn(required, self.workflow)

    def test_uses_only_pinned_actions_and_the_repository_bootstrap_variables(self) -> None:
        for required in (
            "actions/github-script@3a2844b7e9c422d3c10d287c895573f7108da1b3",
            "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0",
            "actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c",
            "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
            "vars.EVOGUARD_BOOTSTRAP_RUNTIME_URL",
            "vars.EVOGUARD_BOOTSTRAP_RUNTIME_SHA256",
            "sha256sum --check",
        ):
            self.assertIn(required, self.workflow)

    def test_uploads_only_the_four_data_evidence_files(self) -> None:
        expected = (
            "${{ runner.temp }}/source.json",
            "${{ runner.temp }}/context.json",
            "${{ runner.temp }}/verdict.json",
            "${{ runner.temp }}/handoff.json",
        )
        for path in expected:
            self.assertIn(path, self.workflow)
        self.assertIn("evoguard-release-source-evidence-v1-${{ github.run_attempt }}", self.workflow)
        self.assertIn("retention-days: 1", self.workflow)


if __name__ == "__main__":
    unittest.main()
