# Pilot status and execution boundary

## P0 baseline: fixture and policy, intentionally inert

This baseline establishes a public-safe executable fixture, a base-owned
black-box policy, and a judge-owned protocol pack. It does not add workflow A,
B, or C and does not create an artifact attestation.

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
   blob SHA. Repeat for B. Only then add C and run a complete chain while
   `main` remains unchanged.

## Required live rounds

Before any V2 or admission discussion, preserve public-safe evidence for:

- one clean A-to-B-to-C run;
- a moved-`main` rejection;
- an altered-artifact rejection;
- a wrong workflow/run-attempt rejection; and
- a failed-A rejection.

No result from this repository is production approval or a release decision.
