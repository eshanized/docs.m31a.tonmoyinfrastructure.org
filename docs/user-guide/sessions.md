# Sessions & Multi-Turn Interactions

M31A maintains durable multi-turn interactive sessions allowing developers to collaborate iteratively with the autonomous runtime.

## Session Lifecycle

Sessions are stored in the SQLite `sessions` table and track active execution runs, conversation messages, token usage, and operator preferences.

```bash
# Start a new named interactive session
m31a session new --title "Refactor Auth System"

# List existing sessions
m31a session list

# Resume a previous session
m31a session resume <SESSION_ID>

# Show conversation history and token metrics
m31a session show <SESSION_ID>
```

## Multi-Turn Context Compaction

As conversations grow, M31A's `ContextCompiler` (`src/context/compiler.rs`) monitors context window utilization against the active NVIDIA NIM model's ceiling:
1. **Headroom Reservation**: Reserves 1,536 to 4,096 tokens for tool calling definitions and final responses.
2. **Compaction Threshold**: When context reaches 80-85% capacity, older turns are compacted into semantic summaries while preserving critical file diffs and tool execution evidence.
3. **Evidence Priority Ranking**: Verification failures and compiler error diagnostics receive top priority in compiled prompt envelopes.
