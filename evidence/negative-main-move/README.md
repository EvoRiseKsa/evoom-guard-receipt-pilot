# Controlled moved-main rejection

This directory records the public-safe observation from the controlled
moved-`main` receipt-pilot test completed on 2026-07-21. The machine-readable
record is [`OBSERVATION.json`](OBSERVATION.json).

## Sequence and result

1. A completed successfully in
   [run 29675987307](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29675987307)
   against protected-`main` commit
   `a3fc9f14a8c683fa5466d0d4124826f3151cb4d0` (S).
2. B started from that successful A run and waited at the separately protected
   negative-control Environment before its preflight.
3. Reviewed marker-only [PR #16](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/pull/16)
   advanced `main` to the one-parent successor
   `1e7b0213ada2f03f1b4e3028a37398b45ad6eb02` (T), whose parent is exactly S.
4. After Environment approval, B
   [run 29676005850](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29676005850)
   rejected the changed protected branch during preflight with
   `protected main changed after reverify; refuse receipt production`.
   Its receipt job was skipped and the run produced zero artifacts.
5. C [run 29867423549](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29867423549)
   rejected the failed B trigger before artifact download with
   `trigger is not the configured successful producer-receipt workflow_run`.
   It also produced zero artifacts.
6. Both temporary activation variables were deleted after C reached its
   terminal state.

The main CI run for T,
[29867381230](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29867381230),
also completed successfully. That CI fact separates the intentional receipt
chain rejection from an unrelated failure of the marker commit.

## Claim boundary

This is a controlled fail-closed observation: B refused to create a receipt
after protected `main` moved away from A's recorded commit, and C refused the
failed B predecessor before download. It is not an `ALLOW`, an admission,
release, deployment, independent review, or proof that the implementation is
free from other defects.

The JSON file is an archival observation, not a live GitHub query. Re-query
GitHub before relying on current run, repository-variable, branch-protection,
or artifact-retention state.
