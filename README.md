# EvoOM Guard Receipt Pilot

This repository is a **public, disposable, non-production** pilot for the
EvoOM Guard Authenticated Producer Receipt research path.

It exists to test the following evidence-only topology on GitHub Actions:

```text
A. protected-main reverify (manual dispatch)
        -> B. provider-attested producer receipt (workflow_run)
        -> C. fresh preflight re-verification (workflow_run)
```

## Public-data boundary

Everything committed here and every Actions artifact must be safe for public
disclosure. Do **not** add any of the following:

- credentials, tokens, private keys, or Environment secrets;
- customer code, production source, incident evidence, or private diagnostics;
- a release, deployment, publishing step, or an admission key;
- an `ALLOW` claim or a claim that the receipt independently proves Guard ran.

The fixture is intentionally a tiny calculator. Its only job is to make the
control flow and negative tests observable without exposing real data.

## Current status

The bootstrap prerequisite is met by the immutable
[`v3.8.0` Guard release](https://github.com/EvoRiseKsa/EvoOM-Guard-m/releases/tag/v3.8.0):

- URL: `https://github.com/EvoRiseKsa/EvoOM-Guard-m/releases/download/v3.8.0/evo-guard.pyz`
- SHA-256: `47bdcfbe2814fdd687afd62d1c476cbd5248db65683c97d2867a56dbbf9ee643`

This baseline adds a small CLI fixture, a base-owned black-box policy, a
judge-owned verifier pack, and registered A, B, and C workflows
(`.github/workflows/evoguard-release-source-reverify.yml`,
`.github/workflows/evoguard-produce-release-source-receipt.yml`, and
`.github/workflows/evoguard-reverify-release-source-receipt.yml`).  A is **disabled
by default**: it runs only when the administrator-controlled Actions variable
`EVOGUARD_RECEIPT_PILOT_CHAIN_ENABLED` is exactly `true`. That variable is
absent by default. A has one test-only manual boolean input,
`test_postverify_hold`, which defaults to `false` and merely pauses the
unprivileged workflow for a fixed five minutes *after* it has uploaded its
data-only evidence. It exists solely to perform the documented moved-`main`
rejection control; it adds no permission, secret, Environment, write, or
candidate execution. The activation variable is enabled only for one
controlled round after B and C are reviewed, then deleted immediately after
the terminal outcome. The required A/B workflow identifiers and raw-Git blob
SHA anchors are recorded as administrator-controlled variables.

B is triggered only by a completed A run, validates A's numeric workflow ID,
re-derives the raw-Git controls without a candidate checkout, then can ask
GitHub to attest the exact receipt bytes. It has the attestation permission
only when the same activation variable is `true`; it is inactive now and does
not by itself make an admission, release, deployment, or `ALLOW` decision.

C is triggered only by a completed B run. It has read-only `actions`,
`contents`, and attestation permissions, rechecks the current protected-main
identity and both A/B raw-Git anchors, and invokes the published v3.8 runtime
to make a **fresh** GitHub Artifact Attestation verification of B's exact
receipt bytes. It preserves only data-only verification evidence. C does not
make an admission, release, deployment, merge, or publication decision.

CI downloads the published runtime, verifies its SHA-256, and checks that the
policy's pack digest matches that runtime's canonical `pack-doctor` result.
It does **not** run A, B, or C, produce a receipt, publish software, or make
an admission decision.

See [PILOT_STATUS.md](PILOT_STATUS.md) for the staged plan and hard stop
conditions. One controlled clean round completed on 2026-07-19; its exact
public-safe evidence is retained in
[evidence/round1](evidence/round1/README.md). The status file records both
the completed round and prior fail-closed attempts.

## What success means

A successful round means only that the public evidence chain is internally
consistent and that GitHub attested the receipt bytes created by stage B. It
does not make an admission decision, publish software, or prove independently
that stage A executed the Guard runtime.

This repository is source-available under the included license.
