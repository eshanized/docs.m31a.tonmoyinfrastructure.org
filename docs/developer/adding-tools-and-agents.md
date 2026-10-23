# Adding Tools & Agent Roles

How to extend M31A with new capabilities or agent personas.

## Adding a New Tool

1. Implement the `TypedTool` trait in `src/tools/`.
2. Define input arguments with `serde::Deserialize`.
3. Specify required capabilities and risk classification.
4. Register the tool in `ToolRegistry::new_default` or `register_extended_tools`.
5. Add unit tests verifying policy gate enforcement.

## Adding an Agent Role

1. Add role identifier to `src/state_machine/agent.rs`.
2. Define role profile in `src/agent/registry/builtins.rs` with model policy, context limits, and capability envelope.
3. Add corresponding prompt template in `prompts/agents/`.
4. Register role in `RoleRegistry`.
