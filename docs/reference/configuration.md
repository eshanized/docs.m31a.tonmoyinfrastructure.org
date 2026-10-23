# Configuration Schema & Precedence Reference

Complete specification of M31A configuration fields and defaults.

## Configuration File Example (`config.toml`)

```toml
# Authoritative defaults from src/config/canonical.rs
model = "meta/llama-3.2-11b-vision-instruct"

[runtime]
sandbox_mode = "standard"
concurrency_limit = 4
timeout_secs = 300

[policy]
default_action = "ask"
interactive_approvals = true
sandbox_mode = "standard"

[git]
branch_prefix = "m31a/run"
retention_policy = "keep_on_failure"
execution_isolation = "best_effort"

[tui]
theme = "dark-slate-cyan"
fps = 30
```
