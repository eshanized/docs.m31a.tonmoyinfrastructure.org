# Contributor Guidelines

Guidelines for submitting bug reports, documentation updates, and pull requests to M31A.

## Non-Negotiable Rules

1. Single crate architecture: Do not introduce Cargo workspace splits.
2. Downward dependency discipline: Lower layers must not import higher layers.
3. Policy gate non-bypassability: All side effects must pass through Layer 1.
4. TUI is a read-only projection: Authoritative state belongs in SQLite.
5. No fake success: Unimplemented paths return explicit errors.
