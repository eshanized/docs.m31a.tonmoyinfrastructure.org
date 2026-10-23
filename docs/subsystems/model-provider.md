# Subsystem: Model & Provider Layer

The model subsystem (`src/model/`) interfaces with language model reasoning engines.

## NVIDIA NIM Exclusivity

Production model invocation is handled exclusively by `NvidiaProvider` (`src/model/provider/nvidia.rs`), communicating via OpenAI-compatible Server-Sent Events (SSE) streaming with `https://integrate.api.nvidia.com/v1`.

### Masked Secrets
API keys are wrapped in `MaskedSecret` (`src/config/provider_registry.rs`). The raw key is exposed only when constructing HTTP `Authorization: Bearer ...` headers. In all logs, events, and TUI projections, it is masked (`nvap...[MASKED]`).
