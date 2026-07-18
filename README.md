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

The repository is intentionally inert at baseline. It has no active receipt
workflows yet. The merged receipt contract in
[`EvoOM-Guard-m`](https://github.com/EvoRiseKsa/EvoOM-Guard-m) needs a new,
byte-pinned Guard runtime before a live A-to-B-to-C experiment can run. The
published `v3.7.0` zipapp predates the receipt CLI and must not be used here.

See [PILOT_STATUS.md](PILOT_STATUS.md) for the staged plan and hard stop
conditions.

## What success means

A successful round means only that the public evidence chain is internally
consistent and that GitHub attested the receipt bytes created by stage B. It
does not make an admission decision, publish software, or prove independently
that stage A executed the Guard runtime.

This repository is source-available under the included license.
