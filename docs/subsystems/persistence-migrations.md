# Subsystem: Persistence & Migrations

SQLite database management and schema evolution (`src/persistence/`).

## WAL Mode & Connection Pool

- Configured with `PRAGMA journal_mode = WAL` and `PRAGMA synchronous = NORMAL`.
- Supports concurrent reader threads without blocking writes.
- Manages migrations 001 through 032.
