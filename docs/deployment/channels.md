# Deployment Channels & Updates

M31A maintains two completely isolated channels:

| Property | Production Channel (`m31a`) | Development Channel (`m31a-dev`) |
|---|---|---|
| **Binary Name** | `m31a` | `m31a-dev` |
| **Cargo Feature**| Default (no feature) | `--features development` |
| **Global State** | `~/.local/share/m31a/` | `~/.local/share/m31a-dev/` |
| **Update Feed** | `stable` | `development` |
| **Mutual Exclusion**| Fails compile if both set | Fails compile if both set |

## In-Place Updater

```bash
# Check for updates
m31a update --check

# Apply update
m31a update

# Rollback to previous binary
m31a rollback
```
