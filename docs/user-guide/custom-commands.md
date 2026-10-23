# User-Defined Slash Commands

Operators can extend M31A's cockpit with reusable, project-specific custom slash commands defined in TOML.

## Custom Command Schema

Store custom commands in `.m31a/commands/<name>.toml` or user global directory `~/.config/m31a/commands/`:

```toml
# .m31a/commands/review-pr.toml
name = "review-pr"
description = "Perform rigorous architecture and security review of current Git diff"
role = "reviewer"
profile = "security_review"
autonomy = "safe"

prompt = """
Inspect all uncommitted changes or diff against origin/master.
Verify that:
1. No sensitive credentials or API keys are exposed.
2. Error handling does not use unwrap() in production paths.
3. Unit tests are included for new code paths.
Emit a structured review scorecard with findings categorized by severity.
"""
```

## Invocation

Once defined, the command appears in the TUI autocomplete and can be executed directly:

```text
> /review-pr
```

Or from the CLI:

```bash
m31a run "/review-pr"
```
