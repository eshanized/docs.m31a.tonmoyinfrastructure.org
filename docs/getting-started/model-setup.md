# Model Setup & NVIDIA Credentials

M31A uses NVIDIA NIM as its exclusive production model provider.

## Obtaining Credentials

1. Visit the NVIDIA API Catalog at [build.nvidia.com](https://build.nvidia.com).
2. Sign in and generate an API key with NIM model access.
3. Your key will have the format: `nvapi-...`.

## Configuring Credentials

M31A supports three ways to configure your key, evaluated in precedence order:

### 1. Environment Variable (Recommended for CI)

```bash
export NVIDIA_API_KEY="nvapi-your-key-here"
```

### 2. User Configuration (~/.config/m31a/config.toml)

```bash
m31a config set provider.nvidia_nim.api_key "nvapi-your-key-here"
```

### 3. TUI Settings Editor

In the interactive cockpit, press `Ctrl+,` to open the Settings surface, navigate to **Provider Credentials**, enter your key, and press `Enter`. The key is masked immediately (`nvap...[MASKED]`).

## Canonical Default Model

The default model is defined in `src/config/canonical.rs`:
```toml
model = "meta/llama-3.2-11b-vision-instruct"
```

Supported NVIDIA NIM models include:
- `meta/llama-3.2-11b-vision-instruct` (Default reasoning & vision)
- `meta/llama-3.1-70b-instruct` (Heavy synthesis & architecture)
- `meta/llama-3.1-405b-instruct` (Large-scale decomposition)
- `nvidia/llama-3.1-nemotron-70b-instruct` (High-precision alignment)

To select a different model for a run:

```bash
m31a run --model "meta/llama-3.1-70b-instruct" "Refactor the authentication module"
```

In the TUI, switch models dynamically using the `/model` slash command.
