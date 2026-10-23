# Diagnostic Procedures & Health Probes

Structured guide for diagnosing runtime issues.

## Diagnostic Commands

```bash
# Complete system diagnosis
m31a doctor

# Category-specific probe
m31a doctor --category environment
m31a doctor --category git
m31a doctor --category models
m31a doctor --category sandbox
m31a doctor --category storage

# Inspect recent execution spans
m31a telemetry inspect <RUN_ID> --spans
```
