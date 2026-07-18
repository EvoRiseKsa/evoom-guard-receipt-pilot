# Pilot status and execution boundary

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

Do not set `EVOGUARD_RECEIPT_PILOT_CHAIN_ENABLED` yet. P3 must add C and P4
must be a source-only calculator change before the first live round.

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
   blob SHA. Repeat for B. Only then add C, add a source-only P4 change, and
   run a complete chain while `main` remains unchanged.

## Required live rounds

Before any V2 or admission discussion, preserve public-safe evidence for:

- one clean A-to-B-to-C run;
- a moved-`main` rejection;
- an altered-artifact rejection;
- a wrong workflow/run-attempt rejection; and
- a failed-A rejection.

No result from this repository is production approval or a release decision.
