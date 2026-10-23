# Subsystem: Deployment Channels & Updates

Compile-time channel isolation and update mechanisms (`src/deployment/`).

## Mutually Exclusive Channels

- Production: binary `m31a`, global directory `~/.local/share/m31a`, feed `stable`.
- Development: binary `m31a-dev`, global directory `~/.local/share/m31a-dev`, feed `development`.
- Rollback mechanism restores previous binary from `.bak` backup if an update fails.
