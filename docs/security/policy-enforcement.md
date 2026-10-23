# Policy Enforcement Mechanics

Technical implementation of Layer 1 policy evaluation.

## Rule Matching Algorithm

Rules in `src/policy/matcher.rs` match on:
1. Tool identifier (e.g. `fs:write`, `cli:bash`, `git:commit`)
2. Target path canonicalization (resolving symlinks and `..` traversals)
3. Autonomy mode constraints
4. Effective risk score

Evaluation returns `PolicyDecision::Allow`, `Deny`, `Ask`, or `Escalate`.
