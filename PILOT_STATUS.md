# Pilot status and execution boundary

## Current live-evidence state

The A-to-B-to-C chain is currently disabled and **no successful clean
end-to-end round has been recorded**. The first controlled dispatch on
2026-07-18 is useful negative evidence, not a positive receipt result:

- [A reverify run 29664749999](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29664749999)
  completed with `ERROR` in the unprivileged judge before it produced a usable
  successful verdict: `/usr/bin/python: No module named pytest`.
- Its successor [B run 29664763518](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29664763518)
  rejected the non-successful A predecessor before producing a receipt or
  requesting an attestation.
- Its successor [C run 29664768973](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29664768973)
  rejected the non-successful B predecessor before downloading an artifact or
  verifying a receipt.

[PR #7](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/pull/7)
subsequently added a hash-locked `pytest` bootstrap to A. Its passing Pilot CI
does not prove the A-to-B-to-C chain: no A, B, or C run has been dispatched
after that bootstrap. The activation variable remains unset; do not enable it
until the live-round prerequisites below are satisfied and reviewed.

## P0 baseline: fixture and policy

This baseline establishes a public-safe executable fixture, a base-owned
black-box policy, and a judge-owned protocol pack. It does not create an
artifact attestation.

## P1: registered but disabled A reverify workflow

`.github/workflows/evoguard-release-source-reverify.yml` defines A with
`workflow_dispatch` only, `permissions: {}`, data-only artifacts, and a
raw-Git re-derivation check. It has no secrets, Environment, OIDC, write
permission, attestation, signing, release, or admission operation.

The metadata job requires the separate administrator-controlled Actions
variable `EVOGUARD_RECEIPT_PILOT_CHAIN_ENABLED` to equal `true`. The variable
must remain **unset** in P1, P2, and P3. Consequently, dispatching A now does
not checkout or execute a candidate.

After P1 is merged, record its numeric workflow ID and the raw-Git blob SHA
from `main` as these repository Actions variables:

```text
EVOGUARD_RELEASE_SOURCE_REVERIFY_WORKFLOW_ID
EVOGUARD_RELEASE_SOURCE_REVERIFY_WORKFLOW_BLOB_SHA
```

Do not change this workflow after recording its blob SHA; a change requires a
new review and pin.

## P2: registered but disabled B producer-receipt workflow

`.github/workflows/evoguard-produce-release-source-receipt.yml` defines B as
the only `workflow_run` consumer of the named A workflow. It is disabled by the
same absent activation variable. Before reading evidence it checks A's numeric
workflow ID, the exact successful triggering run, the current `main` SHA, and
the repository identity. It never checks out or executes the candidate.

When it is eventually enabled, B may use `attestations: write` and
`id-token: write` only to ask GitHub to attest the exact canonical receipt
file. It still has no secret, Environment, `contents: write`, signing,
release, publishing, or admission action.

After P2 is merged, record B's numeric workflow ID and raw-Git blob SHA from
`main` as these repository Actions variables:

```text
EVOGUARD_RELEASE_SOURCE_RECEIPT_WORKFLOW_ID
EVOGUARD_RELEASE_SOURCE_RECEIPT_WORKFLOW_BLOB_SHA
```

Do not set `EVOGUARD_RECEIPT_PILOT_CHAIN_ENABLED` yet. P4 must be a
source-only calculator change before the first live round.

## P3: registered but disabled C fresh receipt re-verification workflow

`.github/workflows/evoguard-reverify-release-source-receipt.yml` defines C as
the only `workflow_run` consumer of the named B workflow. It is disabled by
the same absent activation variable. Before it downloads an artifact, C checks
B's numeric workflow ID, the exact successful B run, the current `main` SHA,
and repository identity. It never checks out or executes candidate source.

When it is eventually enabled, C has only `actions: read`, `contents: read`,
and `attestations: read`. It snapshots a fixed, bounded B artifact set, binds
its contents to the A/B numeric IDs and raw-Git blob anchors, and uses the
published v3.8 runtime to make a fresh constrained GitHub Artifact Attestation
verification. Its data-only output is a non-admitting prerequisite, not an
`ALLOW`, release, deployment, publication, or merge decision.

C has no downstream trusted consumer in this pilot, so no C workflow variable
is required. Do not set `EVOGUARD_RECEIPT_PILOT_CHAIN_ENABLED` yet: P4 must
remain a source-only calculator change, followed by controlled positive and
negative rounds while `main` stays unchanged.

## Hard prerequisites before activating A-to-B-to-C

1. Use only the published immutable `v3.8.0` runtime, which contains the receipt
   CLI: `https://github.com/EvoRiseKsa/EvoOM-Guard-m/releases/download/v3.8.0/evo-guard.pyz`.
   Its SHA-256 is `47bdcfbe2814fdd687afd62d1c476cbd5248db65683c97d2867a56dbbf9ee643`.
2. Add those exact values as the repository Actions variables
   `EVOGUARD_BOOTSTRAP_RUNTIME_URL` and `EVOGUARD_BOOTSTRAP_RUNTIME_SHA256`.
   Variables are administrator-controlled trust anchors and must be audited
   separately from Git history.
3. Protect `main` with linear history, required review, CODEOWNERS, and required
   checks. The reviewer role is operational separation only; the two accounts
   belong to the same owner and are not independent security review.
4. Add A, review and merge it, then record A's numeric workflow ID and raw-Git
   blob SHA. Repeat for B. Add and review C; it has no downstream consumer so
   no C anchor is required. Only then add a source-only P4 change and run a
   complete chain while `main` remains unchanged.

## Required live rounds

Before any V2 or admission discussion, preserve public-safe evidence for:

- one clean A-to-B-to-C run;
- a moved-`main` rejection;
- an altered-artifact rejection;
- a wrong workflow/run-attempt rejection; and
- a failed-A rejection.

No result from this repository is production approval or a release decision.
