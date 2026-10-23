# Threat Model & Attack Surface

Analysis of threats and how M31A mitigates them.

### Prompt Injection
Untrusted repository data (e.g. comments, READMEs) attempting to instruct the model to "delete all files" or "curl evil.com".
- *Mitigation*: The LLM has zero direct execution authority. Mutating commands trigger the Policy Gate, requiring human approval (`Ask`) in Safe mode or strict denial (`Deny`) in Plan mode.

### Secret Exfiltration
Model attempting to read `~/.ssh/id_rsa` or `~/.aws/credentials` and output them.
- *Mitigation*: Sensitive path filters block reads at the kernel seam before filesystem IO occurs. Network egress is restricted exclusively to NVIDIA NIM endpoints.
