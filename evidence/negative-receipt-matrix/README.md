# Receipt negative matrix — 2026-07-22

This directory freezes the exact public-safe data from the three remaining
receipt-negative controls. All controls used the same protected-`main` commit
`3276acc17ac009115530e46d73ee743c53da536d` and the same B receipt bytes.
They are non-admitting evidence only.

## Fixed upstream chain

- A [run 29880368085](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29880368085)
  succeeded at attempt 1. Its control artifact was ID `8514511618`, digest
  `sha256:e9d3b820e1bfaad9af2592cdb2b902f83ec6dafccca706f0889ee0a545b4c4bb`;
  its evidence artifact was ID `8514518380`, digest
  `sha256:ae79ff98c270b7462e0d784ee659c1da3be3fa65327c92c6f980e7b038aa23bf`.
- B [run 29880394791](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29880394791)
  succeeded at attempt 1 and produced artifact ID `8514524549`, digest
  `sha256:e5d522037f4c90a9980a086a4df7ed2f00c2c6732ca4f04fcb3ccabd7f5c488c`.
  The exact `producer-receipt.json` SHA-256 is
  `7717c53a6a8874955aaf4cbc556fe69042be562e48dc236d9c04043b6b961061`.
- C used [run 29880410278](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29880410278)
  with a separate attempt for each controlled rejection below. Protected
  `main` did not move during the matrix.

The A and B workflow blobs were respectively
`73a1add9053e33bd249dc4b986a24fdf6cfa537c` and
`813e0492c0b33308b6dd027511dc610f574d7691`. The bootstrap runtime was the
published v3.8.0 artifact with SHA-256
`47bdcfbe2814fdd687afd62d1c476cbd5248db65683c97d2867a56dbbf9ee643`.

## Expected rejections

1. C attempt 2 selected `wrong-workflow-v1`. It first established that the
   event was the real configured B run, then substituted the distinct pinned A
   workflow ID (`315913599`) for the expected B workflow ID (`315921551`). The
   producer-workflow identity predicate rejected it before artifact download.
2. C attempt 3 selected `wrong-run-attempt-v1`. It downloaded and snapshotted
   the exact B artifact, then required attempt 2 while the receipt bound itself
   to attempt 1. The producer binding rejected it before provider verification.
3. C attempt 4 selected `altered-artifact-v1`. The unaltered bytes first passed
   a fresh constrained GitHub provider verification on the same runner. The
   control then inserted one ASCII space before the final LF; parsed JSON
   semantics stayed unchanged, while SHA-256 changed from `7717c53a...61061`
   to `9247857d...46835`. The provider returned exit code 1 and HTTP 404 for the
   changed subject digest. It did not accept the altered bytes.

The per-control `negative-observation.json` files are the workflow-produced
records. `unaltered-provider-baseline.json` is the exact successful provider
output from immediately before mutation; the paired stdout/stderr files are
the exact failed provider output after mutation. Later reruns replaced the
earlier attempt artifacts on GitHub, so the attempt-2 and attempt-3 files were
downloaded before the next rerun and are frozen here with a repository-level
manifest.

## Correction discovered before the recorded matrix

An initial source-only attempt exposed a GitHub job-dependency issue: A
[run 29880153019](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29880153019)
succeeded, and B [run 29880175433](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29880175433)
passed preflight, but GitHub skipped B's receipt job because the optional
moved-main gate was a transitive skipped dependency. C
[run 29880185555](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29880185555)
then rejected the missing receipt. No attestation was produced. PR
[#22](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/pull/22)
added an explicit `always() && needs.preflight.result == 'success'` condition;
the recorded B run above confirms the receipt job then executed only after a
successful preflight.

## Boundary and cleanup

`EVOGUARD_RECEIPT_PILOT_CHAIN_ENABLED` and
`EVOGUARD_RECEIPT_PILOT_NEGATIVE_RECEIPT_CONTROL` were deleted immediately
after C attempt 4 terminated. No secret, private key, Environment, OIDC write,
release, deployment, publication, merge, signing, or `ALLOW` operation existed
in C.

The GitHub roles are operational only: `EvoRiseKsa` and `MANA-awam` are
controlled by the same owner. This is not independent review. GitHub's
attestation authenticates B's receipt bytes and workflow provenance; it does
not independently prove that A executed Guard, nor does any result here prove
code correctness or authorize production use.
