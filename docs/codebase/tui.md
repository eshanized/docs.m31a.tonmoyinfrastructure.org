# Ratatui TUI Cockpit

> **Architectural Layer:** L9 TUI Cockpit  
> **Source Directory:** `src/tui`  
> **File Count:** 62 source files  

62-file terminal cockpit, read-only projection over SQLite, streaming, and screens.

## Module Files & Detailed Reference

| Source File | Lines | Key Types | Responsibility |
|---|:---:|---|---|
| [app.rs](#src-tui-app-rs) | 3552 | `TuiApplication` | The one TUI application root (L9 projection owner).  `TuiApplication` ... |
| [approval.rs](#src-tui-approval-rs) | 218 | `ApprovalModal, ApprovalDecision` | Interactive policy approval modal.  High importance — clearly elevated... |
| [binding.rs](#src-tui-binding-rs) | 144 | `TuiRuntimeBinding, RuntimeAssemblyOutcome` | One TUI composition boundary (Principle 2): `TuiRuntimeBinding`.  ```t... |
| [channel.rs](#src-tui-channel-rs) | 365 | `OutboxState, ActionSendError, TuiActionSender` | Bounded channel abstractions and backpressure support for TUI (Problem... |
| [badge.rs](#src-tui-component-badge-rs) | 72 | `Functions/Traits` | Quiet semantic status badges.  Color supports meaning; symbol + text c... |
| [code.rs](#src-tui-component-code-rs) | 113 | `Functions/Traits` | Bounded Code Block and Tool Output Viewer (TUI-01, TDS-02).  Enforces ... |
| [diff.rs](#src-tui-component-diff-rs) | 232 | `DiffParser, DiffStats, ParsedDiffLine` | Production-Grade Unified Diff Presentation Component (TUI-01, TDS-03, ... |
| [key_hint.rs](#src-tui-component-key_hint-rs) | 63 | `KeyHint` | Dynamic Keyboard Hint Presentation Primitives (TUI-01, TDS-01).  Provi... |
| [mod.rs](#src-tui-component-mod-rs) | 13 | `Functions/Traits` | Reusable TUI Visual Component Primitives (TUI-01, TDS-01–04). |
| [progress.rs](#src-tui-component-progress-rs) | 73 | `Functions/Traits` | Progress Bar and Visual Progress Primitives (TUI-01, TDS-02).  Provide... |
| [composer.rs](#src-tui-composer-rs) | 1965 | `AutocompleteSuggestion, FileDiscoveryReceiver, TuiComposer` | Interactive Prompt Composer Component (COP-01, CLI-01, CLI-04, D-04). ... |
| [conversation.rs](#src-tui-conversation-rs) | 1047 | `TuiConversationItem` | TUI Conversation Timeline Presentation Models (PRD §01, CLI-02, CLI-04... |
| [errors.rs](#src-tui-errors-rs) | 113 | `TuiError, TuiErrorKind` | Explicit TUI error states (Principles 10–11).  Every major runtime fai... |
| [focus.rs](#src-tui-focus-rs) | 168 | `FocusManager, FocusTarget` | Explicit Focus Management Model for TUI 2.0 (TUI-01, TDS-01).  Provide... |
| [guard.rs](#src-tui-guard-rs) | 101 | `TerminalGuard` | Terminal Guard &amp; Panic Safety Subsystem (TDS-01, TDS-02, D-10).  P... |
| [icons.rs](#src-tui-icons-rs) | 457 | `IconRegistry, Spinner, IconKey` | Semantic Nerd Font Icon System with Safe Fallback (TUI-03, D-15).  Pro... |
| [mod.rs](#src-tui-input-mod-rs) | 5 | `Functions/Traits` | Reusable text input widget (shared by composer, palette, wizard). |
| [text_input.rs](#src-tui-input-text_input-rs) | 581 | `TextInput, InputMasking, InputMode` | Zero-Dependency Reusable Text Input Component (COP-01, CFX-03, D-04, D... |
| [keymap.rs](#src-tui-keymap-rs) | 229 | `KeyContext, KeyAction` | The single input-priority authority.  Keyboard ownership is explicit a... |
| [compact.rs](#src-tui-layout-compact-rs) | 39 | `Functions/Traits` | Compact Layout (&lt;100w, 80x24 minimum).  Single column: quiet header... |
| [mod.rs](#src-tui-layout-mod-rs) | 379 | `LayoutAreas, ResponsiveLayout, WorkspaceLayoutGeometry` | Responsive Layout Classification &amp; Breakdown (TUI-02).  Classifies... |
| [wide.rs](#src-tui-layout-wide-rs) | 46 | `Functions/Traits` | Multi-Column Wide Layouts (Standard, Large, Ultra-wide).  Conversation... |
| [lifecycle.rs](#src-tui-lifecycle-rs) | 455 | `TuiLifecycleProjection, TuiLifecycleStage` | Governed lifecycle projection for the conversation-first TUI.  Pure pr... |
| [mod.rs](#src-tui-mod-rs) | 61 | `Functions/Traits` | Terminal TUI Cockpit &amp; Projection Subsystem.  Delivers the operati... |
| [model.rs](#src-tui-model-rs) | 4964 | `ExecutionHeartbeat, LiveToolOperation, TuiAgentSnapshot` | In-Memory TUI Projection ViewModel (TUI-03, D-15).  Pure in-memory pro... |
| [navigation.rs](#src-tui-navigation-rs) | 403 | `NavigationRouter, NavigationAction, RouteResolution` | Canonical Navigation &amp; Shortcut Router (TUI-01, D-16).  Maps globa... |
| [help.rs](#src-tui-overlay-help-rs) | 69 | `Functions/Traits` | Quiet contextual help overlay. |
| [manager.rs](#src-tui-overlay-manager-rs) | 51 | `OverlayManager, OverlayKind, OverlayPriority` | Priority-Aware Overlay System Manager (Section 11, TUI-01).  Enforces ... |
| [mod.rs](#src-tui-overlay-mod-rs) | 7 | `Functions/Traits` | Centralized Modal &amp; Overlay System (Section 11, TUI-01). |
| [palette_v2.rs](#src-tui-palette_v2-rs) | 679 | `PaletteItemV2, UniversalCommandPalette, PaletteActionV2` | Universal Fuzzy Command Palette V2 (COP-03, D-05, T-13-12).  Provides ... |
| [registry.rs](#src-tui-registry-rs) | 602 | `ViewMetadata, ViewRegistry, ViewId` | 40 Canonical Views Typed Registry (COP-03, D-05, UI_UX_SPEC §113).  St... |
| [replay.rs](#src-tui-replay-rs) | 266 | `ReplayController, ReplaySpeed` | Post-Mortem &amp; Checkpoint Replay Subsystem (TUI-01, D-19).  Provide... |
| [routes.rs](#src-tui-routes-rs) | 737 | `RouteContext` | Modular route composition (Principles 7–8).  Each route composes M31A'... |
| [runtime_bridge.rs](#src-tui-runtime_bridge-rs) | 2244 | `TuiRuntimeBridge` | Asynchronous Runtime Bridge for TUI Cockpit (COP-04, CLI-01, CLI-04, D... |
| [sanitizer.rs](#src-tui-sanitizer-rs) | 184 | `Functions/Traits` | Terminal Text Sanitization &amp; ANSI Escape Stripping (TUI-06, THREAT... |
| [mod.rs](#src-tui-screens-mod-rs) | 13 | `Functions/Traits` | TUI dialog screens.  Route composition lives in [`crate::tui::routes`]... |
| [wizard.rs](#src-tui-screens-wizard-rs) | 3437 | `DiscoveryReceiver, SetupWizardScreen, ProviderVerificationState` | 7-Step Guided Onboarding Setup Wizard Screen (FRX-02, FRX-03, D-02).  ... |
| [workspace_setup.rs](#src-tui-screens-workspace_setup-rs) | 1043 | `DetectedRepoContext, WorkspaceSetupScreen, GitIsolationChoice` | Focused Workspace Configuration Screen (Section 4).  Provides the cano... |
| [context_rail.rs](#src-tui-shell-context_rail-rs) | 364 | `Functions/Traits` | Contextual Right Rail for Active Session Workspace (MODE B).  Compact,... |
| [footer.rs](#src-tui-shell-footer-rs) | 135 | `Functions/Traits` | Quiet context-sensitive shell footer.  A single muted hint line. Focus... |
| [header.rs](#src-tui-shell-header-rs) | 200 | `Functions/Traits` | Quiet application shell header (conversation-first).  Shows only high-... |
| [mod.rs](#src-tui-shell-mod-rs) | 11 | `Functions/Traits` | Persistent Application Shell (Section 5, TUI-01). |
| [workspace.rs](#src-tui-shell-workspace-rs) | 1624 | `Functions/Traits` | Unified Workspace Orchestration &amp; Composition Surface (Section 5, ... |
| [state.rs](#src-tui-state-rs) | 159 | `TuiEvent` | TUI typed event flow: runtime outcomes enter presentation state throug... |
| [status.rs](#src-tui-status-rs) | 127 | `StatusPresentation, StatusKind` | 12-Status Presentation Taxonomy (TDS-04, D-03).  Provides the canonica... |
| [agents.rs](#src-tui-surface-agents-rs) | 289 | `AgentStateDisplay` | Agent Swarm &amp; Autonomous Roles Surface (Section 14, TUI-01).  Visu... |
| [artifacts.rs](#src-tui-surface-artifacts-rs) | 266 | `Functions/Traits` | Artifact Explorer &amp; Output Management Surface (Section 28, TUI-01)... |
| [conversation.rs](#src-tui-surface-conversation-rs) | 239 | `Functions/Traits` | Primary conversational execution surface (conversation-first).  Quiet,... |
| [decision.rs](#src-tui-surface-decision-rs) | 177 | `Functions/Traits` | Native interactive decision prompt surface.  Renders pending decisions... |
| [doctor.rs](#src-tui-surface-doctor-rs) | 137 | `Functions/Traits` | Doctor Diagnostics Surface (TUI-01, CLI-04).  Visualizes 6-category sy... |
| [git.rs](#src-tui-surface-git-rs) | 208 | `Functions/Traits` | Git Timeline &amp; Unstaged Diff Surface (Section 24, TUI-01).  Provid... |
| [jobs.rs](#src-tui-surface-jobs-rs) | 199 | `Functions/Traits` | Process Sandboxing &amp; Background Jobs Surface (TUI-01).  Visualizes... |
| [mod.rs](#src-tui-surface-mod-rs) | 78 | `Functions/Traits` | Contextual Application Surfaces (Section 5, 6, 12–29).  Replaces disco... |
| [model_selector.rs](#src-tui-surface-model_selector-rs) | 601 | `ModelInfo, ModelSelectorState, ProviderInfo` | Models Surface.  Renders live model provider state and allows switchin... |
| [replay.rs](#src-tui-surface-replay-rs) | 129 | `Functions/Traits` | Post-Mortem Event Replay Surface (Section 27, TUI-01, T-11-20).  Visua... |
| [settings.rs](#src-tui-surface-settings-rs) | 1506 | `SettingsRow, SettingsState, SettingsAction` | Settings surface — projection/editor of the canonical configuration sy... |
| [tasks.rs](#src-tui-surface-tasks-rs) | 334 | `Functions/Traits` | Task DAG &amp; Master-Detail Inspection Surface (Section 13, TUI-01). ... |
| [telemetry.rs](#src-tui-surface-telemetry-rs) | 162 | `Functions/Traits` | Telemetry &amp; Model Usage Surface (Section 23, TUI-01).  Provides co... |
| [tools.rs](#src-tui-surface-tools-rs) | 280 | `DisplayToolItem` | Tool &amp; Capability Telemetry Surface (Section 8, TUI-01).  Visualiz... |
| [verification.rs](#src-tui-surface-verification-rs) | 337 | `Functions/Traits` | Verification Gates &amp; Proof Evidence Surface (Section 25, TUI-01). ... |
| [workflow.rs](#src-tui-surface-workflow-rs) | 907 | `WorkflowDashboardState, WorkflowAction, WorkflowViewMode` | Workflow Visual Dashboard Surface.  Renders live workflow execution st... |
| [theme.rs](#src-tui-theme-rs) | 431 | `ThemeTokens, ThemeMode` | Centralized Theme &amp; Design Token System (TDS-03, D-03).  Provides ... |

---

### `src/tui/app.rs` {#src-tui-app-rs}

- **Source Link:** [`src/tui/app.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/app.rs)
- **Lines of Code:** 3552 (160531 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
The one TUI application root (L9 projection owner).  `TuiApplication` owns every presentation responsibility: UI state, runtime binding, routing, input, transient UI, and rendering. Enforces Law 9: "The TUI is a projection, never authoritative state." Features dirty-state frame scheduling (30–60 FPS), sub-5ms render budget, bounded update consumption, and zero database queries during draw.  Construction is synchronous and runtime-free: `new()` builds a valid engine, `with_runtime_startup()` arms the production startup state, the first frame draws before any runtime await, and the canonical `AppRuntime` (assembled by the real composition root in `main.rs`) attaches later via the binding. Events flow `runtime → bridge → TuiEvent → apply_tui_event → render`; `render` performs zero I/O and never touches the runtime.

#### Types & Trait Declarations
- **Structs (1):** `TuiApplication`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn with_runtime_startup(self,
        workspace_root: PathBuf,
        config: &crate::config::ResolvedConfiguration,) -;
// pub
fn with_interaction_rx(mut self, rx: impl Into<TuiInteractionReceiver>) -> Self;
// pub
fn with_bridge_tx(mut self, tx: impl Into<TuiActionSender>) -> Self;
// private
fn send_or_fail(&mut self, op: &str, action: ApplicationAction) -> bool;
// pub
fn retry_quarantine_refresh(&mut self) -> bool;
// pub
fn retry_catalog_refresh(&mut self) -> bool;
// private
fn handle_quarantine_key(&mut self, key: KeyEvent, is_modal: bool) -> Option<RuntimeCommand>;
// pub
fn has_context_panel(&self) -> bool;
// pub
fn normalize_focus(&mut self);
// pub
fn normalize_context_rail_state(&mut self);
// pub
fn set_terminal_size(&mut self, width: u16, height: u16);
// pub
fn handle_resize(&mut self, width: u16, height: u16);
// pub
fn handle_mouse_scroll(&mut self, up: bool);
```

---

### `src/tui/approval.rs` {#src-tui-approval-rs}

- **Source Link:** [`src/tui/approval.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/approval.rs)
- **Lines of Code:** 218 (7364 bytes)

#### Primary Responsibility
Interactive policy approval modal.  High importance — clearly elevated — but professional, not cyberpunk. Keys: y/Enter approve once, a approve always, n reject, Esc dismiss. Behavior preserved; only presentation rebuilt.

#### Types & Trait Declarations
- **Structs (1):** `ApprovalModal`
- **Enums (1):** `ApprovalDecision`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn new() -> Self;
// pub
fn open(&mut self, request: TuiApprovalRequest);
// pub
fn close(&mut self);
// pub
fn handle_key(&mut self, key: KeyEvent) -> Option<ApprovalDecision>;
// pub
fn render(&self, f: &mut Frame, area: Rect);
// pub
fn render_with_theme(&self, f: &mut Frame, area: Rect, tokens: &ThemeTokens);
// private
fn truncate(s: &str, max: usize) -> String;
// private
fn centered_approval_rect(percent_x: u16, percent_y: u16, r: Rect) -> Rect;
```

---

### `src/tui/binding.rs` {#src-tui-binding-rs}

- **Source Link:** [`src/tui/binding.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/binding.rs)
- **Lines of Code:** 144 (4764 bytes)

#### Primary Responsibility
One TUI composition boundary (Principle 2): `TuiRuntimeBinding`.  ```text AppRuntime → TuiRuntimeBinding → TuiApplication → state/routing/input/render ```  The binding consumes the canonical `AppRuntime` (built once by the real composition root). It never constructs a production runtime or any production authority (capability/tool registries, pipeline, policy, approvals, artifacts, model caller, context compiler, auth, git, jobs). It owns only channels and task handles: the bridge sender, the interaction receiver, and the bridge supervisor handle.

#### Types & Trait Declarations
- **Structs (1):** `TuiRuntimeBinding`
- **Enums (1):** `RuntimeAssemblyOutcome`

#### Key Functions & Signatures (12 shown)
```rust
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn has_runtime(&self) -> bool;
// pub
fn has_bridge(&self) -> bool;
// pub
fn runtime(&self) -> Option<Arc<AppRuntime>>;
// pub
fn last_error(&self) -> Option<&TuiError>;
// pub
fn bridge_sender(&self) -> Option<TuiActionSender>;
// pub
fn take_interaction_receiver(&mut self) -> Option<TuiInteractionReceiver>;
// pub
async fn attach_runtime(&mut self,
        runtime: Arc<AppRuntime>,
        resume_session_id: Option<SessionId>,) -> R;
// pub
fn record_failure(&mut self, error: TuiError);
// pub
fn poll_bridge_supervision(&mut self) -> Option<TuiError>;
// private
fn binding_starts_empty_and_records_failures_visibly();
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`binding_starts_empty_and_records_failures_visibly`

---

### `src/tui/channel.rs` {#src-tui-channel-rs}

- **Source Link:** [`src/tui/channel.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/channel.rs)
- **Lines of Code:** 365 (13728 bytes)

#### Primary Responsibility
Bounded channel abstractions and backpressure support for TUI (Problem 7).  Provides `TuiActionSender` and `TuiInteractionReceiver` supporting both bounded channels (production default) and unbounded channels (for test compatibility).

#### Types & Trait Declarations
- **Structs (1):** `OutboxState`
- **Enums (4):** `ActionSendError`, `TuiActionSender`, `TuiInteractionReceiver`, `TuiInteractionSender`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn try_send(&self, action: ApplicationAction) -> Result<(), ActionSendError>;
// pub
fn send(&self, action: ApplicationAction) -> Result<(), ActionSendError>;
// pub
fn is_closed(&self) -> bool;
// private
fn from(s: mpsc::Sender<ApplicationAction>) -> Self;
// private
fn from(s: mpsc::UnboundedSender<ApplicationAction>) -> Self;
// pub
fn try_recv(&mut self) -> Result<InteractionEvent, TryRecvError>;
// pub
async fn recv(&mut self) -> Option<InteractionEvent>;
// private
fn from(r: mpsc::Receiver<InteractionEvent>) -> Self;
// private
fn from(r: mpsc::UnboundedReceiver<InteractionEvent>) -> Self;
// private
fn is_terminal_or_approval(event: &InteractionEvent) -> bool;
// pub
fn push_critical(&mut self, event: InteractionEvent) -> Result<(), ActionSendError>;
// private
fn log_saturation_warning(&mut self);
// pub
fn try_send(&self, event: InteractionEvent) -> Result<(), ActionSendError>;
// pub
fn flush_outbox(&self);
```

---

### `src/tui/component/badge.rs` {#src-tui-component-badge-rs}

- **Source Link:** [`src/tui/component/badge.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/component/badge.rs)
- **Lines of Code:** 72 (2566 bytes)

#### Primary Responsibility
Quiet semantic status badges.  Color supports meaning; symbol + text carries it. No emoji blocks.

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn render_status_badge(status: StatusKind, tokens: &ThemeTokens) -> Vec<Span<'a>>;
// pub
fn render_risk_badge(risk: &str, tokens: &ThemeTokens) -> Span<'a>;
// pub
fn render_agent_tag(role: &str, tokens: &ThemeTokens) -> Span<'a>;
// pub
fn render_key_chip(key: &str, tokens: &ThemeTokens) -> Span<'a>;
// pub
fn format_key_hints_placeholder() -> Style;
```

---

### `src/tui/component/code.rs` {#src-tui-component-code-rs}

- **Source Link:** [`src/tui/component/code.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/component/code.rs)
- **Lines of Code:** 113 (4146 bytes)

#### Primary Responsibility
Bounded Code Block and Tool Output Viewer (TUI-01, TDS-02).  Enforces Law 5 and Section 8/28: Large outputs (up to 500MB) must never flood the framebuffer or block the render path. Provides clean truncation, artifact locator citations, and structured terminal styling.

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn render_bounded_output(content: &str,
    max_lines: usize,
    width: u16,
    artifact_id: Option<&str>,
    tokens:;
```

---

### `src/tui/component/diff.rs` {#src-tui-component-diff-rs}

- **Source Link:** [`src/tui/component/diff.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/component/diff.rs)
- **Lines of Code:** 232 (8452 bytes)

#### Primary Responsibility
Production-Grade Unified Diff Presentation Component (TUI-01, TDS-03, Section 24).  Parses and renders unified diffs with syntax coloring, line numbers, hunk headers, file attribution, and addition/deletion telemetry.

#### Types & Trait Declarations
- **Structs (3):** `DiffParser`, `DiffStats`, `ParsedDiffLine`
- **Enums (1):** `DiffLineType`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn parse(diff_text: &str) -> (Vec<ParsedDiffLine>, DiffStats);
// private
fn parse_hunk_indices(header: &str) -> (usize, usize);
// pub
fn render_diff_lines(parsed_lines: &[ParsedDiffLine],
    width: u16,
    tokens: &ThemeTokens,) -> Vec<Line<'a>>;
// private
fn truncate_str(s: &str, max: u16) -> String;
```

---

### `src/tui/component/key_hint.rs` {#src-tui-component-key_hint-rs}

- **Source Link:** [`src/tui/component/key_hint.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/component/key_hint.rs)
- **Lines of Code:** 63 (1900 bytes)

#### Primary Responsibility
Dynamic Keyboard Hint Presentation Primitives (TUI-01, TDS-01).  Provides responsive footer keybindings and contextual command hints.

#### Types & Trait Declarations
- **Structs (1):** `KeyHint`

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn format_key_hints(hints: &[KeyHint], max_width: u16, tokens: &ThemeTokens) -> Line<'a>;
```

---

### `src/tui/component/mod.rs` {#src-tui-component-mod-rs}

- **Source Link:** [`src/tui/component/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/component/mod.rs)
- **Lines of Code:** 13 (462 bytes)

#### Primary Responsibility
Reusable TUI Visual Component Primitives (TUI-01, TDS-01–04).

---

### `src/tui/component/progress.rs` {#src-tui-component-progress-rs}

- **Source Link:** [`src/tui/component/progress.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/component/progress.rs)
- **Lines of Code:** 73 (2136 bytes)

#### Primary Responsibility
Progress Bar and Visual Progress Primitives (TUI-01, TDS-02).  Provides dense, high-clarity progress bars and metrics for task DAG, verification pipelines, and job execution.

#### Key Functions & Signatures (2 shown)
```rust
// pub
fn format_progress_bar(percentage: u8, width: usize) -> String;
// pub
fn render_progress_line(label: &str,
    percentage: u8,
    width: u16,
    tokens: &ThemeTokens,) -> Line<'a>;
```

---

### `src/tui/composer.rs` {#src-tui-composer-rs}

- **Source Link:** [`src/tui/composer.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/composer.rs)
- **Lines of Code:** 1965 (75527 bytes)

#### Primary Responsibility
Interactive Prompt Composer Component (COP-01, CLI-01, CLI-04, D-04).  Provides the primary operator input surface for the M31A Cockpit: - Natural language prompt composition with full Unicode support - Multiline editing with block quotes (`"""`) and line continuation (`\`) - Centralized slash command autocomplete popup (sourced from `SlashCommandRegistry`) - Real-time `@file` and `@directory` mention autocompletion - Input history navigation (Up/Down traversal) - Clean rendering with zero DB/filesystem I/O during draw

#### Types & Trait Declarations
- **Structs (3):** `AutocompleteSuggestion`, `FileDiscoveryReceiver`, `TuiComposer`
- **Enums (3):** `AutocompleteKind`, `ComposerAction`, `FileDiscoveryState`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn is_loading(&self) -> bool;
// pub
fn is_ready(&self) -> bool;
// pub
fn is_failed(&self) -> bool;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn default() -> Self;
// pub
fn new(workspace_root: PathBuf) -> Self;
// pub
fn with_cached_models(mut self, models: Vec<(String, String);
// pub
fn with_cached_files(mut self, files: Vec<String>) -> Self;
// pub
fn set_workspace_root(&mut self, root: PathBuf);
// pub
fn file_discovery_state(&self) -> &FileDiscoveryState;
// pub
fn spawn_file_discovery(&mut self);
// pub
fn poll_file_discovery(&mut self) -> bool;
// pub
fn apply_file_discovery_result(&mut self,
        scan_id: u64,
        result: Result<Vec<String>, String>,) -> bool;
// pub
fn cancel_file_discovery(&mut self);
```

#### Unit Verification (10 inline tests)
Tests defined within module:
`test_composer_basic_input_and_submit`, `test_composer_slash_autocomplete_trigger`, `test_composer_history_navigation`, `test_composer_model_autocomplete_empty_catalog_has_no_synthetic_fallback`, `test_composer_model_autocomplete_populates_from_catalog`, `test_composer_file_autocomplete_first_use_is_non_blocking_and_async`, `test_composer_file_autocomplete_empty_workspace`, `test_composer_file_autocomplete_failed_worker_reports_diagnostic`, `test_composer_file_autocomplete_workspace_switch_cancels_and_resets`, `test_composer_file_autocomplete_stale_scan_result_discarded`

---

### `src/tui/conversation.rs` {#src-tui-conversation-rs}

- **Source Link:** [`src/tui/conversation.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/conversation.rs)
- **Lines of Code:** 1047 (39187 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
TUI Conversation Timeline Presentation Models (PRD §01, CLI-02, CLI-04).  Provides strongly typed, human-readable presentation models for the live interactive conversation stream: - User prompts with @mention badges - Assistant reasoning and model responses - Real-time tool invocations and structured results - Verification gate proofs and summaries - Policy approval escalation prompts and resolutions - System lifecycle events and error reporting  Enforces: - Semantic badges (`[USER]`, `[ASST]`, `[TOOL]`, `[VERIFY]`, `[ASK]`, `[ERR]`, `[SYS]`) - Secret scrubbing and terminal escape sanitization - Theme-aware rendering honoring `NO_COLOR` - Non-color semantic status encoding

#### Types & Trait Declarations
- **Enums (1):** `TuiConversationItem`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn badge(&self) -> &'static str;
// pub
fn icon_key(&self) -> IconKey;
// pub
fn render_lines_with_icons(&'a self,
        max_width: u16,
        tokens: &ThemeTokens,
        _icons: &IconRegistry;
// pub
fn timestamp(&self) -> DateTime<Utc>;
// pub
fn from_turn(turn: &ConversationTurn) -> Self;
// pub
fn content_width(area_width: u16) -> usize;
// pub
fn render_lines(&self, width: u16, tokens: &ThemeTokens) -> Vec<Line<'static>>;
// private
fn truncate_to_width(s: &str, width: usize) -> String;
// private
fn wrap_conversation_text(text: &str,
    width: usize,
    style: ratatui::style::Style,) -> Vec<Line<'static>>;
// private
fn wrap_prefixed(prefix: &str,
    text: &str,
    width: usize,
    style: ratatui::style::Style,) -> Vec<Line<'static>;
// private
fn render_command_output_text(text: &str,
    width: usize,
    tokens: &ThemeTokens,) -> Vec<Line<'static>>;
```

---

### `src/tui/errors.rs` {#src-tui-errors-rs}

- **Source Link:** [`src/tui/errors.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/errors.rs)
- **Lines of Code:** 113 (3395 bytes)

#### Primary Responsibility
Explicit TUI error states (Principles 10–11).  Every major runtime failure becomes visible TUI state. The renderer never silently returns an empty frame: failures are typed, carry a human-readable message, and render through the normal shell (header / startup panel / composer / footer).  M31A visual identity is unchanged; this module only classifies failures so the startup panel and notifications can explain *what* failed.

#### Types & Trait Declarations
- **Structs (1):** `TuiError`
- **Enums (1):** `TuiErrorKind`

#### Key Functions & Signatures (12 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn title(&self) -> &'static str;
// pub
fn new(kind: TuiErrorKind, message: impl Into<String>) -> Self;
// pub
fn runtime(message: impl Into<String>) -> Self;
// pub
fn bridge(message: impl Into<String>) -> Self;
// pub
fn hydration(message: impl Into<String>) -> Self;
// pub
fn model(message: impl Into<String>) -> Self;
// pub
fn workspace(message: impl Into<String>) -> Self;
// pub
fn display(&self) -> String;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn error_display_prefixes_kind_title();
// private
fn kinds_have_stable_ids();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`error_display_prefixes_kind_title`, `kinds_have_stable_ids`

---

### `src/tui/focus.rs` {#src-tui-focus-rs}

- **Source Link:** [`src/tui/focus.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/focus.rs)
- **Lines of Code:** 168 (5154 bytes)

#### Primary Responsibility
Explicit Focus Management Model for TUI 2.0 (TUI-01, TDS-01).  Provides single-source-of-truth focus ownership across: - Composer: Input editor for natural language and slash commands - Conversation: Main execution stream (scrollable, interactive items) - ContextPanel: Master/detail side surface (tasks, agents, tools, diff, etc.) - Overlay: Modals, Command Palette, Help, Approval dialogs

#### Types & Trait Declarations
- **Structs (1):** `FocusManager`
- **Enums (1):** `FocusTarget`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn is_composer(&self) -> bool;
// pub
fn is_conversation(&self) -> bool;
// pub
fn is_context_panel(&self) -> bool;
// pub
fn is_settings(&self) -> bool;
// pub
fn is_overlay(&self) -> bool;
// pub
fn new(initial: FocusTarget) -> Self;
// pub
fn current(&self) -> FocusTarget;
// pub
fn set_focus(&mut self, target: FocusTarget);
// pub
fn focus_composer(&mut self);
// pub
fn unfocus_composer(&mut self);
// pub
fn enter_overlay(&mut self);
// pub
fn exit_overlay(&mut self);
// pub
fn enter_settings(&mut self);
// pub
fn exit_settings(&mut self);
```

---

### `src/tui/guard.rs` {#src-tui-guard-rs}

- **Source Link:** [`src/tui/guard.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/guard.rs)
- **Lines of Code:** 101 (3159 bytes)

#### Primary Responsibility
Terminal Guard &amp; Panic Safety Subsystem (TDS-01, TDS-02, D-10).  Provides RAII-based terminal mode management and global panic restoration hooks. Ensures that regardless of exit status (normal exit, error, panic, or signal), the terminal's raw mode, alternate screen buffer, mouse capture, and cursor visibility are completely and idempotently restored.

#### Types & Trait Declarations
- **Structs (1):** `TerminalGuard`

#### Key Functions & Signatures (8 shown)
```rust
// pub
fn acquire() -> io::Result<Self>;
// pub
fn restore(&mut self) -> io::Result<()>;
// pub
fn emergency_restore() -> io::Result<()>;
// pub
fn is_active(&self) -> bool;
// private
fn drop(&mut self);
// pub
fn install_panic_hook();
// private
fn test_panic_hook_installation_is_idempotent();
// private
fn test_guard_emergency_restore_idempotency();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_panic_hook_installation_is_idempotent`, `test_guard_emergency_restore_idempotency`

---

### `src/tui/icons.rs` {#src-tui-icons-rs}

- **Source Link:** [`src/tui/icons.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/icons.rs)
- **Lines of Code:** 457 (15312 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Semantic Nerd Font Icon System with Safe Fallback (TUI-03, D-15).  Provides a single canonical icon registry used by all TUI rendering. Never scatters raw icon literals throughout the code. Supports Nerd Font mode and a safe ASCII/Unicode fallback so the TUI remains readable on: - Nerd Font terminal - normal Unicode terminal - restricted ANSI terminal

#### Types & Trait Declarations
- **Structs (2):** `IconRegistry`, `Spinner`
- **Enums (2):** `IconKey`, `IconMode`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn detect(theme_mode: ThemeMode) -> Self;
// pub
fn new(mode: IconMode) -> Self;
// pub
fn from_theme(theme_mode: ThemeMode) -> Self;
// pub
fn mode(&self) -> IconMode;
// pub
fn get(&self, key: IconKey) -> &'static str;
// pub
fn new() -> Self;
// pub
fn nerd_font() -> Self;
// pub
fn ascii() -> Self;
// pub
fn for_mode(mode: IconMode) -> Self;
// pub
fn tick(&mut self) -> &'static str;
// pub
fn current(&self) -> &'static str;
// pub
fn reset(&mut self);
// private
fn default() -> Self;
// private
fn test_icon_modes_produce_output();
// private
fn test_spinner_cycles();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_icon_modes_produce_output`, `test_spinner_cycles`

---

### `src/tui/input/mod.rs` {#src-tui-input-mod-rs}

- **Source Link:** [`src/tui/input/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/input/mod.rs)
- **Lines of Code:** 5 (150 bytes)

#### Primary Responsibility
Reusable text input widget (shared by composer, palette, wizard).

---

### `src/tui/input/text_input.rs` {#src-tui-input-text_input-rs}

- **Source Link:** [`src/tui/input/text_input.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/input/text_input.rs)
- **Lines of Code:** 581 (17969 bytes)

#### Primary Responsibility
Zero-Dependency Reusable Text Input Component (COP-01, CFX-03, D-04, D-08).  Provides Unicode-safe cursor navigation, single-line and multiline editing, history navigation, word boundary traversal, and secret masking.

#### Types & Trait Declarations
- **Structs (1):** `TextInput`
- **Enums (2):** `InputMasking`, `InputMode`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn default() -> Self;
// pub
fn new(mode: InputMode) -> Self;
// pub
fn single_line() -> Self;
// pub
fn multi_line() -> Self;
// pub
fn set_mode(&mut self, mode: InputMode);
// pub
fn with_placeholder(mut self, placeholder: impl Into<String>) -> Self;
// pub
fn with_masking(mut self, masking: InputMasking) -> Self;
// pub
fn with_max_length(mut self, max: usize) -> Self;
// pub
fn value(&self) -> &str;
// pub
fn text(&self) -> &str;
// pub
fn set_value(&mut self, val: &str);
// pub
fn set_text(&mut self, val: &str);
// pub
fn handle_key(&mut self, key: crossterm::event::KeyEvent) -> bool;
// pub
fn clear(&mut self);
// pub
fn char_count(&self) -> usize;
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_text_input_unicode_and_editing`, `test_text_input_secret_masking`

---

### `src/tui/keymap.rs` {#src-tui-keymap-rs}

- **Source Link:** [`src/tui/keymap.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/keymap.rs)
- **Lines of Code:** 229 (7271 bytes)

#### Primary Responsibility
The single input-priority authority.  Keyboard ownership is explicit and tested here:  ```text replay → dialog → palette → help → wizard → palette-chord → interrupt → composer → route → global ```  This module classifies keys; it never executes domain actions. Execution lives in `TuiApplication::handle_*_key`, which consumes every classification — no result is discarded and no second matcher exists.

#### Types & Trait Declarations
- **Structs (1):** `KeyContext`
- **Enums (1):** `KeyAction`

#### Key Functions & Signatures (13 shown)
```rust
// pub
fn new(replay_active: bool,
        dialog_open: bool,
        palette_open: bool,
        help_open: bool,
        wiza;
// pub
fn with_decision(mut self, decision_pending: bool) -> Self;
// pub
fn resolve_key(key: KeyEvent, ctx: KeyContext) -> KeyAction;
// private
fn is_palette_chord(key: KeyEvent, composer_focused: bool) -> bool;
// private
fn is_exit_chord(key: KeyEvent) -> bool;
// private
fn key(code: KeyCode) -> KeyEvent;
// private
fn ctrl(code: KeyCode) -> KeyEvent;
// private
fn priority_dialog_over_everything();
// private
fn transient_owners_beat_composer_and_route();
// private
fn ctrl_p_opens_palette_from_composer_and_route();
// private
fn colon_types_in_composer_but_opens_palette_on_route();
// private
fn ctrl_c_is_exit_chord_before_composer();
// private
fn replay_locks_all_keys();
```

#### Unit Verification (6 inline tests)
Tests defined within module:
`priority_dialog_over_everything`, `transient_owners_beat_composer_and_route`, `ctrl_p_opens_palette_from_composer_and_route`, `colon_types_in_composer_but_opens_palette_on_route`, `ctrl_c_is_exit_chord_before_composer`, `replay_locks_all_keys`

---

### `src/tui/layout/compact.rs` {#src-tui-layout-compact-rs}

- **Source Link:** [`src/tui/layout/compact.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/layout/compact.rs)
- **Lines of Code:** 39 (1165 bytes)

#### Primary Responsibility
Compact Layout (&lt;100w, 80x24 minimum).  Single column: quiet header, conversation, composer, minimal footer. No sidebar, no telemetry, no dashboard.

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn compute_compact_layout(area: Rect) -> LayoutAreas;
```

---

### `src/tui/layout/mod.rs` {#src-tui-layout-mod-rs}

- **Source Link:** [`src/tui/layout/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/layout/mod.rs)
- **Lines of Code:** 379 (13049 bytes)

#### Primary Responsibility
Responsive Layout Classification &amp; Breakdown (TUI-02).  Classifies terminal dimensions into 4 tiers: - Compact (&lt;100w): Single-column stacked layout with tabbed pane switching; optimized for 80x24. - Standard (100–159w): Dual-column layout (sidebar + main cockpit). - Large (160–219w): Three-column layout (nav sidebar + cockpit + telemetry). - UltraWide (&gt;=220w): Full wide-screen layout with expanded inspector panes.

#### Types & Trait Declarations
- **Structs (3):** `LayoutAreas`, `ResponsiveLayout`, `WorkspaceLayoutGeometry`
- **Enums (2):** `LayoutTier`, `ScrollTargetPane`

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn from_dimensions(width: u16, height: u16) -> Self;
// pub
fn is_below_minimum(width: u16, height: u16) -> bool;
// pub
fn as_str(&self) -> &'static str;
// pub
fn classify_terminal_size(width: u16, height: u16) -> LayoutTier;
// pub
fn partition(area: Rect) -> (LayoutTier, LayoutAreas);
// pub
fn split_vertical_chrome(area: Rect) -> (Rect, Rect, Rect);
// pub
fn compute_layout(area: Rect) -> (LayoutTier, LayoutAreas);
// pub
fn target_pane_at(&self, col: u16, row: u16) -> Option<ScrollTargetPane>;
// pub
fn rect_contains(rect: Rect, col: u16, row: u16) -> bool;
// pub
fn compute_workspace_layout_geometry(terminal: Rect,
    screen: crate::tui::navigation::ScreenId,
    has_modal_or_over;
```

---

### `src/tui/layout/wide.rs` {#src-tui-layout-wide-rs}

- **Source Link:** [`src/tui/layout/wide.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/layout/wide.rs)
- **Lines of Code:** 46 (1549 bytes)

#### Primary Responsibility
Multi-Column Wide Layouts (Standard, Large, Ultra-wide).  Conversation-first: the conversation always dominates. Wide viewports add a modest contextual inspector only when explicitly requested via navigation detail — never a permanent telemetry sidebar by default. `sidebar`/`telemetry` rects are therefore None unless the caller opens a detail; the workspace renders conversation full-width.

#### Key Functions & Signatures (4 shown)
```rust
// private
fn compute_wide_layout(area: Rect) -> LayoutAreas;
// pub
fn compute_standard_layout(area: Rect) -> LayoutAreas;
// pub
fn compute_large_layout(area: Rect) -> LayoutAreas;
// pub
fn compute_ultrawide_layout(area: Rect) -> LayoutAreas;
```

---

### `src/tui/lifecycle.rs` {#src-tui-lifecycle-rs}

- **Source Link:** [`src/tui/lifecycle.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/lifecycle.rs)
- **Lines of Code:** 455 (18183 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Governed lifecycle projection for the conversation-first TUI.  Pure presentation projection over the canonical M31A runtime lifecycle. This module never executes tools, never mutates workspace state, never authorizes execution, and never writes to the database. It only derives renderable lifecycle state from trusted runtime events.  Authority order: persisted `LifecycleStage` &gt; runtime `EventType` &gt; `InteractionEvent` summaries. UI-only guesses are never invented here.

#### Types & Trait Declarations
- **Structs (1):** `TuiLifecycleProjection`
- **Enums (1):** `TuiLifecycleStage`

#### Key Functions & Signatures (14 shown)
```rust
// pub
fn label(&self) -> &'static str;
// pub
fn bracket_label(&self) -> String;
// pub
fn is_terminal(&self) -> bool;
// pub
fn is_governance_gate(&self) -> bool;
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn select_next_option(&mut self);
// pub
fn select_prev_option(&mut self);
// pub
fn selected_option(&self) -> Option<&str>;
// pub
fn short_hash(hash: &str) -> String;
// private
fn touch(&mut self);
// private
fn sealed(&self) -> bool;
// pub
fn apply_lifecycle_stage(&mut self,
        state: &crate::persistence::sqlite::repositories::lifecycle::PersistedLifecy;
// pub
fn apply_event(&mut self, event: &EventEnvelope);
```

---

### `src/tui/mod.rs` {#src-tui-mod-rs}

- **Source Link:** [`src/tui/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/mod.rs)
- **Lines of Code:** 61 (1862 bytes)

#### Primary Responsibility
Terminal TUI Cockpit &amp; Projection Subsystem.  Delivers the operational cockpit. Enforces Law 9: "The TUI is a projection, never authoritative state."  Public surface is deliberately small: the application root, the runtime binding, the event reducer, the navigation authority, and the primitives the binary and integration tests drive directly. Everything else is reached through its module path (`tui::model::TuiViewModel`, …).

---

### `src/tui/model.rs` {#src-tui-model-rs}

- **Source Link:** [`src/tui/model.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/model.rs)
- **Lines of Code:** 4964 (200157 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
In-Memory TUI Projection ViewModel (TUI-03, D-15).  Pure in-memory projection of runtime state. Never executes SQLite queries or synchronous I/O during rendering.

#### Types & Trait Declarations
- **Structs (22):** `ExecutionHeartbeat`, `LiveToolOperation`, `TuiAgentSnapshot`, `TuiApprovalRequest`, `TuiArtifactSnapshot`, `TuiDoctorCheck`, `TuiJobSnapshot`, `TuiLogLine`, `TuiModelUsage`, `TuiQuarantineItem`, `TuiRecoverySnapshot`, `TuiSandboxStatus`, `TuiSkillSnapshot`, `TuiSystemStats`, `TuiTaskSnapshot`, `TuiTimelineEntry`, `TuiToolDefinitionSnapshot`, `TuiToolSnapshot`, `TuiTraceabilityChain`, `TuiVerificationCheck`, `TuiVerificationSummary`, `TuiViewModel`
- **Enums (10):** `ActivityKind`, `DoctorStatus`, `LiveToolState`, `QuarantineProjectionState`, `RuntimeStartupState`, `SectionProjectionState`, `SessionViewMode`, `TaskGraphProjectionState`, `TuiCredentialStatus`, `UiOperationState`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn is_ready(&self) -> bool;
// pub
fn is_failed(&self) -> bool;
// pub
fn is_startup(&self) -> bool;
// pub
fn label(&self) -> String;
// pub
fn failure_reason(&self) -> Option<&str>;
// pub
fn is_welcome(&self) -> bool;
// pub
fn is_active(&self) -> bool;
// pub
fn is_closed(&self) -> bool;
// pub
fn is_working(&self) -> bool;
// pub
fn is_waiting(&self) -> bool;
// pub
fn icon_key(&self) -> crate::tui::icons::IconKey;
// private
fn default() -> Self;
// pub
fn new(id: impl Into<String>,
        title: impl Into<String>,
        status: impl Into<String>,
        agent_role: O;
// pub
fn effective_prompt_tokens(&self) -> u64;
// pub
fn effective_completion_tokens(&self) -> u64;
```

---

### `src/tui/navigation.rs` {#src-tui-navigation-rs}

- **Source Link:** [`src/tui/navigation.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/navigation.rs)
- **Lines of Code:** 403 (14254 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Canonical Navigation &amp; Shortcut Router (TUI-01, D-16).  Maps global canonical keyboard shortcuts: - `1`–`0`: Primary operational screens (Dashboard, Mission, Task Graph, Agents, Tools, Jobs, Verification, Git, Approvals, Doctor) - `l`, `m`, `a`, `r`, `?`: Auxiliary screens (Logs, Model, Artifacts, Replay, Help) - `Ctrl+P` or `:`: Open universal fuzzy Command Palette - `Esc`: Pop navigation history stack or close overlay

#### Types & Trait Declarations
- **Structs (1):** `NavigationRouter`
- **Enums (3):** `NavigationAction`, `RouteResolution`, `ScreenId`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn title(&self) -> &'static str;
// pub
fn title_with_shortcut(&self) -> &'static str;
// pub
fn shortcut(&self) -> &'static str;
// pub
fn canonical_screen(view: ViewId) -> ScreenId;
// pub
fn resolve_view(view: ViewId) -> RouteResolution;
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn navigate_to_view(&mut self, view: ViewId);
// pub
fn open_modal(&mut self, modal: ViewId);
// pub
fn close_modal(&mut self);
// pub
fn open_detail(&mut self, detail: ViewId);
// pub
fn close_detail(&mut self);
// pub
fn open_overlay(&mut self, overlay: ViewId);
// pub
fn close_overlay(&mut self);
// pub
fn navigate_to(&mut self, target: ScreenId);
```

---

### `src/tui/overlay/help.rs` {#src-tui-overlay-help-rs}

- **Source Link:** [`src/tui/overlay/help.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/overlay/help.rs)
- **Lines of Code:** 69 (2290 bytes)

#### Primary Responsibility
Quiet contextual help overlay.

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn render_help_overlay(f: &mut Frame, area: Rect, tokens: &ThemeTokens);
```

---

### `src/tui/overlay/manager.rs` {#src-tui-overlay-manager-rs}

- **Source Link:** [`src/tui/overlay/manager.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/overlay/manager.rs)
- **Lines of Code:** 51 (1277 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Priority-Aware Overlay System Manager (Section 11, TUI-01).  Enforces centralized modal and overlay priority: 1. Critical Policy Approval (highest priority - owns input until resolved) 2. Universal Command Palette (Ctrl+P / :) 3. Contextual Help Dialog (?)

#### Types & Trait Declarations
- **Structs (1):** `OverlayManager`
- **Enums (2):** `OverlayKind`, `OverlayPriority`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn new() -> Self;
// pub
fn open_help(&mut self);
// pub
fn close_help(&mut self);
// pub
fn toggle_help(&mut self);
```

---

### `src/tui/overlay/mod.rs` {#src-tui-overlay-mod-rs}

- **Source Link:** [`src/tui/overlay/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/overlay/mod.rs)
- **Lines of Code:** 7 (194 bytes)

#### Primary Responsibility
Centralized Modal &amp; Overlay System (Section 11, TUI-01).

---

### `src/tui/palette_v2.rs` {#src-tui-palette_v2-rs}

- **Source Link:** [`src/tui/palette_v2.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/palette_v2.rs)
- **Lines of Code:** 679 (23168 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Universal Fuzzy Command Palette V2 (COP-03, D-05, T-13-12).  Provides instant navigation across all 40 canonical views, active mission entities, and runtime commands via fuzzy search (SkimMatcherV2) with credential masking.

#### Types & Trait Declarations
- **Structs (2):** `PaletteItemV2`, `UniversalCommandPalette`
- **Enums (1):** `PaletteActionV2`

#### Key Functions & Signatures (15 shown)
```rust
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn register_all_commands(&mut self);
// pub
fn register_slash_commands(&mut self,
        slash_registry: &crate::interaction::commands::SlashCommandRegistry,);
// pub
fn with_slash_registry(mut self,
        slash_registry: &crate::interaction::commands::SlashCommandRegistry,) -> Self;
// pub
fn items(&self) -> &[PaletteItemV2];
// pub
fn is_open(&self) -> bool;
// pub
fn open(&mut self);
// pub
fn close(&mut self);
// pub
fn query(&self) -> &str;
// pub
fn set_query(&mut self, query: &str);
// pub
fn selected_item(&self) -> Option<&PaletteItemV2>;
// pub
fn select_next(&mut self);
// pub
fn select_prev(&mut self);
```

---

### `src/tui/registry.rs` {#src-tui-registry-rs}

- **Source Link:** [`src/tui/registry.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/registry.rs)
- **Lines of Code:** 602 (17132 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
40 Canonical Views Typed Registry (COP-03, D-05, UI_UX_SPEC §113).  Strongly typed registry cataloging all 40 canonical operational views with identity, numeric code (1–40), classification kind, shortcut hotkey, and URL/route path.

#### Types & Trait Declarations
- **Structs (2):** `ViewMetadata`, `ViewRegistry`
- **Enums (2):** `ViewId`, `ViewKind`

#### Key Functions & Signatures (12 shown)
```rust
// pub
fn number(&self) -> u8;
// pub
fn all() -> &'static [ViewId];
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn len(&self) -> usize;
// pub
fn is_empty(&self) -> bool;
// pub
fn get(&self, id: ViewId) -> Option<&ViewMetadata>;
// pub
fn get_by_number(&self, number: u8) -> Option<&ViewMetadata>;
// pub
fn get_by_route(&self, route: &str) -> Option<&ViewMetadata>;
// pub
fn get_by_hotkey(&self, hotkey: char) -> Option<&ViewMetadata>;
// pub
fn find_by_name(&self, query: &str) -> Vec<&ViewMetadata>;
// pub
fn all(&self) -> Vec<&ViewMetadata>;
```

---

### `src/tui/replay.rs` {#src-tui-replay-rs}

- **Source Link:** [`src/tui/replay.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/replay.rs)
- **Lines of Code:** 266 (8472 bytes)

#### Primary Responsibility
Post-Mortem &amp; Checkpoint Replay Subsystem (TUI-01, D-19).  Provides read-only historical execution scrub through event and checkpoint timelines: - `[`: Step backward 1 event - `]`: Step forward 1 event - `Space`: Play / Pause timeline playback - `1` / `2` / `4`: Select scrub playback speed (1x, 2x, 4x) - `Esc`: Exit Replay mode  Strictly enforces D-19 and T-11-20: Replay mode is 100% read-only, displays a high-visibility amber banner `[REPLAY MODE - READ ONLY]`, and completely blocks/strips all mutating operator actions to ensure zero side effects.

#### Types & Trait Declarations
- **Structs (1):** `ReplayController`
- **Enums (1):** `ReplaySpeed`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn step_interval(&self) -> std::time::Duration;
// private
fn default() -> Self;
// pub
fn new() -> Self;
// pub
fn load_history(&mut self, history: Vec<EventEnvelope>);
// pub
fn exit(&mut self);
// pub
fn step_backward(&mut self) -> bool;
// pub
fn step_forward(&mut self) -> bool;
// pub
fn jump_to(&mut self, target: usize);
// pub
fn seek_to_start(&mut self) -> bool;
// pub
fn seek_to_end(&mut self) -> bool;
// pub
fn toggle_playback(&mut self);
// pub
fn advance_elapsed(&mut self, elapsed: std::time::Duration) -> bool;
// pub
fn tick_playback(&mut self) -> bool;
// pub
fn reconstruct_current_view(&self) -> TuiViewModel;
```

---

### `src/tui/routes.rs` {#src-tui-routes-rs}

- **Source Link:** [`src/tui/routes.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/routes.rs)
- **Lines of Code:** 737 (24270 bytes)

#### Primary Responsibility
Modular route composition (Principles 7–8).  Each route composes M31A's existing surfaces — no business logic, no I/O, no policy, no runtime calls. The previous giant `render_workspace()` match is preserved pixel-for-pixel here as small per-route functions so screens own their composition:  ```text Session = header + conversation + execution/tool activity + contextual inspector + composer + footer ```  Other routes keep M31A's visual design and responsive behavior unchanged (conversation + inspector split on wide terminals, single surface on narrow ones). `render_workspace()` in `shell/workspace.rs` remains the thin orchestrator (startup → welcome → route → composer → rail → detail → overlay) and delegates upper-area composition here.

#### Types & Trait Declarations
- **Structs (1):** `RouteContext`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn new(screen: ScreenId,
        focus: FocusTarget,
        context_selected_idx: usize,
        replay: &'a ReplayCont;
// pub
fn render_route_upper(f: &mut Frame,
    upper_area: Rect,
    model: &mut TuiViewModel,
    _composer: &TuiComposer,
  ;
// private
fn wide_split(area: Rect, left_pct: u16, right_pct: u16) -> (Rect, Rect);
// private
fn conversation_focused(ctx: &RouteContext<'_>) -> bool;
// private
fn panel_focused(ctx: &RouteContext<'_>) -> bool;
// pub
fn render_session(f: &mut Frame,
    area: Rect,
    model: &mut TuiViewModel,
    ctx: &RouteContext<'_>,
    tokens: &;
// private
fn render_split_with_selected(f: &mut Frame,
    area: Rect,
    model: &mut TuiViewModel,
    ctx: &RouteContext<'_>,
 ;
// pub
fn render_tasks(f: &mut Frame,
    area: Rect,
    model: &mut TuiViewModel,
    ctx: &RouteContext<'_>,
    tokens: &Th;
// pub
fn render_agents(f: &mut Frame,
    area: Rect,
    model: &mut TuiViewModel,
    ctx: &RouteContext<'_>,
    tokens: &T;
// pub
fn render_tools(f: &mut Frame,
    area: Rect,
    model: &mut TuiViewModel,
    ctx: &RouteContext<'_>,
    tokens: &Th;
// pub
fn render_git(f: &mut Frame,
    area: Rect,
    model: &mut TuiViewModel,
    ctx: &RouteContext<'_>,
    tokens: &Them;
// pub
fn render_verification(f: &mut Frame,
    area: Rect,
    model: &mut TuiViewModel,
    ctx: &RouteContext<'_>,
    toke;
// pub
fn render_jobs(f: &mut Frame,
    area: Rect,
    model: &mut TuiViewModel,
    ctx: &RouteContext<'_>,
    tokens: &The;
// pub
fn render_doctor(f: &mut Frame,
    area: Rect,
    model: &mut TuiViewModel,
    ctx: &RouteContext<'_>,
    tokens: &T;
// pub
fn render_models(f: &mut Frame,
    area: Rect,
    model: &mut TuiViewModel,
    ctx: &RouteContext<'_>,
    tokens: &T;
```

#### Unit Verification (1 inline tests)
Tests defined within module:
`every_route_composes_without_blank`

---

### `src/tui/runtime_bridge.rs` {#src-tui-runtime_bridge-rs}

- **Source Link:** [`src/tui/runtime_bridge.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/runtime_bridge.rs)
- **Lines of Code:** 2244 (94883 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate | 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Asynchronous Runtime Bridge for TUI Cockpit (COP-04, CLI-01, CLI-04, D-15).  Connects the synchronous 60 FPS TUI projection layer to the asynchronous `AppRuntime` core without violating Law 9 ("The model proposes. The runtime decides") or Law 15 (Zero database I/O during frame rendering).  Responsibilities: - Receives typed `ApplicationAction` from the composer/palette - Dispatches actions to `AppRuntime`, `SqliteSessionRepository`, and `SlashCommandRegistry` - Subscribes to `BroadcastEventBus` and transforms kernel events into `InteractionEvent`s - Streams `InteractionEvent`s back to the TUI update channel

#### Types & Trait Declarations
- **Structs (1):** `TuiRuntimeBridge`

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn send_action(&self, action: ApplicationAction) -> bool;
// pub
fn take_event_receiver(&mut self) -> Option<TuiInteractionReceiver>;
// pub
fn sender(&self) -> TuiActionSender;
// pub
async fn spawn(runtime: Arc<AppRuntime>,
        resume_session_id: Option<SessionId>,) -> Result<(Self, tokio::task::Jo;
// private
async fn hydrate_session_state(runtime: &Arc<AppRuntime>,
    session_repo: &SqliteSessionRepository,
    session: &Sess;
// private
fn response_to_hydration_events(resp: PreExecutionResponse, out: &mut Vec<InteractionEvent>);
// private
async fn run_bridge_worker(mut runtime: Arc<AppRuntime>,
    workspace_root: PathBuf,
    session_repo: SqliteSessionRep;
// private
async fn ensure_bridge_session(session: &'a mut Option<Session>,
    session_repo: &SqliteSessionRepository,
    workspa;
// private
async fn dispatch_bridge_action(action: ApplicationAction,
    runtime: &mut Arc<AppRuntime>,
    workspace_root: &Path,;
// private
async fn emit_workflow_snapshot_if_known(runtime: &AppRuntime,
    run_id_str: &str,
    event_tx: &TuiInteractionSender;
```

---

### `src/tui/sanitizer.rs` {#src-tui-sanitizer-rs}

- **Source Link:** [`src/tui/sanitizer.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/sanitizer.rs)
- **Lines of Code:** 184 (6803 bytes)

#### Primary Responsibility
Terminal Text Sanitization &amp; ANSI Escape Stripping (TUI-06, THREAT-01).  Mitigates T-11-18 (terminal control injection) by stripping dangerous ANSI sequences, OSC title overrides, and cursor repositioning commands before rendering untrusted repository, tool, web, or MCP content.

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn sanitize_terminal_text(input: &str) -> String;
// pub
fn sanitize_diff(diff: &str) -> String;
// pub
fn sanitize_tool_spool(spool: &str) -> String;
// pub
fn truncate_to_width(s: &str, max_width: usize) -> std::borrow::Cow<'_, str>;
// pub
fn truncate_str_safe(s: &str, max_width: usize) -> String;
// pub
fn format_display_model(raw: &str) -> String;
// private
fn test_format_display_model();
// private
fn test_sanitizer_strips_color_and_formatting();
// private
fn test_sanitizer_strips_cursor_repositioning_and_clearing();
// private
fn test_sanitizer_strips_osc_terminal_title_injection();
// private
fn test_unicode_safe_truncation_ascii();
// private
fn test_unicode_safe_truncation_limits_zero_and_one();
// private
fn test_unicode_safe_truncation_multibyte_and_emoji();
// private
fn test_unicode_safe_truncation_wide_and_combining();
// private
fn test_unicode_safe_truncation_no_allocation_when_fits();
```

#### Unit Verification (9 inline tests)
Tests defined within module:
`test_format_display_model`, `test_sanitizer_strips_color_and_formatting`, `test_sanitizer_strips_cursor_repositioning_and_clearing`, `test_sanitizer_strips_osc_terminal_title_injection`, `test_unicode_safe_truncation_ascii`, `test_unicode_safe_truncation_limits_zero_and_one`, `test_unicode_safe_truncation_multibyte_and_emoji`, `test_unicode_safe_truncation_wide_and_combining`, `test_unicode_safe_truncation_no_allocation_when_fits`

---

### `src/tui/screens/mod.rs` {#src-tui-screens-mod-rs}

- **Source Link:** [`src/tui/screens/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/screens/mod.rs)
- **Lines of Code:** 13 (484 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
TUI dialog screens.  Route composition lives in [`crate::tui::routes`]; this module hosts only the setup wizard dialog state machine. It owns no routing authority.

---

### `src/tui/screens/wizard.rs` {#src-tui-screens-wizard-rs}

- **Source Link:** [`src/tui/screens/wizard.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/screens/wizard.rs)
- **Lines of Code:** 3437 (143105 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
7-Step Guided Onboarding Setup Wizard Screen (FRX-02, FRX-03, D-02).  Interactive terminal wizard walking the operator through Workspace Trust, Doctor Diagnostics, Provider Selection, Model Selection, Profile Selection, Autonomy/Safety constraints, and Final Verification.

#### Types & Trait Declarations
- **Structs (2):** `DiscoveryReceiver`, `SetupWizardScreen`
- **Enums (4):** `ProviderVerificationState`, `WizardDiscoveryState`, `WizardOutcome`, `WizardProfile`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn all() -> &'static [Self];
// pub
fn canonical_id(&self) -> &'static str;
// pub
fn from_canonical_id(id: &str) -> Option<Self>;
// pub
fn name(&self) -> &'static str;
// pub
fn description(&self) -> &'static str;
// pub
fn recommendation(&self) -> &'static str;
// pub
fn autonomy_mode(&self) -> &'static str;
// pub
fn is_success(&self) -> bool;
// pub
fn badge(&self) -> &'static str;
// pub
fn is_loading(&self) -> bool;
// pub
fn is_ready(&self) -> bool;
// private
fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result;
// pub
fn new(workspace_path: PathBuf) -> Self;
// pub
fn with_config_scope(mut self, scope: crate::storage::ConfigScope) -> Self;
// pub
fn config_scope_label(&self) -> String;
```

---

### `src/tui/screens/workspace_setup.rs` {#src-tui-screens-workspace_setup-rs}

- **Source Link:** [`src/tui/screens/workspace_setup.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/screens/workspace_setup.rs)
- **Lines of Code:** 1043 (39798 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Focused Workspace Configuration Screen (Section 4).  Provides the canonical workspace configuration experience: - Focused, reliable, keyboard-driven interface. - Captures essential project facts without an artificial 7-step wizard. - Pre-fills sensible defaults via repository inspection (`Cargo.toml`, `package.json`, etc.). - Allows single-confirmation acceptance of detected defaults. - Atomically persists canonical configuration to `&lt;workspace&gt;/.m31a/M31A.toml`. - Never writes credentials or secrets to workspace files. - Preserves existing configuration sections during reconfiguration.

#### Types & Trait Declarations
- **Structs (2):** `DetectedRepoContext`, `WorkspaceSetupScreen`
- **Enums (5):** `GitIsolationChoice`, `PolicyPostureChoice`, `ProjectTypeChoice`, `SetupField`, `WorkspaceSetupOutcome`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn display_label(&self) -> &'static str;
// pub
fn from_str_loose(s: &str) -> Self;
// pub
fn as_str(&self) -> &'static str;
// pub
fn display_label(&self) -> &'static str;
// pub
fn from_str_loose(s: &str) -> Self;
// pub
fn as_str(&self) -> &'static str;
// pub
fn display_label(&self) -> &'static str;
// pub
fn from_str_loose(s: &str) -> Self;
// pub
fn inspect(root: &Path) -> Self;
// pub
fn title(&self) -> &'static str;
// pub
fn new(workspace_root: PathBuf) -> Self;
// private
fn load_from_existing(&mut self, path: &Path);
// pub
fn active_field(&self) -> SetupField;
// pub
fn active_field_idx(&self) -> usize;
```

---

### `src/tui/shell/context_rail.rs` {#src-tui-shell-context_rail-rs}

- **Source Link:** [`src/tui/shell/context_rail.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/shell/context_rail.rs)
- **Lines of Code:** 364 (13186 bytes)

#### Primary Responsibility
Contextual Right Rail for Active Session Workspace (MODE B).  Compact, secondary status information displayed alongside the primary conversation: - SESSION: active/working/waiting/ready state &amp; duration - ACTION: pending approval prompt if any - CURRENT: live working activity - CONTEXT: token count &amp; cost - TODO: task progress checklist - AGENTS: active agents &amp; roles - TOOLS: current or recent tool execution - GIT: branch &amp; working copy status - VERIFICATION: test/check summary

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn render_context_rail(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    tokens: &ThemeTokens,
    is_focused;
// pub
fn calculate_total_rail_lines(model: &TuiViewModel) -> usize;
// private
fn section_header(title: impl Into<String>, tokens: &ThemeTokens) -> Line<'static>;
// private
fn truncate_str(s: &str, max: usize) -> String;
```

---

### `src/tui/shell/footer.rs` {#src-tui-shell-footer-rs}

- **Source Link:** [`src/tui/shell/footer.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/shell/footer.rs)
- **Lines of Code:** 135 (4460 bytes)

#### Primary Responsibility
Quiet context-sensitive shell footer.  A single muted hint line. Focus is communicated by cursor placement and subtle selection — never by large `[COMPOSER] / [STREAM] / [MODAL]` badges.

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn render_footer(f: &mut Frame,
    area: Rect,
    screen: ScreenId,
    focus: FocusTarget,
    is_composer_focused: b;
// pub
fn render_footer_full(f: &mut Frame,
    area: Rect,
    screen: ScreenId,
    focus: FocusTarget,
    is_composer_focus;
// private
fn footer_hint(screen: ScreenId,
    focus: FocusTarget,
    is_composer_focused: bool,
    lifecycle: &crate::tui::life;
```

---

### `src/tui/shell/header.rs` {#src-tui-shell-header-rs}

- **Source Link:** [`src/tui/shell/header.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/shell/header.rs)
- **Lines of Code:** 200 (6769 bytes)

#### Primary Responsibility
Quiet application shell header (conversation-first).  Shows only high-value persistent information: `M31A · model · branch · state` Telemetry (tokens, cost, event counts, ids) lives in details/palette surfaces — never in the default header.

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn render_header(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    screen: ScreenId,
    replay: &ReplayContr;
// private
fn header_state(model: &'a TuiViewModel,
    tokens: &'a ThemeTokens,) -> (&'static str, String, Style);
// private
fn short_model_name(raw: &str) -> String;
// private
fn short_branch(model: &TuiViewModel) -> String;
// private
fn truncate(s: &str, max: usize) -> String;
```

---

### `src/tui/shell/mod.rs` {#src-tui-shell-mod-rs}

- **Source Link:** [`src/tui/shell/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/shell/mod.rs)
- **Lines of Code:** 11 (293 bytes)

#### Primary Responsibility
Persistent Application Shell (Section 5, TUI-01).

---

### `src/tui/shell/workspace.rs` {#src-tui-shell-workspace-rs}

- **Source Link:** [`src/tui/shell/workspace.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/shell/workspace.rs)
- **Lines of Code:** 1624 (65584 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Unified Workspace Orchestration &amp; Composition Surface (Section 5, 18, TUI-01).  Organizes the primary cockpit workspace into cohesive split-pane surfaces ensuring the operator never feels ejected from the autonomous execution loop.

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn render_workspace(f: &mut Frame,
    area: Rect,
    model: &mut TuiViewModel,
    composer: &TuiComposer,
    screen:;
// private
fn render_welcome_workspace(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    composer: &TuiComposer,
    tok;
// private
fn render_startup_workspace(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    composer: &TuiComposer,
    tok;
// private
fn render_unfocused_composer(f: &mut Frame,
    area: Rect,
    composer: &TuiComposer,
    is_busy: bool,
    is_waitin;
// private
fn render_detail_inspector(f: &mut Frame,
    area: Rect,
    detail: ViewId,
    model: &TuiViewModel,
    tokens: &The;
// private
fn render_view_overlay(f: &mut Frame,
    area: Rect,
    overlay: ViewId,
    model: &TuiViewModel,
    tokens: &ThemeT;
// pub(crate)
fn constrain_reading_width(area: Rect, max_width: u16) -> Rect;
// private
fn render_setup_wizard_overlay(f: &mut Frame,
    area: Rect,
    setup_wizard: &mut Option<SetupWizardScreen>,
    work;
// pub
fn format_keybindings_guide_lines() -> Vec<String>;
// pub
fn format_quarantine_manager_lines(model: &TuiViewModel) -> Vec<String>;
```

---

### `src/tui/state.rs` {#src-tui-state-rs}

- **Source Link:** [`src/tui/state.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/state.rs)
- **Lines of Code:** 159 (6167 bytes)

#### Primary Responsibility
TUI typed event flow: runtime outcomes enter presentation state through exactly one reducer.  The canonical store remains [`crate::tui::model::TuiViewModel`] (a pure in-memory projection; zero render-time I/O). This module provides:  - [`TuiEvent`]: the single typed bridge from runtime outcomes to UI state. - [`apply_tui_event`]: incremental reducer — each event touches only its relevant section (no full reloads, no conversation rebuilds per delta).  Production ingress is [`crate::tui::app::TuiApplication::poll_updates`], which wraps every drained bridge event as `TuiEvent::Interaction` and reduces it here. There is no second event path.

#### Types & Trait Declarations
- **Enums (1):** `TuiEvent`

#### Key Functions & Signatures (4 shown)
```rust
// private
fn from(ev: InteractionEvent) -> Self;
// pub
fn apply_tui_event(model: &mut TuiViewModel, event: &TuiEvent) -> usize;
// private
fn stream_delta_appends_incrementally_without_rebuild();
// private
fn startup_events_flip_only_startup_state();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`stream_delta_appends_incrementally_without_rebuild`, `startup_events_flip_only_startup_state`

---

### `src/tui/status.rs` {#src-tui-status-rs}

- **Source Link:** [`src/tui/status.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/status.rs)
- **Lines of Code:** 127 (3963 bytes)

#### Primary Responsibility
12-Status Presentation Taxonomy (TDS-04, D-03).  Provides the canonical dual symbol/bracketed badges and styling tokens for all operational statuses in M31A. Ensures color is never the sole carrier of semantic information.

#### Types & Trait Declarations
- **Structs (1):** `StatusPresentation`
- **Enums (1):** `StatusKind`

#### Key Functions & Signatures (5 shown)
```rust
// pub
fn badge(&self) -> &'static str;
// pub
fn label(&self) -> &'static str;
// pub
fn format(kind: StatusKind, theme: &ThemeTokens) -> (&'static str, Style);
// private
fn test_all_twelve_statuses_have_unique_badges();
// private
fn test_status_presentation_formatting();
```

#### Unit Verification (2 inline tests)
Tests defined within module:
`test_all_twelve_statuses_have_unique_badges`, `test_status_presentation_formatting`

---

### `src/tui/surface/agents.rs` {#src-tui-surface-agents-rs}

- **Source Link:** [`src/tui/surface/agents.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/agents.rs)
- **Lines of Code:** 289 (9256 bytes)

#### Primary Responsibility
Agent Swarm &amp; Autonomous Roles Surface (Section 14, TUI-01).  Visualizes autonomous agent swarm state, active tasks, token consumption, model routing, and operational status badges.

#### Types & Trait Declarations
- **Structs (1):** `AgentStateDisplay`

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn render_agents_surface(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    tokens: &ThemeTokens,
    is_focus;
// pub
fn map_agent_state(state: &str, tokens: &ThemeTokens) -> AgentStateDisplay;
// private
fn render_agents_table(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    tokens: &ThemeTokens,
    selected_i;
// private
fn render_agent_detail(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    tokens: &ThemeTokens,
    selected_i;
```

---

### `src/tui/surface/artifacts.rs` {#src-tui-surface-artifacts-rs}

- **Source Link:** [`src/tui/surface/artifacts.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/artifacts.rs)
- **Lines of Code:** 266 (8635 bytes)

#### Primary Responsibility
Artifact Explorer &amp; Output Management Surface (Section 28, TUI-01).  Visualizes generated artifacts, reports, test logs, and patches without freezing the UI or dumping massive outputs into the terminal buffer. Authoritative data derives purely from canonical runtime state (ArtifactService / TuiViewModel).

#### Key Functions & Signatures (4 shown)
```rust
// private
fn format_bytes(bytes: u64) -> String;
// pub
fn render_artifacts_surface(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    tokens: &ThemeTokens,
    is_fo;
// private
fn render_artifacts_list(f: &mut Frame,
    area: Rect,
    artifacts: &[TuiArtifactSnapshot],
    tokens: &ThemeTokens,;
// private
fn render_artifact_detail(f: &mut Frame,
    area: Rect,
    artifacts: &[TuiArtifactSnapshot],
    tokens: &ThemeTokens;
```

---

### `src/tui/surface/conversation.rs` {#src-tui-surface-conversation-rs}

- **Source Link:** [`src/tui/surface/conversation.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/conversation.rs)
- **Lines of Code:** 239 (8919 bytes)

#### Primary Responsibility
Primary conversational execution surface (conversation-first).  Quiet, open layout: no boxes around the stream, no telemetry dashboard. Hierarchy comes from spacing, role labels, and restrained emphasis.

#### Key Functions & Signatures (4 shown)
```rust
// pub
fn render_conversation_surface(f: &mut Frame,
    area: Rect,
    model: &mut TuiViewModel,
    tokens: &ThemeTokens,
  ;
// private
fn render_scrollbar(f: &mut Frame,
    area: Rect,
    total: usize,
    viewport: usize,
    scroll_top: usize,
    tok;
// private
fn inline_execution_line(model: &'a TuiViewModel, tokens: &'a ThemeTokens) -> Option<Line<'a>>;
// private
fn render_welcome_empty_state(lines: &mut Vec<Line<'_>>, tokens: &ThemeTokens);
```

---

### `src/tui/surface/decision.rs` {#src-tui-surface-decision-rs}

- **Source Link:** [`src/tui/surface/decision.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/decision.rs)
- **Lines of Code:** 177 (6309 bytes)

#### Primary Responsibility
Native interactive decision prompt surface.  Renders pending decisions (planning choices, plan reviews, tasks reviews, execution authorization, clarifications) as native TUI selectable option lists.

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn render_decision_prompt(f: &mut Frame,
    area: Rect,
    decision: &InteractiveDecision,
    tokens: &ThemeTokens,
 ;
```

---

### `src/tui/surface/doctor.rs` {#src-tui-surface-doctor-rs}

- **Source Link:** [`src/tui/surface/doctor.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/doctor.rs)
- **Lines of Code:** 137 (4731 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Doctor Diagnostics Surface (TUI-01, CLI-04).  Visualizes 6-category system health, environment prerequisites, and runtime configuration diagnostics.

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn render_doctor_surface(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    tokens: &ThemeTokens,
    is_focus;
```

---

### `src/tui/surface/git.rs` {#src-tui-surface-git-rs}

- **Source Link:** [`src/tui/surface/git.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/git.rs)
- **Lines of Code:** 208 (6900 bytes)

#### Primary Responsibility
Git Timeline &amp; Unstaged Diff Surface (Section 24, TUI-01).  Provides a dedicated, high-grade terminal diff inspection surface: - Branch status and worktree attribution - Diff metrics: files changed, +additions (green), -deletions (red) - Syntax-highlighted hunks with old/new line numbers - Scrollable viewport with non-blocking key navigation

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn render_git_surface(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    tokens: &ThemeTokens,
    is_focused:;
```

---

### `src/tui/surface/jobs.rs` {#src-tui-surface-jobs-rs}

- **Source Link:** [`src/tui/surface/jobs.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/jobs.rs)
- **Lines of Code:** 199 (7664 bytes)
- **Runtime Properties:** 🛑 Supports Cancellation Tokens

#### Primary Responsibility
Process Sandboxing &amp; Background Jobs Surface (TUI-01).  Visualizes background process execution, isolation tiers, sandboxing, CPU/duration telemetry, and process lifecycle states.

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn render_jobs_surface(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    tokens: &ThemeTokens,
    is_focused;
```

---

### `src/tui/surface/mod.rs` {#src-tui-surface-mod-rs}

- **Source Link:** [`src/tui/surface/mod.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/mod.rs)
- **Lines of Code:** 78 (2482 bytes)

#### Primary Responsibility
Contextual Application Surfaces (Section 5, 6, 12–29).  Replaces disconnected 40 screens with contextual surfaces, routes, panels, and progressive master-detail projections.

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn visible_list_range(total_items: usize,
    selected_idx: usize,
    viewport_height: usize,) -> (usize, usize);
```

---

### `src/tui/surface/model_selector.rs` {#src-tui-surface-model_selector-rs}

- **Source Link:** [`src/tui/surface/model_selector.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/model_selector.rs)
- **Lines of Code:** 601 (19897 bytes)

#### Primary Responsibility
Models Surface.  Renders live model provider state and allows switching providers/models via canonical runtime actions.

#### Types & Trait Declarations
- **Structs (3):** `ModelInfo`, `ModelSelectorState`, `ProviderInfo`
- **Enums (2):** `ModelSelectorAction`, `ModelSelectorMode`

#### Key Functions & Signatures (10 shown)
```rust
// pub
fn new() -> Self;
// pub
fn render_model_selector(f: &mut Frame,
    area: Rect,
    providers: &[ProviderInfo],
    models: &[ModelInfo],
    cu;
// private
fn render_model_selector_header(f: &mut Frame,
    area: Rect,
    current_provider: &str,
    current_model: &str,
    ;
// private
fn render_providers_list(f: &mut Frame,
    area: Rect,
    providers: &[ProviderInfo],
    tokens: &ThemeTokens,
    bo;
// private
fn render_models_list(f: &mut Frame,
    area: Rect,
    models: &[ModelInfo],
    tokens: &ThemeTokens,
    border_styl;
// private
fn render_current_config(f: &mut Frame,
    area: Rect,
    current_provider: &str,
    current_model: &str,
    current;
// pub
fn handle_model_selector_key(key: crossterm::event::KeyEvent,
    ui_state: &mut ModelSelectorState,
    providers: &[Pr;
// pub
fn resolve_display_models_and_providers(catalog_models: &[crate::model::router::resolver::ModelCandidate],
    active_pr;
// pub
fn resolve_display_models_and_providers_full(catalog_models: &[crate::model::router::resolver::ModelCandidate],
    acti;
// pub
fn is_catalog_empty(models: &[ModelInfo]) -> bool;
```

---

### `src/tui/surface/replay.rs` {#src-tui-surface-replay-rs}

- **Source Link:** [`src/tui/surface/replay.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/replay.rs)
- **Lines of Code:** 129 (3840 bytes)

#### Primary Responsibility
Post-Mortem Event Replay Surface (Section 27, TUI-01, T-11-20).  Visualizes historical event timelines with step-by-step playback: - Clear, unmistakable [REPLAY / POST-MORTEM - READ-ONLY] indicator - Play/pause, step forward/backward, speed multiplier controls - State reconstruction inspection at each historical frame

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn render_replay_surface(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    replay: &ReplayController,
    tok;
```

---

### `src/tui/surface/settings.rs` {#src-tui-surface-settings-rs}

- **Source Link:** [`src/tui/surface/settings.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/settings.rs)
- **Lines of Code:** 1506 (57910 bytes)

#### Primary Responsibility
Settings surface — projection/editor of the canonical configuration system.  `/settings` is a projection/editor of `ResolvedConfiguration`, never a second configuration system. Categories mirror the actual `AppConfig` schema; every row shows value, source/provenance, and restart-required state. Edits validate through the typed schema, preview, confirm, atomically persist, and reload the effective configuration.

#### Types & Trait Declarations
- **Structs (2):** `SettingsRow`, `SettingsState`
- **Enums (2):** `SettingsAction`, `SettingsCategory`

#### Key Functions & Signatures (15 shown)
```rust
// pub
fn all() -> &'static [Self];
// pub
fn title(&self) -> &'static str;
// pub
fn from_str_relaxed(s: &str) -> Option<Self>;
// pub
fn text(key: impl Into<String>,
        label: impl Into<String>,
        value: impl Into<String>,) -> Self;
// pub
fn read_only(key: impl Into<String>,
        label: impl Into<String>,
        value: impl Into<String>,) -> Self;
// pub
fn new() -> Self;
// pub
fn category(&self) -> SettingsCategory;
// pub
fn select_category(&mut self, cat: SettingsCategory);
// pub
fn mask_secret_configured(present: bool) -> String;
// pub
fn mask_credential_status(status: &crate::tui::model::TuiCredentialStatus) -> String;
// pub
fn rows_for_category(category: SettingsCategory,
    config: &crate::config::ResolvedConfiguration,
    catalog: Option<;
// pub
fn rows_for_category_full(category: SettingsCategory,
    config: &crate::config::ResolvedConfiguration,
    catalog: Op;
// pub
fn rows_for_category_with_cred_status(category: SettingsCategory,
    config: &crate::config::ResolvedConfiguration,
   ;
// pub
fn handle_settings_key(key: crossterm::event::KeyEvent,
    state: &mut SettingsState,
    row_count: usize,
    editing;
// pub
fn render_settings(f: &mut Frame,
    area: Rect,
    state: &mut SettingsState,
    rows: &[SettingsRow],
    tokens: &;
```

#### Unit Verification (4 inline tests)
Tests defined within module:
`settings_categories_cover_schema`, `empty_catalog_renders_explicit_state`, `secret_values_are_masked`, `test_reset_draft_field_to_default_preserves_other_edits`

---

### `src/tui/surface/tasks.rs` {#src-tui-surface-tasks-rs}

- **Source Link:** [`src/tui/surface/tasks.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/tasks.rs)
- **Lines of Code:** 334 (12011 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Task DAG &amp; Master-Detail Inspection Surface (Section 13, TUI-01).  Provides dense, structured DAG visualization with master/detail inspection: - Master list of tasks with status glyphs (✓, ▶, ✗, ○) and progress bars - Detail pane showing assigned agent, dependencies, progress %, inputs/outputs, verification status, and execution attempts

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn render_tasks_surface(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    tokens: &ThemeTokens,
    is_focuse;
// private
fn render_task_master_list(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    tokens: &ThemeTokens,
    select;
// private
fn render_task_detail_pane(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    tokens: &ThemeTokens,
    select;
```

---

### `src/tui/surface/telemetry.rs` {#src-tui-surface-telemetry-rs}

- **Source Link:** [`src/tui/surface/telemetry.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/telemetry.rs)
- **Lines of Code:** 162 (5403 bytes)

#### Primary Responsibility
Telemetry &amp; Model Usage Surface (Section 23, TUI-01).  Provides comprehensive observability over runtime operations: - Token consumption (prompt, completion, total) and estimated financial cost - Uptime, processed event counts, RSS memory usage - Active provider, model tier, and execution profile

#### Key Functions & Signatures (1 shown)
```rust
// pub
fn render_telemetry_surface(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    tokens: &ThemeTokens,
    is_fo;
```

---

### `src/tui/surface/tools.rs` {#src-tui-surface-tools-rs}

- **Source Link:** [`src/tui/surface/tools.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/tools.rs)
- **Lines of Code:** 280 (9210 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Tool &amp; Capability Telemetry Surface (Section 8, TUI-01).  Visualizes registered canonical tools, execution traces, error rates, risk tiers, and invocation telemetry backed by ToolRegistry and runtime events.

#### Types & Trait Declarations
- **Structs (1):** `DisplayToolItem`

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn render_tools_surface(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    tokens: &ThemeTokens,
    is_focuse;
// private
fn render_tools_list(f: &mut Frame,
    area: Rect,
    tools: &[DisplayToolItem],
    tokens: &ThemeTokens,
    selecte;
// private
fn render_tool_detail(f: &mut Frame,
    area: Rect,
    tools: &[DisplayToolItem],
    tokens: &ThemeTokens,
    select;
```

---

### `src/tui/surface/verification.rs` {#src-tui-surface-verification-rs}

- **Source Link:** [`src/tui/surface/verification.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/verification.rs)
- **Lines of Code:** 337 (11708 bytes)
- **Runtime Properties:** 🛡️ Enforces Policy Gate

#### Primary Responsibility
Verification Gates &amp; Proof Evidence Surface (Section 25, TUI-01).  Visualizes independent verification gates, checks, execution evidence, failure classifications, and proof artifacts backed by canonical runtime state.

#### Key Functions & Signatures (3 shown)
```rust
// pub
fn render_verification_surface(f: &mut Frame,
    area: Rect,
    model: &TuiViewModel,
    tokens: &ThemeTokens,
    is;
// private
fn render_checks_list(f: &mut Frame,
    area: Rect,
    checks: &[TuiVerificationCheck],
    tokens: &ThemeTokens,
    ;
// private
fn render_check_evidence(f: &mut Frame,
    area: Rect,
    checks: &[TuiVerificationCheck],
    model: &TuiViewModel,
 ;
```

---

### `src/tui/surface/workflow.rs` {#src-tui-surface-workflow-rs}

- **Source Link:** [`src/tui/surface/workflow.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/surface/workflow.rs)
- **Lines of Code:** 907 (29186 bytes)

#### Primary Responsibility
Workflow Visual Dashboard Surface.  Renders live workflow execution state from WorkflowExecutionSnapshot. Conversation-first: opens as detail inspector on TaskGraph screen.

#### Types & Trait Declarations
- **Structs (1):** `WorkflowDashboardState`
- **Enums (2):** `WorkflowAction`, `WorkflowViewMode`

#### Key Functions & Signatures (11 shown)
```rust
// pub
fn new() -> Self;
// pub
fn render_workflow_dashboard(f: &mut Frame,
    area: Rect,
    snapshot: &WorkflowExecutionSnapshot,
    tokens: &Theme;
// private
fn render_workflow_header(f: &mut Frame,
    area: Rect,
    snapshot: &WorkflowExecutionSnapshot,
    tokens: &ThemeTok;
// private
fn status_style_for_run(status: WorkflowRunState, tokens: &ThemeTokens) -> Style;
// private
fn step_status_style(status: WorkflowStepState, tokens: &ThemeTokens) -> (Style, &'static str);
// private
fn render_overview(f: &mut Frame,
    area: Rect,
    snapshot: &WorkflowExecutionSnapshot,
    tokens: &ThemeTokens,
  ;
// private
fn render_step_graph(f: &mut Frame,
    area: Rect,
    snapshot: &WorkflowExecutionSnapshot,
    tokens: &ThemeTokens,
;
// private
fn render_step_inspector(f: &mut Frame,
    area: Rect,
    snapshot: &WorkflowExecutionSnapshot,
    tokens: &ThemeToke;
// private
fn render_controls(f: &mut Frame,
    area: Rect,
    snapshot: &WorkflowExecutionSnapshot,
    tokens: &ThemeTokens,
  ;
// private
fn truncate(s: &str, max_len: usize) -> String;
// pub
fn handle_workflow_dashboard_key(key: crossterm::event::KeyEvent,
    ui_state: &mut WorkflowDashboardState,
    snapsho;
```

---

### `src/tui/theme.rs` {#src-tui-theme-rs}

- **Source Link:** [`src/tui/theme.rs` on GitHub](https://github.com/eshanized/M31A/blob/3eddbfd3c296515c44268b386271dde0107c6a8b/src/tui/theme.rs)
- **Lines of Code:** 431 (18014 bytes)

#### Primary Responsibility
Centralized Theme &amp; Design Token System (TDS-03, D-03).  Provides semantic design tokens for the conversation-first M31A TUI. All renderers must style through these tokens — never scatter literal `Color::Cyan / Yellow / Magenta` through presentation code.  The default theme ("Default" / M31A) is a restrained developer-oriented palette: neutral canvas, subtle separators, muted text hierarchy, and a single quiet accent. Status meaning is carried by symbol + text, never by color alone.

#### Types & Trait Declarations
- **Structs (1):** `ThemeTokens`
- **Enums (1):** `ThemeMode`

#### Key Functions & Signatures (13 shown)
```rust
// pub
fn as_str(&self) -> &'static str;
// pub
fn cycle(&self) -> Self;
// pub
fn from_str_relaxed(s: &str) -> Self;
// pub
fn canonical_default() -> Self;
// pub
fn to_config_str(&self) -> &'static str;
// pub
fn resolve(mode: ThemeMode) -> Self;
// pub
fn is_no_color_active() -> bool;
// pub
fn is_mono(&self) -> bool;
// private
fn m31a_default() -> Self;
// private
fn dark_slate_cyan_calm() -> Self;
// private
fn high_contrast() -> Self;
// private
fn clean_light() -> Self;
// private
fn monochrome_ansi() -> Self;
```

---
