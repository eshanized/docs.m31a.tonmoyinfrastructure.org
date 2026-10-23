# Subsystem: Context & Prompt System

Manages prompt templates, token budgeting, and context compaction (`src/context/`, `src/prompt/`).

## Dynamic Context Compilation

The `ContextCompiler` compiles prompt envelopes dynamically:
- Calculates exact token counts using tiktoken-compatible tokenizers.
- Compresses older conversation history when context exceeds 80% of model limits.
- Injects repository baseline evidence, relevant symbols, and active policy rules.
