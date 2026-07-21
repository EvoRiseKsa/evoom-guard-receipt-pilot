# Controlled Main-Move Markers

This public, inert document is reserved for explicitly reviewed protected-
`main` advances used by receipt-pilot negative controls. It contains no
executable configuration, policy, verifier pack, runtime pin, Actions
variable, credential, private data, evidence result, release operation,
deployment operation, admission decision, or `ALLOW` claim.

Its first change is intentionally a marker only. It becomes the main-moving
change `M` only in the separately documented moved-`main` control:

1. A source-only A run has completed successfully while protected `main` is
   the recorded source `S`.
2. The controlled B workflow has entered the test-only
   `negative_main_move_gate`. That gate is selected only by the two temporary
   repository variables and waits for the reviewer in the dedicated GitHub
   Environment; it creates no receipt before the gate passes.
3. This PR is then squash-merged to produce target `T`. `T` must have exactly
   one parent, and that parent must be `S`.
4. Only after that merge may the designated reviewer approve the Environment.
   B must then reject the changed protected `main` before receipt production,
   and C must reject B before artifact download.

The recorded result belongs in `PILOT_STATUS.md` only after the A, B, and C
outcomes are independently observed and archived. This marker does not itself
enable a receipt chain, authorize a merge, or assert a successful outcome.
