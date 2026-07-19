# Pilot status and execution boundary

## Current live-evidence state

One controlled, public-safe A-to-B-to-C round completed successfully on
2026-07-19. Every stage used the same protected-`main` commit
`eaec5be2d1f98ea1aa665438ec90f9531d33da2b`; `main` remained at that commit
through C's fresh verification, and the temporary activation variable was
deleted immediately afterward.

- [A reverify run 29673270182](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29673270182)
  completed successfully from manual `workflow_dispatch` and emitted the
  source control and data-only evidence inputs.
- [B producer run 29673284587](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29673284587)
  completed successfully from A's `workflow_run`, produced
  `producer-receipt.json`, and requested one GitHub Artifact Attestation for
  the exact receipt bytes.
- [C fresh re-verification run 29673294302](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29673294302)
  completed successfully from B's `workflow_run`, rechecked the raw-Git and
  workflow bindings, and freshly verified one attestation under its bounded
  GitHub policy.

The archived receipt hash is
`6cce351ea8722d5c1f6055a265baa4492de7d5bbdcb07721e5dafa3bb444345d`.
The complete exact-byte public evidence and its manifest are in
[evidence/round1](evidence/round1/README.md).

This is a successful *evidence-chain* result only. It is not an `ALLOW`,
admission, release, deployment, merge decision, independent review, or proof
of code correctness/security. In particular, GitHub's attestation proves the
identity and provenance of B's receipt bytes; it does not independently prove
that A executed Guard.

## Historical fail-closed controls

The preceding attempts remain useful negative evidence:

- [A run 29664749999](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29664749999)
  ended with the unprivileged-judge dependency error `/usr/bin/python: No
  module named pytest`; B and C rejected it without a receipt or attestation.
- [A run 29672581131](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29672581131)
  failed before candidate execution because a shell continuation passed a
  literal backslash to `pip`; its B and C successors again rejected the failed
  predecessor without producing or verifying a receipt.

The second failure was corrected by [PR #11](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/pull/11),
then a new source-only candidate was merged in
[PR #12](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/pull/12)
before the recorded positive round. The activation variable is absent now and
must stay absent except during a separately reviewed controlled round.

## Controlled moved-main rejection hook

The manual A workflow has one **test-only** boolean input named
`test_postverify_hold`, defaulting to `false`. When it is explicitly `true`,
A first completes its normal raw-Git re-derivation and uploads its fixed
data-only evidence set, then holds for exactly 300 seconds before it completes
and can trigger B. It adds no permission, secret, Environment, OIDC identity,
write operation, candidate execution, or variable-controlled duration.

Its only purpose is a reproducible moved-`main` negative control: during that
fixed window, merge one separately reviewed, public-safe marker-only PR that
does not modify workflows, policy, packs, runtime pins, Actions variables, or
evidence. B must then reject its predecessor because current protected `main`
is no longer A's recorded `head_sha`; its receipt job must be skipped. C must
then reject B's failed predecessor before artifact download. Delete the
activation variable only after C reaches its terminal outcome. If the marker
does not land within the 300-second window, or the observed jobs do not have
those outcomes, the round is inconclusive and must not be reported as a pass.

This hook is not an admission feature, a production delay, a release gate, or
a proof that any code is secure. It exists solely to make the existing B
fail-closed binding testable without a timing race.

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
