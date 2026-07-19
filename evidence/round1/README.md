# Controlled live round 1

This directory preserves the exact public-safe payloads downloaded from the
first successful controlled A-to-B-to-C receipt-pilot round on 2026-07-19.
The GitHub Actions artifacts expire after one day; this commit retains the
payloads and their SHA-256 manifest without adding credentials, customer data,
private keys, or production code.

## Runs and binding

All stages completed successfully on the same protected-`main` commit
`eaec5be2d1f98ea1aa665438ec90f9531d33da2b`:

- A — [manual reverify run 29673270182](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29673270182)
- B — [automatic producer run 29673284587](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29673284587)
- C — [automatic fresh re-verification run 29673294302](https://github.com/EvoRiseKsa/evoom-guard-receipt-pilot/actions/runs/29673294302)

`a/`, `b/`, and `c/` preserve the downloaded payloads from those stages.
`MANIFEST.sha256` covers those payloads exactly; it intentionally excludes
this explanatory file.

## Reproduction checks

From this directory, check the stored byte hashes with a SHA-256 tool. Then
independently re-query GitHub's attestation service for B's exact receipt:

```bash
gh attestation verify b/producer-receipt.json \
  --repo EvoRiseKsa/evoom-guard-receipt-pilot \
  --signer-workflow EvoRiseKsa/evoom-guard-receipt-pilot/.github/workflows/evoguard-produce-release-source-receipt.yml \
  --signer-digest eaec5be2d1f98ea1aa665438ec90f9531d33da2b \
  --source-digest eaec5be2d1f98ea1aa665438ec90f9531d33da2b \
  --source-ref refs/heads/main \
  --deny-self-hosted-runners
```

At archival time, the file
`b/producer-receipt.json` had SHA-256
`6cce351ea8722d5c1f6055a265baa4492de7d5bbdcb07721e5dafa3bb444345d`.
C's `fresh-provider-receipt.json` records the same digest and a verified
attestation count of one.

## What this establishes — and does not establish

The files establish that the recorded Actions stages completed under their
bounded workflow conditions, that B created the retained receipt bytes, and
that GitHub's attestation verification accepted one provenance attestation for
those bytes with the stated signer, source, reference, and hosted-runner
constraints.

They do **not** establish an `ALLOW`, artifact admission, release,
deployment, merge decision, code correctness, code security, or independent
security review. The receipt and provider attestation do not independently
prove that A executed Guard; that limitation is deliberate and remains a
prerequisite for any separate V2/admission design.
