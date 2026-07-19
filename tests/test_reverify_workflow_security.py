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

    def test_has_no_timing_hook_or_variable_controlled_delay(self) -> None:
        self.assertNotIn("test_postverify_hold", self.workflow)
        self.assertNotIn("moved-main control", self.workflow)
        self.assertNotIn("sleep 300", self.workflow)
        self.assertNotIn("EVOGUARD_RECEIPT_PILOT_POSTVERIFY_HOLD", self.workflow)

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
            "actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1",
            "vars.EVOGUARD_BOOTSTRAP_RUNTIME_URL",
            "vars.EVOGUARD_BOOTSTRAP_RUNTIME_SHA256",
            "sha256sum --check",
        ):
            self.assertIn(required, self.workflow)

    def test_bootstraps_a_hash_locked_judge_before_any_checkout(self) -> None:
        setup = "Set up the unprivileged judge Python runtime"
        install = "Install hash-locked judge test dependencies"
        checkout = "Checkout exact parent only"
        guard = "Re-verify parent to protected main without credentials"
        self.assertLess(self.workflow.index(setup), self.workflow.index(install))
        self.assertLess(self.workflow.index(install), self.workflow.index(checkout))
        self.assertLess(self.workflow.index(checkout), self.workflow.index(guard))
        for required in (
            'python-version: "3.12"',
            "--only-binary=:all:",
            "--require-hashes",
            "pytest==9.0.3",
            "colorama==0.4.6",
            "iniconfig==2.3.0",
            "packaging==26.2",
            "pluggy==1.6.0",
            "pygments==2.20.0",
            "2c5efc453d45394fdd706ade797c0a81091eccd1d6e4bccfcd476e2b8e0ab5d9",
            "4f1d9991f5acc0ca119f9d443620b77f9d6b33703e51011c16baf57afb285fc6",
            "f631c04d2c48c52b84d0d0549c99ff3859c98df65b3101406327ecc7d53fbf12",
            "5fc45236b9446107ff2415ce77c807cee2862cb6fac22b8a73826d0693b0980e",
            "e920276dd6813095e9377c0bc5566d94c932c33b27a3e3945d8389c374dd4746",
            "81a9e26dd42fd28a23a2d169d86d7ac03b46e2f8b59ed4698fb4785f946d0176",
        ):
            self.assertIn(required, self.workflow)

    def test_hash_locked_bootstrap_does_not_pass_a_literal_escape_to_pip(self) -> None:
        command = (
            'python -m pip install --disable-pip-version-check --only-binary=:all: '
            '--require-hashes -r "$RUNNER_TEMP/reverify-requirements.txt"'
        )
        self.assertIn(command, self.workflow)
        self.assertNotIn("--only-binary=:all: " + "\\" * 2, self.workflow)

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
