# Pilot status and execution boundary

## Baseline: created, intentionally inert

This baseline establishes a public-safe fixture and the policy boundary. It
does not add workflow A, B, or C and does not create an artifact attestation.

## Hard prerequisites before activating A-to-B-to-C

1. Publish a new EvoOM Guard runtime containing the receipt CLI from a reviewed
   core release. The `v3.7.0` asset is not valid: it predates the receipt code.
2. Verify the new runtime's exact SHA-256 and use its immutable HTTPS URL.
3. Protect `main` with linear history, required review, CODEOWNERS, and required
   checks. The reviewer role is operational separation only; the two accounts
   belong to the same owner and are not independent security review.
4. Add only repository Actions **variables** for the pinned runtime and the
   reviewed A/B workflow identity. Variables are administrator-controlled trust
   anchors; they are not Git objects and must be audited separately.
5. Add A, review and merge it, then record A's numeric workflow ID and raw-Git
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
