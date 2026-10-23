# Security Architecture & Threat Model

M31A is built on the principle that autonomous AI agents are untrusted actors operating inside your development environment.

## Threat Assumptions

- Model proposals may contain hallucinations, invalid syntax, or unintended side effects.
- Repository contents may contain prompt injection payloads designed to trick agents into exfiltrating secrets.
- External dependencies or build scripts may contain malicious post-install hooks.

## Defense Layers

1. **Non-Bypassable Policy Gate**: Evaluates every tool execution before invocation.
2. **Process Sandboxing**: Landlock filesystem sandboxing and seccomp system call filtering.
3. **Sensitive Path Blocking**: Absolute prohibition on accessing SSH keys, cloud tokens, or password stores.
4. **Secret Masking**: Prevents credentials from ever appearing in logs, events, or UI projections.
