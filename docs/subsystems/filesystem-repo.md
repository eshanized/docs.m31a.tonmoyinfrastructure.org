# Subsystem: Filesystem & Repository Intelligence

Indexes codebases and handles file mutations (`src/repo/`, `src/change/`).

## Code Intelligence

- AST symbol parsing and definition lookup (`src/repo/symbols.rs`).
- Fast regex and keyword search across repositories (`src/repo/search.rs`).
- Workspace drift detection comparing active files against pre-execution baselines.
