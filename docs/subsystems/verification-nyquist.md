# Subsystem: Verification & Nyquist Completion Gate

Enforces Law 6: Completion requires deterministic evidence (`src/verification/`).

## The 7-Tier Verification Hierarchy

```text
Tier 1: Deterministic Check (file presence, syntax, hash consistency)
  ▼
Tier 2: Compiler Check (cargo check, type verification)
  ▼
Tier 3: Test Runner (cargo test, pytest, npm test)
  ▼
Tier 4: Static Analysis (clippy, formatting, linter)
  ▼
Tier 5: Diff & Invariants (workspace baseline snapshot matching)
  ▼
Tier 6: Automated Reviewer (independent review role audit)
  ▼
Tier 7: Failure Diagnosis (diagnostician analysis on failure)
```

Fail-fast gating halts downstream checks immediately if an earlier tier fails.
