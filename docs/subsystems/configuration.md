# Subsystem: Configuration Engine

The M31A configuration subsystem (`src/config/`) enforces deterministic resolution across 8 hierarchical tiers.

## The 8-Tier Precedence Hierarchy

Defined in `src/config/hierarchy.rs`:

```text
Tier 0: Immutable Security Invariants (Kernel hardcoded floors)
  ▲
Tier 1: System-wide Machine Configuration (/etc/m31a/config.toml)
  ▲
Tier 2: User Global Configuration (~/.config/m31a/config.toml)
  ▲
Tier 3: Workspace Repository Configuration (<repo>/.m31a/config.toml)
  ▲
Tier 4: Active Named Profile (safe, coding, autonomous, ci, release)
  ▲
Tier 5: Environment Variables (M31A_*, NVIDIA_API_KEY)
  ▲
Tier 6: CLI Argument Overrides (--config, --model, --autonomy)
  ▲
Tier 7: Interactive Session Overrides (/model, /profile slash commands)
```

## Monotonic Security Merging

The `MonotonicSecurityMerger` (`src/config/merge.rs`) guarantees that higher configuration tiers **can never weaken** security invariants established by lower tiers. A profile or CLI flag can enforce stricter policies (e.g. converting `Ask` to `Deny`), but cannot disable Landlock sandboxing or grant access to sensitive paths.
